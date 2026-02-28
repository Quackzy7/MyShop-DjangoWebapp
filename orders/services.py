import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(order):

    intent = stripe.PaymentIntent.create(
        amount=int(order.total_price * 100), #amount in cents/paisa
        currency="usd",
        metadata={"order_id": order.id}
    )

    payment = Payment.objects.create(
        order=order,
        payment_method="stripe",
        transaction_id=intent.id,
        amount=order.total_price,
        status="pending"
    )

    return intent.client_secret


def confirm_stripe_payment(intent_id):
    intent = stripe.PaymentIntent.retrieve(intent_id)

    payment = Payment.objects.get(transaction_id=intent_id)
    if intent.status == "succeeded":
        payment.status = "completed"
        payment.save()
        
        order = payment.order
        order.is_paid = True 
        order.save()
        
    return payment.order