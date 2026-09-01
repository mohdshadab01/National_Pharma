from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine
from .forms import PrescriptionForm
from .utils import parse_prescription_image

# ⚠️ Apni Google AI Studio ki Gemini API Key yahan paste karein
GEMINI_API_KEY = "AQ.Ab8RN6JTnB1RAQTM3uxL2V7UBCYfcWfUT7TQUolCu2Z09YQ6Vw  "

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

# AI Prescription Upload & Auto-Detect View
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription_obj = form.save()
            
            # AI scanning execution
            detected_medicines = parse_prescription_image(
                prescription_obj.prescription_file.path, 
                GEMINI_API_KEY
            )
            
            # Database medicines se match (Automatic check logic)
            all_medicines = Medicine.objects.all()
            matched_ids = []
            
            for med in all_medicines:
                for detected in detected_medicines:
                    if detected.lower() in med.name.lower():
                        matched_ids.append(med.id)
                        break
            
            return render(request, 'pharmacy/prescription_result.html', {
                'detected_names': detected_medicines,
                'all_medicines': all_medicines,
                'matched_ids': matched_ids
            })
    else:
        form = PrescriptionForm()
    return render(request, 'pharmacy/upload_prescription.html', {'form': form})