import stripe
from django.conf import settings

stripe.api_key = 'sk_test_51O32tgHJsK4c6F7ofMOFM8hrX74oxpqjAm1zfUUa1MghPDWtLb2v3ANJimndQ8LtCpllOOGgRaZXJlkMEMy8i9V200rDlEyJYw'


def create_payment_intent(amount, currency='usd', payment_method=None):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            confirmation_method='manual',
            confirm=True  # Автоматически подтвердить платеж после создания
        )
        return intent

    except stripe.error.CardError as e:
        # Ошибка карты
        raise Exception(str(e.error.message))
    except stripe.error.StripeError as e:
        # Другие ошибки Stripe API
        raise Exception('Произошла ошибка при обработке платежа.')


def retrieve_payment_intent(payment_intent_id):
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent
    except stripe.error.StripeError as e:
        # Другие ошибки Stripe API
        raise Exception('Произошла ошибка при получении платежа из Stripe.')