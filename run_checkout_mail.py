"""Create checkout lifecycle templates and send one order update."""
import os

from lifecycle_templates import send_checkout_mail


def main():
    recipient = os.environ["DEMO_EMAIL_TO"]
    order_number = os.environ.get("ORDER_NUMBER", "STORE-1042")
    message_id = send_checkout_mail(recipient, "order_confirmed", order_number)
    print(f"sent order confirmation: {message_id}")


if __name__ == "__main__":
    main()
