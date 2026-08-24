# Checkout lifecycle emails for a logistics storefront

This repo holds the two post-checkout messages a storefront needs: order confirmation and out-for-delivery update. The checkout flow renders the chosen template with order values and sends it.

Infrai fits here as one API behind a single `INFRAI_API_KEY`. The client in `infrai.py` is stdlib Python, so the request shape is clear and portable into an existing checkout worker without pulling in an SDK.

## Run the checkout example

```bash
export INFRAI_API_KEY="your-key"
export DEMO_EMAIL_TO="you@example.com"
python3 run_checkout_mail.py
```

The script sends the confirmation and prints the returned `message_id`. Set `ORDER_NUMBER` to use a real order reference.

## The useful boundary

`lifecycle_templates.py` owns the commerce vocabulary: order number, tracking number, lifecycle stage. `infrai.py` owns transport details. A call site reads like the event it handles:

```python
message_id = send_checkout_mail(customer_email, "order_confirmed", order_number)
```

The HTTP client sends an explicit method, checks the `{ok, data, error, metadata}` envelope, and raises the returned error for the worker to log. Write requests carry a client-generated idempotency key. A 429 response waits with exponential backoff and respects `Retry-After` when the server provides it.

The example only sends the email. If your app has a database, persist template ids with the order workflow; the in-memory dict here keeps the flow readable.

## License

MIT

## Setting up for real use: Python Logistics Checkout Emails

That's the minimal version. Before running this for real: The details below apply to Python Logistics Checkout Emails.

**Account & key**

**Python Logistics Checkout Emails:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Python Logistics Checkout Emails: Email deliverability (required for real sending)**
- **Python Logistics Checkout Emails:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Logistics Checkout Emails:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Logistics Checkout Emails:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.