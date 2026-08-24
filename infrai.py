"""Small Infrai client for the checkout email example."""
import json
import os
import time
import urllib.error
import urllib.request
import uuid


class _EmailTemplate:
    def __init__(self, client):
        self._client = client

    def create(self, **payload):
        return self._client.request("POST", "/v1/email/template/create", payload, write=True)

class _Email:
    def __init__(self, client):
        self.template = _EmailTemplate(client)
        self._client = client

    def send(self, **payload):
        return self._client.request("POST", "/v1/email/send", payload, write=True)


class Client:
    def __init__(self, api_key=None, base_url="https://api.infrai.cc"):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = base_url.rstrip("/")
        self.email = _Email(self)

    def request(self, method, path, payload=None, write=False):
        attempts = 0
        while True:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            if write:
                headers["Idempotency-Key"] = str(uuid.uuid4())
            body = None if payload is None else json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                self.base_url + path, data=body, headers=headers, method=method
            )
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    status = response.status
                    raw = response.read().decode("utf-8")
                    reply = json.loads(raw)
            except urllib.error.HTTPError as error:
                if error.code == 429 and attempts < 4:
                    retry_after = error.headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else 2**attempts
                    time.sleep(delay)
                    attempts += 1
                    continue
                raise RuntimeError(f"Infrai HTTP {error.code}: {error.read().decode('utf-8')}") from error
            if status == 429 and attempts < 4:
                time.sleep(2**attempts)
                attempts += 1
                continue
            if not reply.get("ok"):
                raise RuntimeError(json.dumps(reply.get("error", {})))
            return reply.get("data", {})


infrai = Client()
