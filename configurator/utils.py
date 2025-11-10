# import base64
# from django.core.files.base import ContentFile
# from openai import OpenAI
# from django.conf import settings

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# def generate_uniform_preview(design):
#     """
#     Generate a realistic AI image of the uniform based on the user's selections.
#     """
#     product_name = design.product.name
#     color = design.color.name
#     fabric = design.fabric.name
#     notes = design.notes or ""
#     logo_desc = "with the company's logo on the left chest" if design.logo else "without logo"

#     prompt = (
#         f"A professional studio photo of a {fabric.lower()} {color.lower()} {product_name.lower()} uniform "
#         f"{logo_desc}. The design should look realistic, neatly folded or displayed on a mannequin. {notes}"
#     )

#     # Generate image
#     result = client.images.generate(
#         model="gpt-image-1",
#         prompt=prompt,
#         size="1024x1024"
#     )

#     # Convert base64 -> Django file
#     image_base64 = result.data[0].b64_json
#     image_data = ContentFile(base64.b64decode(image_base64), name=f"ai_preview_{design.id}.png")

#     # Save it to the model
#     design.ai_preview.save(image_data.name, image_data)
#     design.save()

#     return design.ai_preview.url

# ----------------------------------------Hunging Face Version----------------------------------------

# import base64
# import requests
# from django.core.files.base import ContentFile
# from django.conf import settings

# def generate_uniform_preview(design):
#     """
#     Generate a realistic AI image using Hugging Face (Stable Diffusion XL).
#     """
#     api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

#     headers = {
#         "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
#     }

#     product_name = design.product.name
#     color = design.color.name
#     fabric = design.fabric.name
#     notes = design.notes or ""
#     logo_desc = "with a small logo on the left chest" if design.logo else "without logo"

#     prompt = (
#         f"A professional product photo of a {fabric.lower()} {color.lower()} {product_name.lower()} uniform "
#         f"{logo_desc}. The uniform should be realistic, photographed on a mannequin or neatly folded. {notes}"
#     )

#     data = {"inputs": prompt}

#     response = requests.post(api_url, headers=headers, json=data)
    
#     if response.status_code != 200:
#         raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

#     # Response is raw image bytes
#     image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")

#     design.ai_preview.save(image_data.name, image_data)
#     design.save()

# configurator/utils.py
import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from rembg import remove
from PIL import Image
import io


# def generate_uniform_preview(design):
#     """
#     Generate a professional AI preview of a uniform using Hugging Face image-to-image API.
#     The logo is integrated onto the uniform's chest area realistically.
#     """
#     # ✅ Image-to-Image model that supports API calls
#     api_url = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
#     headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}

#     if not design.logo:
#         raise Exception("No logo found in design.")

#     product_name = design.product.name
#     color = design.color.name
#     fabric = design.fabric.name
#     notes = design.notes or ""

#     prompt = f"""
#     A professional photo of a {color.lower()} {product_name.lower()} uniform made of {fabric.lower()} fabric.
#     Place the provided logo image naturally on the LEFT CHEST area of the uniform.
#     The logo should appear printed or embroidered, aligned properly, and integrated into the fabric.
#     Show realistic lighting, shadows, and textile texture. Clean studio background.
#     {notes}
#     """

#     # Read logo image
#     with open(design.logo.path, "rb") as f:
#         image_bytes = f.read()

#     payload = {
#         "inputs": prompt.strip(),
#     }
#     files = {"image": image_bytes}

#     response = requests.post(api_url, headers=headers, data=payload, files=files)

#     if response.status_code != 200:
#         raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

#     image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")

#     # Save it in your model (make sure this field exists)
#     design.ai_preview.save(image_data.name, image_data)
#     design.save()

#     return design.ai_preview.url
from googletrans import Translator
def translate_arabic_to_english(text):
    translator = Translator()
    result = translator.translate(text, src='ar', dest='en')
    return result.text

def generate_uniform_preview(design):
    """
    Generate a front-facing AI uniform photo using Hugging Face API.
    Now uses HEX color codes directly.
    """
    api_url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}

    import webcolors
    from math import sqrt
    

    def closest_css3_color(requested_rgb):
        """
        يحسب أقرب اسم لون من ألوان CSS3 الرسمية لأي كود RGB.
        لا يعتمد على ثوابت داخلية تم حذفها من الإصدارات الحديثة.
        """
        css3_colors = {
            name: webcolors.hex_to_rgb(hex_value)
            for name, hex_value in webcolors._definitions._CSS3_NAMES_TO_HEX.items()
        }
        # ^ نستخدم internal dict الموجود فعليًا في النسخ الجديدة (مؤكد موجود)

        min_distance = float("inf")
        closest_name = None
        for name, rgb in css3_colors.items():
            distance = sqrt(
                (rgb.red - requested_rgb[0]) ** 2 +
                (rgb.green - requested_rgb[1]) ** 2 +
                (rgb.blue - requested_rgb[2]) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        return closest_name


    def hex_to_name_safe(hex_color: str):
        """
        يحوّل الكود الهيكس إلى أقرب اسم لوني معروف.
        """
        try:
            return webcolors.hex_to_name(hex_color)
        except ValueError:
            rgb = webcolors.hex_to_rgb(hex_color)
            closest_name = closest_css3_color(rgb)
            return closest_name.replace("_", " ")

    
    # 🪡 الأقمشة
    FABRIC_TRANSLATIONS = {
        "قطن خفيف": "cotton",
        "بوليستر": "polyester",
        "كتان طبيعي": "linen",
        "صوف ناعم": "wool",
        "نايلون": "nylon",
        "حرير": "silk",
        "قماش طبي": "medical fabric",
        "مزيج قطني": "cotton blend",
        "بوليستر مقاوم للماء": "water-resistant fabric",
        "قماش صناعي": "synthetic fabric",
    }

    # 🧥 المنتجات
    PRODUCT_TRANSLATIONS = {
        "قميص رسمي": "formal shirt",
        "بنطال رسمي": "formal trousers",
        "جاكيت رسمي": "formal jacket",
        "مئزر طبي": "medical coat",
        "زي ممرضة": "nurse uniform",
        "بلوزة طبية": "medical blouse",
        "قميص مدرسي": "school shirt",
        "تيشيرت رياضي": "sports t-shirt",
        "بنطال رياضي": "sports pants",
        "زي عمل صناعي": "industrial workwear",
        "زي استقبال": "receipt uniform",
    }

    product_name = PRODUCT_TRANSLATIONS.get(design.product.name, design.product.name)
    color_name = hex_to_name_safe(design.color)
    fabric = FABRIC_TRANSLATIONS.get(design.fabric.name, design.fabric.name)
    notes = design.notes or ""
    print(design.color, color_name)
    prompt = f"""
A high-resolution studio photo of a {product_name} uniform made of {fabric} fabric, in {color_name} color.
The uniform is short-sleeved and button-up, designed in a professional style similar to a security or work shirt. 
It is worn in a standing position, shown from the waist up, with the torso facing directly forward (camera angle 0° front view).
The shoulders are level and symmetrical, arms relaxed down on both sides but cropped slightly above the wrists, 
so the focus remains on the upper uniform. 
The shirt is neatly tucked into matching uniform trousers with a visible belt line, 
and the overall look should match the proportions and layout of a typical product photo 
where the subject is centered and occupies about 80% of the frame.

The frame size must be fixed (1024×1024 px) — same camera distance, same scale, same position for every generation.
Lighting is soft, even, and professional studio quality — no harsh shadows or reflections.
Background is transparent (alpha channel), pure isolation of the uniform with no backdrop.

Visible fabric details: texture of {fabric}, stitching lines, seams, and natural folds in realistic proportions.
The only variable visual attributes are {color_name} color and {fabric} fabric, while the composition, pose, and framing remain absolutely fixed.
This setup ensures the product can align perfectly for overlaying a logo on the left chest area using CSS.\n
"""

    if notes != "":
        prompt += f"Additional notes: {translate_arabic_to_english(notes)}\n"

    prompt += """
        Negative prompt:
        no people, no faces, no watermark, no text, no logos, no accessories, 
        no background, no shadows, no reflections, no mannequins, no perspective tilt, 
        no zoom changes, no partial crops, no patterns, no multiple views.
        """



    data = {
        "inputs": prompt.strip(),
        "parameters": {"width": 1024, "height": 1024}
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

    # حفظ الصورة المُنشأة
    image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")
    design.ai_preview.save(image_data.name, image_data)
    design.save()

    return design.ai_preview.url

def remove_logo_background(design):
    """
    Remove background from uploaded logo using rembg.
    """
    if not design.logo:
        return

    input_path = design.logo.path
    output_path = os.path.splitext(input_path)[0] + "_nobg.png"

    with open(input_path, "rb") as i:
        input_bytes = i.read()

    # remove() returns PNG bytes with transparent background
    result = remove(input_bytes)

    # Replace logo file with the transparent one
    design.logo.save(os.path.basename(output_path), ContentFile(result))
    design.save()



# # import base64
# # from django.core.files.base import ContentFile
# # from openai import OpenAI
# # from django.conf import settings

# # client = OpenAI(api_key=settings.OPENAI_API_KEY)

# # def generate_uniform_preview(design):
# #     """
# #     Generate a realistic AI image of the uniform based on the user's selections.
# #     """
# #     product_name = design.product.name
# #     color = design.color.name
# #     fabric = design.fabric.name
# #     notes = design.notes or ""
# #     logo_desc = "with the company's logo on the left chest" if design.logo else "without logo"

# #     prompt = (
# #         f"A professional studio photo of a {fabric.lower()} {color.lower()} {product_name.lower()} uniform "
# #         f"{logo_desc}. The design should look realistic, neatly folded or displayed on a mannequin. {notes}"
# #     )

# #     # Generate image
# #     result = client.images.generate(
# #         model="gpt-image-1",
# #         prompt=prompt,
# #         size="1024x1024"
# #     )

# #     # Convert base64 -> Django file
# #     image_base64 = result.data[0].b64_json
# #     image_data = ContentFile(base64.b64decode(image_base64), name=f"ai_preview_{design.id}.png")

# #     # Save it to the model
# #     design.ai_preview.save(image_data.name, image_data)
# #     design.save()

# #     return design.ai_preview.url

# # ----------------------------------------Hunging Face Version----------------------------------------

# # import base64
# # import requests
# # from django.core.files.base import ContentFile
# # from django.conf import settings

# # def generate_uniform_preview(design):
# #     """
# #     Generate a realistic AI image using Hugging Face (Stable Diffusion XL).
# #     """
# #     api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# #     headers = {
# #         "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
# #     }

# #     product_name = design.product.name
# #     color = design.color.name
# #     fabric = design.fabric.name
# #     notes = design.notes or ""
# #     logo_desc = "with a small logo on the left chest" if design.logo else "without logo"

# #     prompt = (
# #         f"A professional product photo of a {fabric.lower()} {color.lower()} {product_name.lower()} uniform "
# #         f"{logo_desc}. The uniform should be realistic, photographed on a mannequin or neatly folded. {notes}"
# #     )

# #     data = {"inputs": prompt}

# #     response = requests.post(api_url, headers=headers, json=data)
    
# #     if response.status_code != 200:
# #         raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

# #     # Response is raw image bytes
# #     image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")

# #     design.ai_preview.save(image_data.name, image_data)
# #     design.save()

# # configurator/utils.py
# import os
# import requests
# from django.core.files.base import ContentFile
# from django.conf import settings
# from rembg import remove
# from PIL import Image
# import io


# # def generate_uniform_preview(design):
# #     """
# #     Generate a professional AI preview of a uniform using Hugging Face image-to-image API.
# #     The logo is integrated onto the uniform's chest area realistically.
# #     """
# #     # ✅ Image-to-Image model that supports API calls
# #     api_url = "https://api-inference.huggingface.co/models/timbrooks/instruct-pix2pix"
# #     headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}

# #     if not design.logo:
# #         raise Exception("No logo found in design.")

# #     product_name = design.product.name
# #     color = design.color.name
# #     fabric = design.fabric.name
# #     notes = design.notes or ""

# #     prompt = f"""
# #     A professional photo of a {color.lower()} {product_name.lower()} uniform made of {fabric.lower()} fabric.
# #     Place the provided logo image naturally on the LEFT CHEST area of the uniform.
# #     The logo should appear printed or embroidered, aligned properly, and integrated into the fabric.
# #     Show realistic lighting, shadows, and textile texture. Clean studio background.
# #     {notes}
# #     """

# #     # Read logo image
# #     with open(design.logo.path, "rb") as f:
# #         image_bytes = f.read()

# #     payload = {
# #         "inputs": prompt.strip(),
# #     }
# #     files = {"image": image_bytes}

# #     response = requests.post(api_url, headers=headers, data=payload, files=files)

# #     if response.status_code != 200:
# #         raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

# #     image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")

# #     # Save it in your model (make sure this field exists)
# #     design.ai_preview.save(image_data.name, image_data)
# #     design.save()

# #     return design.ai_preview.url


# def generate_uniform_preview(design):
#     """
#     Generate a front-facing AI uniform photo using Hugging Face API.
#     Now uses HEX color codes directly.
#     """
#     api_url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
#     headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}

#     import webcolors
#     from math import sqrt

#     def closest_css3_color(requested_rgb):
#         """
#         يحسب أقرب اسم لون من ألوان CSS3 الرسمية لأي كود RGB.
#         لا يعتمد على ثوابت داخلية تم حذفها من الإصدارات الحديثة.
#         """
#         css3_colors = {
#             name: webcolors.hex_to_rgb(hex_value)
#             for name, hex_value in webcolors._definitions._CSS3_NAMES_TO_HEX.items()
#         }
#         # ^ نستخدم internal dict الموجود فعليًا في النسخ الجديدة (مؤكد موجود)

#         min_distance = float("inf")
#         closest_name = None
#         for name, rgb in css3_colors.items():
#             distance = sqrt(
#                 (rgb.red - requested_rgb[0]) ** 2 +
#                 (rgb.green - requested_rgb[1]) ** 2 +
#                 (rgb.blue - requested_rgb[2]) ** 2
#             )
#             if distance < min_distance:
#                 min_distance = distance
#                 closest_name = name
#         return closest_name


#     def hex_to_name_safe(hex_color: str):
#         """
#         يحوّل الكود الهيكس إلى أقرب اسم لوني معروف.
#         """
#         try:
#             return webcolors.hex_to_name(hex_color)
#         except ValueError:
#             rgb = webcolors.hex_to_rgb(hex_color)
#             closest_name = closest_css3_color(rgb)
#             return closest_name.replace("_", " ")

    
#     # 🪡 الأقمشة
#     FABRIC_TRANSLATIONS = {
#         "قطن خفيف": "cotton",
#         "بوليستر": "polyester",
#         "كتان طبيعي": "linen",
#         "صوف ناعم": "wool",
#         "نايلون": "nylon",
#         "حرير": "silk",
#         "قماش طبي": "medical fabric",
#         "مزيج قطني": "cotton blend",
#         "بوليستر مقاوم للماء": "water-resistant fabric",
#         "قماش صناعي": "synthetic fabric",
#     }

#     # 🧥 المنتجات
#     PRODUCT_TRANSLATIONS = {
#         "قميص رسمي": "formal shirt",
#         "بنطال رسمي": "formal trousers",
#         "جاكيت رسمي": "formal jacket",
#         "مئزر طبي": "medical coat",
#         "زي ممرضة": "nurse uniform",
#         "بلوزة طبية": "medical blouse",
#         "قميص مدرسي": "school shirt",
#         "تيشيرت رياضي": "sports t-shirt",
#         "بنطال رياضي": "sports pants",
#         "زي عمل صناعي": "industrial workwear",
#         "زي استقبال": "receipt uniform",
#     }

#     product_name = PRODUCT_TRANSLATIONS.get(design.product.name, design.product.name)
#     color_name = hex_to_name_safe(design.color)
#     fabric = FABRIC_TRANSLATIONS.get(design.fabric.name, design.fabric.name)
#     notes = design.notes or ""
#     print(design.color, color_name)
#     prompt = f"""
# A high-resolution studio photo of a {product_name} uniform made of {fabric} fabric, in {color_name} color.
# The uniform is short-sleeved and button-up, designed in a professional style similar to a security or work shirt. 
# It is worn in a standing position, shown from the waist up, with the torso facing directly forward (camera angle 0° front view).
# The shoulders are level and symmetrical, arms relaxed down on both sides but cropped slightly above the wrists, 
# so the focus remains on the upper uniform. 
# The shirt is neatly tucked into matching uniform trousers with a visible belt line, 
# and the overall look should match the proportions and layout of a typical product photo 
# where the subject is centered and occupies about 80% of the frame.

# The frame size must be fixed (1024×1024 px) — same camera distance, same scale, same position for every generation.
# Lighting is soft, even, and professional studio quality — no harsh shadows or reflections.
# Background is transparent (alpha channel), pure isolation of the uniform with no backdrop.

# Visible fabric details: texture of {fabric}, stitching lines, seams, and natural folds in realistic proportions.
# The only variable visual attributes are {color_name} color and {fabric} fabric, while the composition, pose, and framing remain absolutely fixed.
# This setup ensures the product can align perfectly for overlaying a logo on the left chest area using CSS.

# Negative prompt:
# no people, no faces, no watermark, no text, no logos, no accessories, 
# no background, no shadows, no reflections, no mannequins, no perspective tilt, 
# no zoom changes, no partial crops, no patterns, no multiple views.
# """

#     data = {
#         "inputs": prompt.strip(),
#         "parameters": {"width": 1024, "height": 1024}
#     }

#     response = requests.post(api_url, headers=headers, json=data)
#     if response.status_code != 200:
#         raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

#     # حفظ الصورة المُنشأة
#     image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")
#     design.ai_preview.save(image_data.name, image_data)
#     design.save()

#     return design.ai_preview.url

# def remove_logo_background(design):
#     """
#     Remove background from uploaded logo using rembg.
#     """
#     if not design.logo:
#         return

#     input_path = design.logo.path
#     output_path = os.path.splitext(input_path)[0] + "_nobg.png"

#     with open(input_path, "rb") as i:
#         input_bytes = i.read()

#     # remove() returns PNG bytes with transparent background
#     result = remove(input_bytes)

#     # Replace logo file with the transparent one
#     design.logo.save(os.path.basename(output_path), ContentFile(result))
#     design.save()

import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from rembg import remove
from PIL import Image
import io
import cv2
import numpy as np
from io import BytesIO
import webcolors
from math import sqrt


def generate_uniform_preview(design, include_logo_area=False):
    """
    Generate a front-facing AI uniform photo using Hugging Face API.
    """
    api_url = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}

    def closest_css3_color(requested_rgb):
        """
        يحسب أقرب اسم لون من ألوان CSS3 الرسمية لأي كود RGB.
        """
        css3_colors = {
            name: webcolors.hex_to_rgb(hex_value)
            for name, hex_value in webcolors._definitions._CSS3_NAMES_TO_HEX.items()
        }

        min_distance = float("inf")
        closest_name = None
        for name, rgb in css3_colors.items():
            distance = sqrt(
                (rgb.red - requested_rgb[0]) ** 2 +
                (rgb.green - requested_rgb[1]) ** 2 +
                (rgb.blue - requested_rgb[2]) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        return closest_name

    def hex_to_name_safe(hex_color: str):
        """
        يحوّل الكود الهيكس إلى أقرب اسم لوني معروف.
        """
        try:
            return webcolors.hex_to_name(hex_color)
        except ValueError:
            rgb = webcolors.hex_to_rgb(hex_color)
            closest_name = closest_css3_color(rgb)
            return closest_name.replace("_", " ")

    # 🪡 الأقمشة
    FABRIC_TRANSLATIONS = {
        "قطن خفيف": "cotton",
        "بوليستر": "polyester",
        "كتان طبيعي": "linen",
        "صوف ناعم": "wool",
        "نايلون": "nylon",
        "حرير": "silk",
        "قماش طبي": "medical fabric",
        "مزيج قطني": "cotton blend",
        "بوليستر مقاوم للماء": "water-resistant fabric",
        "قماش صناعي": "synthetic fabric",
    }

    # 🧥 المنتجات
    PRODUCT_TRANSLATIONS = {
        "قميص رسمي": "formal shirt",
        "بنطال رسمي": "formal trousers",
        "جاكيت رسمي": "formal jacket",
        "مئزر طبي": "medical coat",
        "زي ممرضة": "nurse uniform",
        "بلوزة طبية": "medical blouse",
        "قميص مدرسي": "school shirt",
        "تيشيرت رياضي": "sports t-shirt",
        "بنطال رياضي": "sports pants",
        "زي عمل صناعي": "industrial workwear",
        "زي استقبال": "receipt uniform",
    }

    product_name = PRODUCT_TRANSLATIONS.get(design.product.name, design.product.name)
    color_name = hex_to_name_safe(design.color)
    fabric = FABRIC_TRANSLATIONS.get(design.fabric.name, design.fabric.name)
    
    prompt = f"""
A high-resolution studio photo of a {product_name} uniform made of {fabric} fabric, in {color_name} color.
The uniform is short-sleeved and button-up, designed in a professional style similar to a security or work shirt. 
It is worn in a standing position, shown from the waist up, with the torso facing directly forward (camera angle 0° front view).
The shoulders are level and symmetrical, arms relaxed down on both sides but cropped slightly above the wrists, 
so the focus remains on the upper uniform. 
The shirt is neatly tucked into matching uniform trousers with a visible belt line, 
and the overall look should match the proportions and layout of a typical product photo 
where the subject is centered and occupies about 80% of the frame.

The frame size must be fixed (1024×1024 px) — same camera distance, same scale, same position for every generation.
Lighting is soft, even, and professional studio quality — no harsh shadows or reflections.
Background is transparent (alpha channel), pure isolation of the uniform with no backdrop.

Visible fabric details: texture of {fabric}, stitching lines, seams, and natural folds in realistic proportions.
The only variable visual attributes are {color_name} color and {fabric} fabric, while the composition, pose, and framing remain absolutely fixed.
{"Left chest area is clean and ready for logo placement." if include_logo_area else ""}

Negative prompt:
no people, no faces, no watermark, no text, no logos, no accessories, 
no background, no shadows, no reflections, no mannequins, no perspective tilt, 
no zoom changes, no partial crops, no patterns, no multiple views.
"""

    data = {
        "inputs": prompt.strip(),
        "parameters": {"width": 1024, "height": 1024}
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")

    # حفظ الصورة المُنشأة
    image_data = ContentFile(response.content, name=f"ai_preview_{design.id}.png")
    design.ai_preview.save(image_data.name, image_data)
    design.save()

    return design.ai_preview.url


def remove_logo_background(design):
    """
    Remove background from uploaded logo using rembg.
    """
    if not design.logo:
        return None

    try:
        # قراءة صورة الشعار
        if hasattr(design.logo, 'path'):
            input_path = design.logo.path
            with open(input_path, "rb") as i:
                input_bytes = i.read()
        else:
            # إذا كان ملف مرفوع في الذاكرة
            input_bytes = design.logo.read()

        # إزالة الخلفية
        result = remove(input_bytes)

        # حفظ الصورة الناتجة
        output_filename = f"logo_nobg_{design.id}.png"
        design.logo_nobg.save(output_filename, ContentFile(result))
        design.save()
        
        return design.logo_nobg.path
        
    except Exception as e:
        print(f"Error removing logo background: {e}")
        return None


# def generate_uniform_and_add_logo(design):
#     """
#     حل مجاني بالكامل: توليد يونيفورم ثم إضافة الشعار باستخدام معالجة الصور
#     """
#     try:
#         # 1. أولاً: توليد صورة اليونيفورم بدون شعار مع منطقة جاهزة للشعار
#         uniform_image_url = generate_uniform_preview(design, include_logo_area=True)
        
#         # 2. إذا كان هناك شعار، قم بإضافته
#         if design.logo:
#             # 3. إزالة خلفية الشعار أولاً إذا لم تكن مُزالة
#             logo_path = remove_logo_background(design)
#             if logo_path:
#                 # 4. معالجة الصورة وإضافة الشعار
#                 result_content = add_logo_to_uniform(uniform_image_url, logo_path)
                
#                 # 5. حفظ الصورة النهائية
#                 if result_content:
#                     design.final_preview.save(f"uniform_with_logo_{design.id}.png", result_content)
#                     design.save()
#                     return design.final_preview.url
        
#         return uniform_image_url
        
#     except Exception as e:
#         print(f"Error in generate_uniform_and_add_logo: {e}")
#         # في حالة الخطأ، أرجع الصورة الأصلية بدون شعار
#         return uniform_image_url if 'uniform_image_url' in locals() else None


# def add_logo_to_uniform(uniform_image_url, logo_image_path):
#     """
#     إضافة الشعار إلى اليونيفورم باستخدام OpenCV
#     """
#     try:
#         # تحميل صورة اليونيفورم
#         uniform_response = requests.get(uniform_image_url)
#         if uniform_response.status_code != 200:
#             raise Exception(f"Failed to download uniform image: {uniform_response.status_code}")
            
#         uniform_img = Image.open(BytesIO(uniform_response.content))
        
#         # تحويل إلى RGB إذا كان PNG بشفافية
#         if uniform_img.mode in ('RGBA', 'LA'):
#             background = Image.new('RGB', uniform_img.size, (255, 255, 255))
#             background.paste(uniform_img, mask=uniform_img.split()[-1])
#             uniform_img = background
            
#         uniform_cv = cv2.cvtColor(np.array(uniform_img), cv2.COLOR_RGB2BGR)
        
#         # تحميل الشعار مع الشفافية
#         logo_img = cv2.imread(logo_image_path, cv2.IMREAD_UNCHANGED)
#         if logo_img is None:
#             raise Exception("Failed to load logo image")
        
#         # تحديد موقع الشعار (منطقة الصدر اليسرى)
#         chest_x = int(uniform_cv.shape[1] * 0.25)  # 25% من العرض
#         chest_y = int(uniform_cv.shape[0] * 0.35)   # 35% من الارتفاع (أعلى قليلاً)
        
#         # resize الشعار
#         logo_height = int(uniform_cv.shape[0] * 0.12)  # 12% من ارتفاع الصورة
#         if logo_img.shape[0] > 0:
#             aspect_ratio = logo_img.shape[1] / logo_img.shape[0]
#             logo_width = int(logo_height * aspect_ratio)
            
#             # التأكد من أن الأبعاد موجبة
#             logo_width = max(logo_width, 1)
#             logo_height = max(logo_height, 1)
            
#             logo_resized = cv2.resize(logo_img, (logo_width, logo_height))
            
#             # دمج الشعار مع اليونيفورم
#             result = blend_images(uniform_cv, logo_resized, chest_x, chest_y)
            
#             # حفظ الصورة الناتجة
#             result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
#             result_image = Image.fromarray(result_rgb)
            
#             buffer = BytesIO()
#             result_image.save(buffer, format='PNG')
#             buffer.seek(0)
            
#             return ContentFile(buffer.getvalue(), name=f"uniform_with_logo_temp.png")
        
#     except Exception as e:
#         print(f"Error in add_logo_to_uniform: {e}")
#         return None


# def blend_images(background, overlay, x, y):
#     """
#     دمج صورتين مع الشفافية
#     """
#     try:
#         h, w = overlay.shape[:2]
        
#         # التأكد من أن الإحداثيات ضمن حدود الصورة
#         if y + h > background.shape[0] or x + w > background.shape[1]:
#             # ضبط الإحداثيات إذا كانت خارج الحدود
#             y = min(y, background.shape[0] - h)
#             x = min(x, background.shape[1] - w)
#             y = max(y, 0)
#             x = max(x, 0)
        
#         # إذا كان الشعار به قناة ألفا (شفافية)
#         if overlay.shape[2] == 4:
#             # فصل القنانات
#             overlay_rgb = overlay[:,:,:3]
#             overlay_alpha = overlay[:,:,3:4] / 255.0  # جعلها 3D
            
#             # استخراج المنطقة من الخلفية
#             background_region = background[y:y+h, x:x+w]
            
#             # الدمج مع الشفافية
#             blended = background_region * (1 - overlay_alpha) + overlay_rgb * overlay_alpha
#             background[y:y+h, x:x+w] = blended.astype(np.uint8)
#         else:
#             # بدون شفافية - نستخدم طريقة بسيطة
#             background[y:y+h, x:x+w] = overlay
            
#         return background
        
#     except Exception as e:
#         print(f"Error in blend_images: {e}")
#         return background


# # دالة مساعدة للاستخدام السريع
# def generate_final_design(design):
#     """
#     دالة رئيسية لإنشاء التصميم النهائي مع أو بدون شعار
#     """
#     return generate_uniform_and_add_logo(design)
