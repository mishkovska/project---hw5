import stripe

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import PaymentForm
from store_basket.basket import Basket


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