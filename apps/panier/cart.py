from decimal import Decimal
from django.conf import settings
from apps.catalogue.models import TypeHabit
from apps.modeles.models import Modele
from apps.tissus.models import Tissu

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {'items': {}}
        self.cart = cart

    def add(self, item_type, item_id, quantity=1):
        item_key = f"{item_type}_{item_id}"
        if item_key not in self.cart['items']:
            self.cart['items'][item_key] = {
                'type': item_type,
                'id': item_id,
                'quantity': 0
            }
        self.cart['items'][item_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item_key):
        if item_key in self.cart['items']:
            del self.cart['items'][item_key]
            self.save()

    def __iter__(self):
        items = self.cart['items'].items()
        for key, item in items:
            item['key'] = key
            if item['type'] == 'habit':
                obj = TypeHabit.objects.get(pk=item['id'])
                item['obj'] = obj
                item['price'] = obj.prix_standard
            elif item['type'] == 'modele':
                obj = Modele.objects.get(pk=item['id'])
                item['obj'] = obj
                item['price'] = obj.prix_main_oeuvre
            elif item['type'] == 'tissu':
                obj = Tissu.objects.get(pk=item['id'])
                item['obj'] = obj
                item['price'] = obj.prix_metre
            
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart['items'].values())

    def get_total_price(self):
        total = 0
        for item in self:
            total += item['total_price']
        return total

    def clear(self):
        del self.session['cart']
        self.save()
