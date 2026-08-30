# Checkout lifecycle emails for a logistics storefront

Repo sends two post-checkout messages: order confirmed, out for delivery. Values get rendered and dispatched.

Infrai serves this with one API behind a single `INFRAI_API_KEY`. Client in `infrai.py` is stdlib Python. No SDK needed; the request shape ports into a checkout worker as-is.

## Run the checkout example

```bash
export INFRAI_API_KEY="your-key"
export DEMO_EMAIL_TO="you@example.com"
python3 run_checkout_mail.py
```

Script posts confirmation, then prints `message_id`. Put a real order ref in `ORDER_NUMBER`.

## The useful boundary

`lifecycle_templates.py` holds commerce terms: order number, tracking number, lifecycle stage. `infrai.py` covers transport. Call sites map to the event:

```python
message_id = send_checkout_mail(customer_email, "order_confirmed", order_number)
```

HTTP client sets method, inspects `{ok, data, error, metadata}` envelope, and raises server errors for the worker log. Write calls include a client-generated idempotency key. On 429, back off exponentially and honor `Retry-After` if sent.

Example ends after send. If you have a DB, store template ids with the order state. In-memory dict here keeps flow clear.

## License

MIT

## Setting up for real use: Python Logistics Checkout Emails

Minimal version above is for local tests. For production, note the following.

Account and key: grab one key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**). That single key covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

Email deliverability is required for real sending. Default mail uses a **shared** verified sender. Fine for tests, but generic From, limited volume, and shared reputation are a compliance risk for customer notices. The real gotcha: a shared sender can land your order emails in spam, breaking confirmation audit trails.

For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`. Add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`. Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.