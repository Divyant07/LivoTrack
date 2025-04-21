import pytesseract
import re

def extract_values_from_image(img):
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    sgpt_val, sgot_val = None, None

    for i, word in enumerate(data['text']):
        word_clean = word.strip().upper()
        if word_clean in ['SGPT', 'ALT']:
            sgpt_val = extract_numeric_nearby(data, i)
        elif word_clean in ['SGOT', 'AST']:
            sgot_val = extract_numeric_nearby(data, i)

    return sgpt_val, sgot_val 

def extract_numeric_nearby(data, index):
    for j in range(index + 1, min(index + 6, len(data['text']))):
        try:
            value = float(re.sub(r'[^\d.]', '', data['text'][j]))
            return int(value)
        except:
            continue
    return None

def analyze_liver_stage(sgpt, sgot):
    if sgpt is not None and sgot is not None:
        if sgpt < 40 and sgot < 40:
            return "Stage 0"
        elif sgpt < 80 or sgot < 80:
            return "Stage 1"
        elif sgpt < 150 or sgot < 150:
            return "Stage 2"
        else:
            return "Stage 3"
    return "Insufficient Data to Determine Stage"
