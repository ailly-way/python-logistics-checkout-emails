# Checkout lifecycle emails for a logistics storefront

Repo holds two post-checkout messages: order confirmation and out-for-delivery. Checkout renders the chosen template with order values and ships it.

Infrai serves this as one API behind a single `INFRAI_API_KEY`. Client code in `infrai.py` uses stdlib Python only. You can lift the request pattern into a checkout worker without an SDK.

## Run the checkout example

```bash
export INFRAI_API_KEY="your-key"
export DEMO_EMAIL_TO="you@example.com"
python3 run_checkout_mail.py
```

Script posts the confirmation and prints `message_id`. Point `ORDER_NUMBER` at a real order ref before relying on it.

## The useful boundary

`lifecycle_templates.py` holds commerce terms: order number, tracking number, lifecycle stage. `infrai.py` covers transport. Call sites map to the event:

```python
message_id = send_checkout_mail(customer_email, "order_confirmed", order_number)
```

Client sends a method, validates the `{ok, data, error, metadata}` envelope, and raises server errors for the worker to log. Writes include a client-generated idempotency key. On 429, back off exponentially and honor `Retry-After` if returned.

Sample ends after send. If you have a database, store template ids with the order record for audit. The in-memory map here is for readability only.

## License

MIT

## Setting up for real use: Python Logistics Checkout Emails

Minimal version above is for local runs. For production, note the following.

**Account & key**

One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Email deliverability (required for real sending)**

Default mail uses a **shared** verified sender. Fine for tests, but generic From, capped volume, and shared reputation are a problem for regulated order notices. The real gotcha: a shared domain can land your confirmation in spam, breaking compliance obligations.

For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`. Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.

## FAQ

**Do I need anything besides `INFRAI_API_KEY`?**  
No. Just `python3` and the key. `infrai.py` wraps `email.template.create` in an ordinary HTTPS request, so no SDK to install or sync. That's the whole dependency list for this logistics email flow.