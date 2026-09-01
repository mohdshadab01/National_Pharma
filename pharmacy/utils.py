import json
from google import genai
from PIL import Image

def parse_prescription_image(image_path, api_key):
    """
    Gemini 2.5 Flash Vision Model ka use karke image se medicines detect karta hai.
    """
    client = genai.Client(api_key=api_key)
    img = Image.open(image_path)
    
    prompt = (
        "Analyze this doctor prescription image. Extract all medicine names mentioned. "
        "Return ONLY a valid JSON array of strings containing medicine names, like: "
        '["Paracetamol", "Amoxicillin"]. Do not include markdown formatting or extra text.'
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, prompt]
        )
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        medicines = json.loads(clean_text)
        return medicines
    except Exception as e:
        print("AI Processing Error:", e)
        return []