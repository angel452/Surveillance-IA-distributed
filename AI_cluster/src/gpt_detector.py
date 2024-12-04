import base64
from openai import OpenAI
from dotenv import load_dotenv
import os


# Cargar la API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("La API Key de OpenAI no está definida. Verifica el archivo .env.")

client = OpenAI(api_key=api_key)

def extract_content_including_curly_braces(text):

    start = text.find("{")
    if start != -1:
        end = text.rfind("}")
        if end != -1:
            # Extraer y devolver todo desde el primer { hasta el último }
            return text[start:end + 1]
    return text  # Devuelve el texto original si no se encuentran llaves


# Función para codificar una imagen en base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Función para realizar la detección del escenario
def detect_scene(image_path):
    base64_image = encode_image(image_path)
    prompt = '''Analyze the provided image and generate a structured JSON output describing the scene. Ensure the "scene" object includes:

    - environment_type: A single-word description of the environment type (e.g., parking_lot, street, park, beach, plaza, etc.).
    - description: A natural language description of the scene where objects are locate d.
    - features: A set of scene features:
        - weather: Weather condition (single-word:sunny, rainy, cloudy, etc.).
        - time_of_day: Time of day (single-word: day, night, sunset, etc.).
        - terrain: Terrain type (single-word: paved, grass, water, etc.).
        - crowd_level: Crowd level (single-word: high, medium, low).
        - lighting: Lighting type (single-word:natural, artificial).

    The response should focus only on the scene description and avoid object-specific details. Provide the result in English.
    in Json format, only the json, not comments of result
    '''

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
    )
    return extract_content_including_curly_braces(response.choices[0].message.content)

# Función para realizar la detección de objetos
def detect_objects(image_path):
    base64_image = encode_image(image_path)
    prompt = '''Analyze the provided image and generate a structured JSON output describing the detected objects. The JSON output should contain an array called "detections" with individual entries for each object detected. Each entry should follow the structure based on the object type (person, vehicle, or other objects). 

For **person** objects:
- object_name: "person"
- description: A brief description of the person, including gender, age group, posture, etc.
- features:
    - upper_clothing_color: The dominant color of the person's upper clothing.
    - lower_clothing_color: The dominant color of the person's lower clothing.
    - size: Relative size (small, medium, large, based on the person’s height).
    - posture: The person’s posture (e.g., standing, sitting, walking).
    - age_group: Estimated age group (child, teenager, adult, senior).
    - gender: Estimated gender (male, female, unknown).
    - accessories: Any visible accessories in array format (e.g., glasses, hat, backpack).
    - additional_notes: Any other notable features (e.g., carrying an umbrella, holding a bag).

- object_name: "person"
...

For **vehicle** objects:
- object_name: Specific type of vehicle (e.g., "car," "truck,", "bicycle").
- description: A brief description of the vehicle, including type and any distinguishing features or additonal features not view in features.
- features:
    - color1: Primary color of the vehicle (e.g., red, blue, white).
    - color2: Secondary color of the vehicle, if applicable.
    - size: Relative size of the vehicle (small, medium, large, based on its overall dimensions).
    - orientation: Vehicle’s orientation (e.g., frontal, lateral, rear view).
    - type: Type of vehicle: Sedan, SUV, Hatchback, Pickup, Minivan 
- object_name: ...

General Notes:
- Prioritize the peoples and then vehicles in the collage.
- For each object, ensure the "features" field is filled with relevant attributes. If any information cannot be detected, use "unknown" as a placeholder.
- The JSON output should be clear, well-structured, and provide variety in the detected objects.
- Only i give you a persons or vehicles
- If the object type cannot be confidently identified, label it as "unknown" and include a brief description with the features.

Ensure that the result is in English and maintains clarity and specificity in the descriptions.'''

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
    )


    return extract_content_including_curly_braces(response.choices[0].message.content)
