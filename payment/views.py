import json
import stripe

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import PaymentForm
from store_basket.basket import Basket
from orders.views import payment_confirmation


@login_required
def BasketView(request):
    form = PaymentForm(instance=request.user)
    basket = Basket(request)
    total = int(str(basket.get_total_price()).replace('.', ''))

    stripe.api_key = 'sk_test_51NdwzECloRCyzDNGuvBbXBqPjibk9RpQ4ezYdqRlQeudnuyRSQnnv4ujcM1ewlJtbZ6iJEUXjtAqDvrfs3qsAbRK00nuWKnuYb'
    intent = stripe.PaymentIntent.create(
        amount = total,
        currency = 'eur',
        metadata={'userid': request.user.id}
    )

    return render(request, 'store/payment/home.html', {'form': form, 'client_secret': intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'store/payment/orderplaced.html')