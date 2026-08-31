from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine

# Home Page View
def home(request):
    medicines = Medicine.objects.all()
    return render(request, 'home.html', {'medicines': medicines})

# Add to Cart View (Session based)
def add_to_cart(request, medicine_id):
    cart = request.session.get('cart', {})
    medicine_id_str = str(medicine_id)
    
    if medicine_id_str in cart:
        cart[medicine_id_str] += 1
    else:
        cart[medicine_id_str] = 1
        
    request.session['cart'] = cart
    return redirect('cart_detail')

# Cart Detail View
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for medicine_id, quantity in cart.items():
        medicine = get_object_or_404(Medicine, id=medicine_id)
        item_total = medicine.price * quantity
        total_price += item_total
        cart_items.append({
            'medicine': medicine,
            'quantity': quantity,
            'item_total': item_total
        })
        
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

# Clear Cart View
def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart_detail')