"""Checkout lifecycle templates and the message sender."""
import os
import uuid

from infrai import infrai


TEMPLATES = {
    "order_confirmed": {
        "subject": "Order {{order_number}} is confirmed",
        "html": "<h1>Thanks for your order</h1><p>We are preparing {{order_number}} for dispatch.</p>",
    },
    "out_for_delivery": {
        "subject": "Order {{order_number}} is out for delivery",
        "html": "<h1>Your parcel is moving</h1><p>Track {{order_number}} with {{tracking_number}}.</p>",
    },
}


def create_templates():
    namespace = os.environ.get("TEMPLATE_NAMESPACE", "storefront-checkout")
    ids = {}
    for stage, content in TEMPLATES.items():
        name = f"{namespace}-{stage}-{uuid.uuid4().hex[:10]}"
        data = infrai.email.template.create(
            name=name, subject=content["subject"], html=content["html"]
        )
        ids[stage] = data["template_id"]
    return ids


def send_checkout_mail(to, stage, order_number, tracking_number=None):
    values = {"order_number": order_number}
    if tracking_number:
        values["tracking_number"] = tracking_number
    content = TEMPLATES[stage]
    subject = content["subject"]
    html = content["html"]
    for name, value in values.items():
        placeholder = "{{" + name + "}}"
        subject = subject.replace(placeholder, value)
        html = html.replace(placeholder, value)
    data = infrai.email.send(to=to, subject=subject, html=html)
    return data["message_id"]
