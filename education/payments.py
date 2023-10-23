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


