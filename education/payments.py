from django.http import JsonResponse
from .stripe_helpers import create_payment_intent, retrieve_payment_intent
from django.views.decorators.csrf import csrf_exempt


def create_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency = 'usd'
        payment_method = request.POST.get('payment_method')

        try:
            payment_intent = create_payment_intent(amount, currency, payment_method)
            return JsonResponse({'client_secret': payment_intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def retrieve_payment(request, payment_intent_id):
    try:
        payment_intent = retrieve_payment_intent(payment_intent_id)
        return JsonResponse({'status': payment_intent.status})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#
#
# def create_payment(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         currency = 'usd'  # Ваша валюта (может быть изменена)
#         payment_method = request.POST.get('payment_method')
#
#         payment_intent = create_payment_intent(amount, currency, payment_method)
#         return JsonResponse({'client_secret': payment_intent.client_secret})
#     return JsonResponse({'error': 'Invalid request method'})
#
#
# def retrieve_payment(request, payment_intent_id):
#     payment_intent = retrieve_payment_intent(payment_intent_id)
#     return JsonResponse({'status': payment_intent.status})



# import stripe
# from django.http import JsonResponse
#
# stripe.api_key = "sk_test_51O32tgHJsK4c6F7ofMOFM8hrX74oxpqjAm1zfUUa1MghPDWtLb2v3ANJimndQ8LtCpllOOGgRaZXJlkMEMy8i9V200rDlEyJYw"
#
# def create_payment(request):
#     amount = 2000  # Сумма платежа в центах (например, 2000 центов = $20.00)
#     currency = 'usd'  # Валюта платежа (например, 'usd' для долларов США)
#
#     intent = stripe.PaymentIntent.create(
#         amount=amount,
#         currency=currency,
#         payment_method=request.POST['payment_method_id'],
#         confirmation_method='automatic',
#         confirm=True,
#     )
#
#     return generate_response(intent)
#
#
# def generate_response(intent):
#     status = intent['status']
#     if status == 'requires_action' or status == 'requires_payment_method' or status == 'requires_confirmation':
#         # Клиент должен предоставить дополнительные действия для завершения транзакции
#         return JsonResponse({'requires_action': True, 'payment_intent_client_secret': intent.client_secret})
#     elif status == 'succeeded':
#         # Платеж успешно завершен
#         return JsonResponse({'success': True})
#     else:
#         # Другие статусы могут указывать на ошибку в процессе оплаты
#         return JsonResponse({'error': 'Invalid PaymentIntent status'})




# def create_payment_intent(amount, currency, payment_method):
#     return stripe.PaymentIntent.create(
#         amount=amount,
#         currency=currency,
#         payment_method=payment_method,
#         confirmation_method='manual',
#         confirm=True,
#     )
#
#
# def retrieve_payment_intent(payment_intent_id):
#     return stripe.PaymentIntent.retrieve(payment_intent_id)
