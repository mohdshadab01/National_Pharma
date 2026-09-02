from django.shortcuts import render, redirect
import requests
import google.generativeai as genai

def home(request):
    quotes = [
        {"quote": "Wherever the art of Medicine is loved, there is also a love of Humanity.", "author": "Hippocrates"},
        {"quote": "Medicines cure diseases, but only doctors can cure patients.", "author": "Carl Jung"},
        {"quote": "The science of operations is a science itself in microbiology & pharma.", "author": "Ada Lovelace"}
    ]
    blogs = [
        {"title": "Advancements in Microbial Biochemistry 2026", "category": "Microbiology Research", "summary": "Discover how microbial strains are revolutionary in developing targeted pharma capsules."},
        {"title": "Role of AI in Modern Prescription Reading", "category": "AI Healthcare", "summary": "How vision transformers and Gemini LLM reduce medication errors in digital pharmacies."},
        {"title": "Understanding Pharmacology & Receptors", "category": "Medicine Research", "summary": "A deep dive into how active pharmaceutical ingredients interact at cellular sites."}
    ]
    return render(request, 'pharmacy/home.html', {'quotes': quotes, 'blogs': blogs})

def medicine_search(request):
    query = request.GET.get('q', '')
    med_info = None
    if query:
        try:
            url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{query}&limit=1"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()['results'][0]
                med_info = {
                    'name': query.capitalize(),
                    'uses': data.get('indications_and_usage', ['Details available upon consult'])[0],
                    'side_effects': data.get('adverse_reactions', ['Mild reactions may occur'])[0],
                    'price': 180.00
                }
            else:
                med_info = {'name': query.capitalize(), 'uses': 'General Therapeutic Compound', 'side_effects': 'Consult Doctor', 'price': 150.00}
        except Exception:
            med_info = {'name': query.capitalize(), 'uses': 'General Therapeutic Compound', 'side_effects': 'Consult Doctor', 'price': 120.00}

    return render(request, 'pharmacy/medicine_search.html', {'med_info': med_info, 'query': query})

def upload_prescription(request):
    if request.method == 'POST' and request.FILES.get('prescription'):
        cart = request.session.get('cart', {})
        extracted_meds = ["Amoxicillin 500mg", "Paracetamol 650mg", "Cetirizine 10mg"]
        for med in extracted_meds:
            cart[med] = {'price': 140.00, 'qty': 1}
        request.session['cart'] = cart
        return redirect('cart')
    return render(request, 'pharmacy/upload_prescription.html')

def cart(request):
    cart_items = request.session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart_items.values())
    return render(request, 'pharmacy/cart.html', {'cart_items': cart_items, 'total': total})

def microbiology(request):
    return render(request, 'pharmacy/microbiology.html')

def contact(request):
    return render(request, 'pharmacy/contact.html')