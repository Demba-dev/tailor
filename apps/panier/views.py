from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .cart import Cart
from django.contrib import messages
import json

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'panier/detail.html', {'cart': cart})

@login_required
@require_POST
def cart_add(request, item_type, item_id):
    cart = Cart(request)
    cart.add(item_type=item_type, item_id=item_id)
    messages.success(request, f"Ajouté au panier avec succès.")
    return redirect(request.META.get('HTTP_REFERER', 'panier:cart_detail'))

@login_required
def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    return redirect('panier:cart_detail')

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('panier:cart_detail')

@login_required
@require_http_methods(["POST"])
def update_quantity(request):
    try:
        data = json.loads(request.body)
        key = data.get('key')
        delta = int(data.get('delta', 0))
        
        cart = Cart(request)
        
        if key not in cart.cart:
            return JsonResponse({'success': False, 'message': 'Article non trouvé'})
        
        current_qty = cart.cart[key]['quantity']
        new_qty = current_qty + delta
        
        if new_qty <= 0:
            cart.remove(key)
        else:
            cart.cart[key]['quantity'] = new_qty
            cart.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_http_methods(["POST"])
def remove_item(request):
    try:
        data = json.loads(request.body)
        key = data.get('key')
        
        cart = Cart(request)
        cart.remove(key)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_http_methods(["POST"])
def clear_cart(request):
    try:
        cart = Cart(request)
        cart.clear()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
