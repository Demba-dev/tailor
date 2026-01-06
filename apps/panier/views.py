from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib import messages

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'panier/detail.html', {'cart': cart})

@require_POST
def cart_add(request, item_type, item_id):
    cart = Cart(request)
    cart.add(item_type=item_type, item_id=item_id)
    messages.success(request, f"Ajouté au panier avec succès.")
    return redirect(request.META.get('HTTP_REFERER', 'panier:cart_detail'))

def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    return redirect('panier:cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('panier:cart_detail')
