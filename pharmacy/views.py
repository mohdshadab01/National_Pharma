import json
import urllib.parse
import requests
from PIL import Image
import google.generativeai as genai

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- GEMINI API CONFIGURATION ---
# अपनी असली Gemini API Key यहाँ डालें (https://aistudio.google.com/ से प्राप्त करें)
GEMINI_API_KEY = "AQ.Ab8RN6J34ThfZhMBRDqD4lBkbgWL9Wz_OLmhzY643zNfkINq-g"
genai.configure(api_key=GEMINI_API_KEY)


# 1. Home Route
def home(request):
    return render(request, 'pharmacy/home.html')


# 2. Real-Time OpenFDA & Medicine Search (Error Fixed)
def medicine_search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        encoded_query = urllib.parse.quote(query)
        fda_url = f'https://api.fda.gov/drug/label.json?search=openfda.generic_name:"{encoded_query}"+openfda.brand_name:"{encoded_query}"&limit=1'
        
        medicine_info = {
            "name": query.capitalize(),
            "uses": "Consult physician for detailed therapeutic dosage.",
            "side_effects": "Consult Doctor for full adverse profile.",
            "active_ingredient": "Information N/A",
            "image": f"https://source.unsplash.com/400x300/?medicine,{encoded_query}"
        }

        try:
            fda_res = requests.get(fda_url, timeout=5)
            if fda_res.status_code == 200:
                data = fda_res.json().get('results', [])[0]
                uses = data.get('purpose', data.get('indications_and_usage', ['General Therapeutic Compound']))[0]
                side_effects = data.get('adverse_reactions', ['Consult Doctor'])[0]
                active_ing = data.get('active_ingredient', ['N/A'])[0]

                medicine_info["uses"] = uses[:180] + "..." if len(uses) > 180 else uses
                medicine_info["side_effects"] = side_effects[:150] + "..." if len(side_effects) > 150 else side_effects
                medicine_info["active_ingredient"] = active_ing[:100]
        except Exception:
            pass

        results.append(medicine_info)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'results': results})

    return render(request, 'pharmacy/medicine_search.html', {'results': results, 'query': query})


# 3. Real AI Gemini Vision Prescription Scanner (All 6 Errors Fixed)
@csrf_exempt
def scan_prescription(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid Request Method'}, status=405)

    if 'prescription' not in request.FILES:
        return JsonResponse({'status': 'error', 'message': 'No prescription image uploaded'}, status=400)

    try:
        # Uploaded image load karein
        file = request.FILES['prescription']
        img = Image.open(file)

        # Gemini 1.5 Flash Vision Model Init
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Precise Extraction Prompt
        prompt = """
        You are an expert pharmacist and medical OCR specialist.
        Carefully analyze this doctor's handwritten or printed prescription.
        
        Extract all medicines prescribed and output STRICTLY a valid raw JSON array of objects.
        Each object MUST have the following key-value pairs:
        - "medicine_name": Exact Brand Name or Active Chemical Name written.
        - "dosage": Strength (e.g., 500mg, 40mg, 625mg).
        - "frequency": Timing code (e.g., 1-0-1, 1-0-0, 0-0-1, BD, TDS, HS).
        - "duration": Duration (e.g., 5 days, 3 days, 1 week).
        - "instructions": E.g., Before food, After food, Khali pet.

        Do NOT add markdown formatting, backticks (```json), or extra text. Output ONLY pure raw JSON array.
        """

        response = model.generate_content([prompt, img])
        raw_text = response.text.strip()

        # Clean backticks if model returns markdown formatted text
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        parsed_medicines = json.loads(raw_text)

        return JsonResponse({
            'status': 'success',
            'message': 'Prescription scanned successfully with Gemini AI',
            'medicines': parsed_medicines
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'AI Processing Failed: {str(e)}'
        }, status=500)