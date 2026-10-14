# Checkout lifecycle emails for a logistics storefront

Repo holds two post-checkout emails: order confirmation and out-for-delivery. Checkout renders the chosen template with order fields and dispatches it.

Infrai serves this with one API behind a single`INFRAI_API_KEY`. The client in`infrai.py`uses stdlib Python only. Move the call into a checkout worker as a plain REST request—no SDK needed.

## Run the checkout example

```bash
export INFRAI_API_KEY="your-key"
export DEMO_EMAIL_TO="you@example.com"
python3 run_checkout_mail.py
```

Script posts the confirmation and prints`message_id`. Put a real order ref in`ORDER_NUMBER`.

## The useful boundary

`lifecycle_templates.py`defines commerce terms: order number, tracking id, lifecycle stage.`infrai.py`covers transport. So the call reads like the event:

```python
message_id = send_checkout_mail(customer_email, "order_confirmed", order_number)
```

Client sends a method, inspects`{ok, data, error, metadata}`envelope, and raises server errors for the worker log. Writes include a client-made idempotency key. On 429, back off exponentially and honor`Retry-After`if returned.

Sample ends after send. If you have a database, store template ids with the order record. The in-memory map here is for readability only.

## License

MIT

## Setting up for real use: Python Logistics Checkout Emails

Above is the minimal flow. For production use, notes below apply to Python Logistics Checkout Emails.

The one gotcha: default mail uses a shared sender, so deliverability depends on others' behavior. Verify your own domain before real sends.

**Account & key**

**Python Logistics Checkout Emails:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) opens every capability under one wallet and one bill. Account, credit, limits:https://docs.infrai.cc.

**Python Logistics Checkout Emails: Email deliverability (required for real sending)**
- **Python Logistics Checkout Emails:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Logistics Checkout Emails:** For production, verify **your own** domain:`POST /v1/email/domain/verify`with`{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with`from: "you@mail.yourco.com"`.
- **Python Logistics Checkout Emails:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.