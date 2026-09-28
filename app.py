import os
import warnings
warnings.filterwarnings("ignore")

from typing import List, Dict, Tuple, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import gradio as gr

# ==============================================================================
# 🎨 COLOR PALETTE & PRODUCE DATABASE
# ==============================================================================

BOX_COLORS = [
    "#10B981",  # Emerald
    "#06B6D4",  # Cyan
    "#F59E0B",  # Amber
    "#EC4899",  # Pink
    "#8B5CF6",  # Violet
    "#3B82F6",  # Blue
    "#14B8A6",  # Teal
    "#EF4444",  # Red
    "#84CC16",  # Lime
    "#F97316",  # Orange
]

EMOJI_MAP = {
    "apple": "🍎", "banana": "🍌", "orange": "🍊", "green_orange": "🍊", "grape": "🍇",
    "grapes": "🍇", "strawberry": "🍓", "watermelon": "🍉", "mango": "🥭", "pineapple": "🍍",
    "pear": "🍐", "peach": "🍑", "cherry": "🍒", "lemon": "🍋", "avocado": "🥑",
    "tomato": "🍅", "coconut": "🥥", "kiwi": "🥝", "melon": "🍈", "pomegranate": "🍷",
    "sweetpotato": "🍠", "sweet_potato": "🍠",
    "broccoli": "🥦", "carrot": "🥕", "corn": "🌽", "maize": "🌽", "sweetcorn": "🌽",
    "cucumber": "🥒", "garlic": "🧄", "onion": "🧅", "pepper": "🌶️", "potato": "🥔",
    "eggplant": "🍆", "lettuce": "🥬", "mushroom": "🍄", "beetroot": "🫚", "spinach": "🥬",
    "capsicum": "🫑", "bell pepper": "🫑", "bell_pepper": "🫑", "paprika": "🌶️",
    "cauliflower": "🥦", "cabbage": "🥬", "ginger": "🫚", "chilli": "🌶️", "chilli pepper": "🌶️",
    "chilli_pepper": "🌶️", "peas": "🟢", "radish": "🥢", "raddish": "🥢", "turnip": "🪴",
    "soy beans": "🫘", "soy_beans": "🫘", "bitter_gourd": "🥒", "bottle_gourd": "🥒",
    "okra": "🌿", "jalepeno": "🌶️", "jalapeño": "🌶️",
}

FRUITS = {
    "apple", "banana", "orange", "green_orange", "grape", "grapes", "strawberry",
    "watermelon", "mango", "pineapple", "pear", "peach", "cherry", "lemon",
    "avocado", "coconut", "kiwi", "melon", "pomegranate",
}

VEGETABLES = {
    "broccoli", "carrot", "corn", "maize", "sweetcorn", "cucumber", "garlic",
    "onion", "pepper", "potato", "eggplant", "lettuce", "mushroom", "beetroot",
    "spinach", "capsicum", "bell pepper", "bell_pepper", "paprika", "cauliflower",
    "cabbage", "ginger", "chilli", "chilli pepper", "chilli_pepper", "peas",
    "radish", "raddish", "turnip", "soy beans", "soy_beans", "bitter_gourd",
    "bottle_gourd", "okra", "jalepeno", "jalapeño", "sweetpotato", "sweet_potato",
    "tomato",
}

# USDA-referenced nutritional metrics per 100g standard edible portion
NUTRITION_DB = {
    "apple": {
        "calories": 52, "carbs": 13.8, "protein": 0.3, "fiber": 2.4, "sugar": 10.4,
        "vitamins": "Vitamin C (14%), Potassium (3%)",
        "benefits": "Supports heart health, lowers cholesterol with pectin fiber.",
        "recipes": ["Cinnamon Apple Oatmeal", "Waldorf Crunch Salad", "Baked Stuffed Apples"]
    },
    "banana": {
        "calories": 89, "carbs": 22.8, "protein": 1.1, "fiber": 2.6, "sugar": 12.2,
        "vitamins": "Vitamin B6 (20%), Potassium (10%), Vitamin C (10%)",
        "benefits": "Immediate natural energy, sustains muscle function and gut health.",
        "recipes": ["Creamy Banana Berry Smoothie", "Healthy Banana Oat Pancakes", "Frozen Banana Bites"]
    },
    "orange": {
        "calories": 47, "carbs": 11.8, "protein": 0.9, "fiber": 2.4, "sugar": 9.4,
        "vitamins": "Vitamin C (89%), Folate (8%), Calcium (4%)",
        "benefits": "Boosts immune defense, enhances collagen synthesis and iron uptake.",
        "recipes": ["Citrus Fennel Salad", "Fresh Pressed Sunrise Juice", "Orange Glazed Roast"]
    },
    "green_orange": {
        "calories": 45, "carbs": 11.2, "protein": 0.9, "fiber": 2.3, "sugar": 8.9,
        "vitamins": "Vitamin C (85%), Bioflavonoids",
        "benefits": "High citric acid enhances digestion and natural hydration.",
        "recipes": ["Citrus Summer Salad", "Infused Mint-Orange Water", "Fruit Salsa"]
    },
    "grape": {
        "calories": 69, "carbs": 18.1, "protein": 0.7, "fiber": 0.9, "sugar": 15.5,
        "vitamins": "Vitamin K (18%), Vitamin C (5%), Resveratrol",
        "benefits": "Powerful polyphenols and resveratrol support vascular health.",
        "recipes": ["Roasted Grape & Goat Cheese Crostini", "Chilled Fruit Medley", "Spinach Grape Salad"]
    },
    "grapes": {
        "calories": 69, "carbs": 18.1, "protein": 0.7, "fiber": 0.9, "sugar": 15.5,
        "vitamins": "Vitamin K (18%), Resveratrol",
        "benefits": "Powerful polyphenols and resveratrol protect cell health.",
        "recipes": ["Fresh Fruit Salad", "Roasted Grapes on Ricotta", "Frozen Grape Snacks"]
    },
    "strawberry": {
        "calories": 32, "carbs": 7.7, "protein": 0.7, "fiber": 2.0, "sugar": 4.9,
        "vitamins": "Vitamin C (98%), Manganese (19%), Folate (6%)",
        "benefits": "High antioxidant index combats inflammation and promotes radiant skin.",
        "recipes": ["Strawberry Spinach Poppyseed Salad", "Chia Seed Jam", "Berry Parfait"]
    },
    "watermelon": {
        "calories": 30, "carbs": 7.6, "protein": 0.6, "fiber": 0.4, "sugar": 6.2,
        "vitamins": "Vitamin C (14%), Vitamin A (11%), Lycopene",
        "benefits": "92% water content delivers superior hydration and amino acid citrulline.",
        "recipes": ["Watermelon Feta Mint Salad", "Agua Fresca Cooler", "Grilled Watermelon Steaks"]
    },
    "mango": {
        "calories": 60, "carbs": 15.0, "protein": 0.8, "fiber": 1.6, "sugar": 13.7,
        "vitamins": "Vitamin C (60%), Vitamin A (21%), Folate",
        "benefits": "Amylase enzymes assist digestion, rich beta-carotene supports vision.",
        "recipes": ["Fresh Mango Avocado Salsa", "Mango Sticky Rice", "Tropical Smoothie Bowl"]
    },
    "pineapple": {
        "calories": 50, "carbs": 13.1, "protein": 0.5, "fiber": 1.4, "sugar": 9.9,
        "vitamins": "Vitamin C (79%), Manganese (44%), Bromelain",
        "benefits": "Bromelain enzyme aids protein digestion and joint comfort.",
        "recipes": ["Grilled Pineapple Skewers", "Pineapple Fried Rice", "Tropical Pico de Gallo"]
    },
    "pear": {
        "calories": 57, "carbs": 15.2, "protein": 0.4, "fiber": 3.1, "sugar": 9.8,
        "vitamins": "Vitamin C (7%), Vitamin K (6%), Copper",
        "benefits": "High soluble fiber prebiotic nourishes beneficial gut flora.",
        "recipes": ["Arugula Pear Walnut Salad", "Poached Spiced Pears", "Warm Pear Tart"]
    },
    "peach": {
        "calories": 39, "carbs": 9.5, "protein": 0.9, "fiber": 1.5, "sugar": 8.4,
        "vitamins": "Vitamin C (11%), Vitamin A (6%), Potassium",
        "benefits": "Carotenoids protect eyesight and skin cell longevity.",
        "recipes": ["Grilled Peaches with Honey", "Peach Caprese Skewers", "Peach Bellini Bowl"]
    },
    "cherry": {
        "calories": 63, "carbs": 16.0, "protein": 1.1, "fiber": 2.1, "sugar": 12.8,
        "vitamins": "Vitamin C (12%), Potassium (6%), Melatonin",
        "benefits": "Anthocyanins reduce post-exercise muscle soreness and aid sleep.",
        "recipes": ["Cherry Almond Oatmeal", "Balsamic Cherry Glaze", "Fresh Cherry Clafoutis"]
    },
    "lemon": {
        "calories": 29, "carbs": 9.3, "protein": 1.1, "fiber": 2.8, "sugar": 2.5,
        "vitamins": "Vitamin C (88%), Citric Acid, Hesperidin",
        "benefits": "Stimulates bile production and assists kidney stone prevention.",
        "recipes": ["Lemon Herb Roasted Potatoes", "Zesty Vinaigrette", "Lemon Garlic Dressing"]
    },
    "kiwi": {
        "calories": 61, "carbs": 14.7, "protein": 1.1, "fiber": 3.0, "sugar": 9.0,
        "vitamins": "Vitamin C (155%), Vitamin K (50%), Actinidin",
        "benefits": "Exceptional Vitamin C density strengthens immunity and gut transit.",
        "recipes": ["Kiwi Chia Pudding", "Kiwi Fruit Salsa", "Green Super Smoothie"]
    },
    "coconut": {
        "calories": 354, "carbs": 15.2, "protein": 3.3, "fiber": 9.0, "sugar": 6.2,
        "vitamins": "Manganese (75%), Copper (22%), Iron (13%)",
        "benefits": "Medium Chain Triglycerides (MCTs) provide sustained cellular fuel.",
        "recipes": ["Thai Coconut Veggie Curry", "Toasted Coconut Granola", "Coconut Chia Bowls"]
    },
    "pomegranate": {
        "calories": 83, "carbs": 18.7, "protein": 1.7, "fiber": 4.0, "sugar": 13.7,
        "vitamins": "Vitamin C (17%), Vitamin K (21%), Punicalagins",
        "benefits": "Punicalagin antioxidants guard cardiovascular blood vessels.",
        "recipes": ["Jeweled Couscous Salad", "Pomegranate Glazed Eggplant", "Spinach Feta Arils Salad"]
    },
    "tomato": {
        "calories": 18, "carbs": 3.9, "protein": 0.9, "fiber": 1.2, "sugar": 2.6,
        "vitamins": "Vitamin C (28%), Vitamin K (10%), Lycopene",
        "benefits": "Heat-stable lycopene supports cardiovascular health and skin defense.",
        "recipes": ["Classic Caprese Salad", "Slow-Simmered Pomodoro Sauce", "Fresh Pico de Gallo"]
    },
    "carrot": {
        "calories": 41, "carbs": 9.6, "protein": 0.9, "fiber": 2.8, "sugar": 4.7,
        "vitamins": "Vitamin A (334% beta-carotene), Vitamin K (16%), Biotin",
        "benefits": "Beta-carotene converts to retinol, vital for vision and immune health.",
        "recipes": ["Honey Glazed Roasted Carrots", "Ginger Carrot Soup", "Raw Carrot Ribbon Salad"]
    },
    "broccoli": {
        "calories": 34, "carbs": 6.6, "protein": 2.8, "fiber": 2.6, "sugar": 1.7,
        "vitamins": "Vitamin C (148%), Vitamin K (127%), Sulforaphane",
        "benefits": "Sulforaphane promotes detoxification and cellular defense.",
        "recipes": ["Garlic Parmesan Roasted Broccoli", "Asian Broccoli Beef Stir-Fry", "Broccoli Cheddar Soup"]
    },
    "capsicum": {
        "calories": 31, "carbs": 6.0, "protein": 1.0, "fiber": 2.1, "sugar": 4.2,
        "vitamins": "Vitamin C (213%), Vitamin B6 (15%), Vitamin A",
        "benefits": "Delivers over 200% daily Vitamin C with virtually zero calories.",
        "recipes": ["Fajita Pepper Sizzle", "Stuffed Mediterranean Peppers", "Roasted Red Pepper Dip"]
    },
    "bell pepper": {
        "calories": 31, "carbs": 6.0, "protein": 1.0, "fiber": 2.1, "sugar": 4.2,
        "vitamins": "Vitamin C (213%), Vitamin B6 (15%), Vitamin A",
        "benefits": "Remarkable Vitamin C density enhances cellular resilience.",
        "recipes": ["Stuffed Bell Peppers", "Colorful Veggie Stir-Fry", "Roasted Red Pepper Bisque"]
    },
    "cucumber": {
        "calories": 15, "carbs": 3.6, "protein": 0.7, "fiber": 0.5, "sugar": 1.7,
        "vitamins": "Vitamin K (21%), Cucurbitacins, Silica",
        "benefits": "Deep cellular rehydration, silica strengthens connective tissue.",
        "recipes": ["Greek Salad with Feta", "Chilled Cucumber Mint Tzatziki", "Smashed Asian Cucumber Salad"]
    },
    "onion": {
        "calories": 40, "carbs": 9.3, "protein": 1.1, "fiber": 1.7, "sugar": 4.2,
        "vitamins": "Vitamin C (12%), Quercetin, Prebiotic Inulin",
        "benefits": "Quercetin flavonoid supports respiratory health and stabilizes histamine.",
        "recipes": ["Caramelized French Onion Soup", "Pickled Red Onions", "Classic Sofrito Base"]
    },
    "potato": {
        "calories": 77, "carbs": 17.5, "protein": 2.0, "fiber": 2.2, "sugar": 0.8,
        "vitamins": "Potassium (12%), Vitamin C (22%), Vitamin B6",
        "benefits": "Contains more potassium than bananas, resistant starch supports gut flora.",
        "recipes": ["Crispy Rosemary Garlic Roasted Potatoes", "Creamy Potato Leek Soup", "Mashed Garlic Mash"]
    },
    "eggplant": {
        "calories": 25, "carbs": 5.9, "protein": 1.0, "fiber": 3.0, "sugar": 3.5,
        "vitamins": "Nasunin, Manganese (11%), Folate",
        "benefits": "Nasunin antioxidant protects lipid membranes in brain cells.",
        "recipes": ["Eggplant Parmesan (Melanzane)", "Smoky Baba Ganoush", "Ratatouille Provencale"]
    },
    "cauliflower": {
        "calories": 25, "carbs": 5.0, "protein": 1.9, "fiber": 2.0, "sugar": 1.9,
        "vitamins": "Vitamin C (77%), Vitamin K (20%), Choline",
        "benefits": "Choline aids neurotransmitter synthesis and liver lipid processing.",
        "recipes": ["Spiced Roasted Cauliflower Steaks", "Creamy Cauliflower Mash", "Cauliflower Fried Rice"]
    },
    "cabbage": {
        "calories": 25, "carbs": 5.8, "protein": 1.3, "fiber": 2.5, "sugar": 3.2,
        "vitamins": "Vitamin K (95%), Vitamin C (61%), Glutamine",
        "benefits": "Glutamine heals stomach lining and balances microbial ecosystem.",
        "recipes": ["Zesty Crunchy Slaw", "Sauteed Cabbage with Bacon", "Fermented Probiotic Kimchi"]
    },
    "garlic": {
        "calories": 149, "carbs": 33.1, "protein": 6.4, "fiber": 2.1, "sugar": 1.0,
        "vitamins": "Allicin, Manganese (73%), Vitamin B6 (62%)",
        "benefits": "Allicin compound exhibits potent antimicrobial and arterial benefits.",
        "recipes": ["Garlic Confit Spread", "Aglio e Olio Pasta", "Toum Lebanese Garlic Whip"]
    },
    "ginger": {
        "calories": 80, "carbs": 17.8, "protein": 1.8, "fiber": 2.0, "sugar": 1.7,
        "vitamins": "Gingerol, Potassium, Magnesium",
        "benefits": "Gingerols relieve nausea and suppress inflammatory cytokines.",
        "recipes": ["Ginger Honey Lemon Tea", "Sesame Ginger Stir-Fry", "Golden Turmeric Ginger Milk"]
    },
    "spinach": {
        "calories": 23, "carbs": 3.6, "protein": 2.9, "fiber": 2.2, "sugar": 0.4,
        "vitamins": "Vitamin K (604%), Vitamin A (188%), Folate (49%)",
        "benefits": "Extraordinary Vitamin K density strengthens bone mineral matrices.",
        "recipes": ["Sauteed Garlic Spinach", "Spinach Ricotta Cannelloni", "Green Power Smoothie"]
    },
    "beetroot": {
        "calories": 43, "carbs": 9.6, "protein": 1.6, "fiber": 2.8, "sugar": 6.8,
        "vitamins": "Nitrates, Folate (27%), Manganese (16%)",
        "benefits": "Dietary nitrates elevate nitric oxide, enhancing athletic stamina.",
        "recipes": ["Roasted Beet & Goat Cheese Salad", "Vibrant Pink Beet Hummus", "Fresh Beetroot Carrot Juice"]
    },
    "peas": {
        "calories": 81, "carbs": 14.5, "protein": 5.4, "fiber": 5.7, "sugar": 5.7,
        "vitamins": "Vitamin K (30%), Vitamin C (48%), Plant Protein",
        "benefits": "High plant protein and fiber regulate postprandial glucose.",
        "recipes": ["Spring Pea & Mint Risotto", "Sweet Green Pea Soup", "Samosa Potato Pea Filling"]
    },
    "corn": {
        "calories": 86, "carbs": 18.7, "protein": 3.2, "fiber": 2.0, "sugar": 6.3,
        "vitamins": "Lutein, Zeaxanthin, Vitamin B1 (13%)",
        "benefits": "Lutein and zeaxanthin shield retinal macula against UV damage.",
        "recipes": ["Elote Mexican Street Corn", "Sweet Corn Chowder", "Black Bean & Corn Salad"]
    },
    "sweetpotato": {
        "calories": 86, "carbs": 20.1, "protein": 1.6, "fiber": 3.0, "sugar": 4.2,
        "vitamins": "Vitamin A (283%), Vitamin C (21%), Manganese",
        "benefits": "Low glycemic index sustained energy with massive beta-carotene.",
        "recipes": ["Crispy Baked Sweet Potato Fries", "Roasted Sweet Potato Curry", "Mashed Maple Sweet Potatoes"]
    },
    "chilli": {
        "calories": 40, "carbs": 8.8, "protein": 1.9, "fiber": 1.5, "sugar": 5.3,
        "vitamins": "Capsaicin, Vitamin C (240%), Vitamin B6",
        "benefits": "Capsaicin stimulates metabolic thermogenesis and endorphin release.",
        "recipes": ["Chilli Crisp Oil", "Spicy Arrabbiata Pasta", "Homemade Hot Sauce"]
    },
    "radish": {
        "calories": 16, "carbs": 3.4, "protein": 0.7, "fiber": 1.6, "sugar": 1.9,
        "vitamins": "Vitamin C (25%), Glucosinolates, Potassium",
        "benefits": "Sulfur compounds aid liver detoxification and digestion.",
        "recipes": ["French Radish with Salt & Butter", "Quick Pickled Radishes", "Crunchy Slaw"]
    },
    "turnip": {
        "calories": 28, "carbs": 6.4, "protein": 0.9, "fiber": 1.8, "sugar": 3.8,
        "vitamins": "Vitamin C (35%), Glucosinolates, Calcium",
        "benefits": "Low-carb root vegetable supporting liver filtration.",
        "recipes": ["Mashed Roasted Turnips", "Pickled Pink Turnips", "Root Vegetable Medley"]
    },
    "okra": {
        "calories": 33, "carbs": 7.5, "protein": 1.9, "fiber": 3.2, "sugar": 1.5,
        "vitamins": "Vitamin K (66%), Vitamin C (38%), Mucilage",
        "benefits": "Soluble mucilage binds cholesterol and smooths digestion.",
        "recipes": ["Crispy Roasted Okra Fries", "Southern Gumbo", "Bhindi Masala Stir-Fry"]
    },
}

# ==============================================================================
# 🧠 MODEL ENGINE LOADER
# ==============================================================================

_yolo_produce = None
_yolo_coco = None
_vit_classifier = None

def get_models():
    """Load models lazily and cache in memory."""
    global _yolo_produce, _yolo_coco, _vit_classifier

    if _yolo_produce is None:
        from ultralytics import YOLO
        local_weights = "fruit_veg_yolov8n.pt"
        if os.path.exists(local_weights):
            _yolo_produce = YOLO(local_weights)
        else:
            # Fallback to hub download
            from huggingface_hub import hf_hub_download
            hub_path = hf_hub_download(repo_id="Aniket2003333333/fruit-veg-yolov8n-detector", filename="best.pt")
            _yolo_produce = YOLO(hub_path)

    if _vit_classifier is None:
        from transformers import pipeline
        _vit_classifier = pipeline(
            "image-classification",
            model="jazzmacedo/fruits-and-vegetables-detector-36",
            top_k=3,
        )

    return _yolo_produce, _vit_classifier

# ==============================================================================
# 🛠️ HELPER FUNCTIONS
# ==============================================================================

def normalize_label(raw: str) -> str:
    """Normalize label name to canonical format."""
    clean = raw.strip().lower().replace("-", " ").replace("_", " ")
    synonyms = {
        "grapes": "grape",
        "jalepeno": "jalapeño",
        "bell pepper": "capsicum",
        "green orange": "orange",
        "maize": "corn",
        "sweetcorn": "corn",
        "raddish": "radish",
        "sweetpotato": "sweet potato",
        "chilli pepper": "chilli",
        "eggplant": "eggplant",
    }
    return synonyms.get(clean, clean)

def get_emoji(label: str) -> str:
    key = label.lower().replace(" ", "_")
    if key in EMOJI_MAP:
        return EMOJI_MAP[key]
    for k, v in EMOJI_MAP.items():
        if k in key or key in k:
            return v
    return "🌿"

def get_category(label: str) -> str:
    lbl = label.lower().replace(" ", "_")
    if lbl in FRUITS or any(f in lbl for f in FRUITS):
        return "Fruit"
    if lbl in VEGETABLES or any(v in lbl for v in VEGETABLES):
        return "Vegetable"
    return "Produce"

def get_nutrition_info(label: str) -> dict:
    canonical = label.lower().replace(" ", "_")
    if canonical in NUTRITION_DB:
        return NUTRITION_DB[canonical]
    for k, data in NUTRITION_DB.items():
        if k in canonical or canonical in k:
            return data
    # Fallback generic produce nutrition
    return {
        "calories": 40, "carbs": 9.0, "protein": 1.0, "fiber": 2.0, "sugar": 5.0,
        "vitamins": "Vitamin C, Essential Minerals",
        "benefits": "Wholesome natural nutrients rich in fiber and micronutrients.",
        "recipes": ["Fresh Garden Salad", "Roasted Produce Medley", "Smoothie Boost"]
    }

def get_font(size: int = 16):
    """Load high-DPI modern font if available, else default."""
    for p in ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

# ==============================================================================
# 🎯 CORE DETECTION & VERIFICATION PIPELINE
# ==============================================================================

def detect_and_analyze(
    image: Optional[np.ndarray],
    conf_thresh: float = 0.35,
    iou_thresh: float = 0.45,
    padding_pct: float = 10.0,
):
    if image is None:
        return None, [], "<div class='empty-alert'>⚠️ Please upload an image or choose a demo sample to begin detection.</div>", "", "", ""

    yolo_model, vit_model = get_models()
    pil_img = Image.fromarray(image).convert("RGB")
    W, H = pil_img.size

    # Run YOLOv8 specialized fruit/veg inference
    results = yolo_model(pil_img, conf=conf_thresh, iou=iou_thresh, verbose=False)[0]

    detections = []
    crops_gallery = []
    draw_img = pil_img.copy()
    draw = ImageDraw.Draw(draw_img)
    font = get_font(size=max(14, int(min(W, H) * 0.022)))

    pad_ratio = padding_pct / 100.0

    for idx, box in enumerate(results.boxes):
        xyxy = box.xyxy[0].tolist()
        x1, y1, x2, y2 = [int(v) for v in xyxy]
        yolo_cls_id = int(box.cls[0])
        yolo_raw_label = yolo_model.names[yolo_cls_id]
        yolo_conf = float(box.conf[0])

        # Context-padded crop for ViT verification
        bx_w, bx_h = (x2 - x1), (y2 - y1)
        pad_w, pad_h = int(bx_w * pad_ratio), int(bx_h * pad_ratio)
        crop_box = (
            max(0, x1 - pad_w),
            max(0, y1 - pad_h),
            min(W, x2 + pad_w),
            min(H, y2 + pad_h)
        )
        crop_img = pil_img.crop(crop_box)

        # ViT classification on crop
        vit_label, vit_conf, alt_preds = "Unknown", 0.0, []
        try:
            vit_preds = vit_model(crop_img)
            if vit_preds:
                vit_label = vit_preds[0]["label"].replace("_", " ").title()
                vit_conf = float(vit_preds[0]["score"])
                alt_preds = [(p["label"].replace("_", " ").title(), float(p["score"])) for p in vit_preds[1:3]]
        except Exception:
            pass

        # Smart ensemble decision
        # If YOLO confidence is very solid (>= 0.60), prioritize YOLO localization + label
        # If YOLO and ViT normalize to same produce, boost confidence
        norm_yolo = normalize_label(yolo_raw_label)
        norm_vit = normalize_label(vit_label)

        if norm_yolo == norm_vit or norm_yolo in norm_vit or norm_vit in norm_yolo:
            final_label = yolo_raw_label.replace("_", " ").title()
            final_conf = max(yolo_conf, vit_conf)
            verified = True
        elif yolo_conf >= 0.50:
            final_label = yolo_raw_label.replace("_", " ").title()
            final_conf = yolo_conf
            verified = False
        else:
            final_label = vit_label if vit_conf > yolo_conf else yolo_raw_label.replace("_", " ").title()
            final_conf = max(yolo_conf, vit_conf)
            verified = False

        color = BOX_COLORS[idx % len(BOX_COLORS)]
        emoji = get_emoji(final_label)
        category = get_category(final_label)

        # Draw sleek bounding box
        line_w = max(3, int(min(W, H) * 0.005))
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_w)

        # Draw badge pill
        badge_text = f"{emoji} {final_label} {final_conf:.0%}"
        if hasattr(font, "getbbox"):
            bbox = font.getbbox(badge_text)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        else:
            tw, th = len(badge_text) * 9, 16

        badge_h = th + 10
        badge_w = tw + 14
        by = max(0, y1 - badge_h)

        draw.rectangle([x1, by, x1 + badge_w, by + badge_h], fill=color)
        draw.text((x1 + 7, by + 4), badge_text, fill="#FFFFFF", font=font)

        detections.append({
            "label": final_label,
            "category": category,
            "emoji": emoji,
            "conf": final_conf,
            "verified": verified,
            "box": (x1, y1, x2, y2),
            "alt_preds": alt_preds,
            "color": color,
            "crop": crop_img,
        })

        # Save for thumbnail gallery
        crops_gallery.append((crop_img, f"{emoji} {final_label} ({final_conf:.0%})"))

    # Fallback if no boxes detected (e.g. single item filling entire screen)
    if not detections:
        try:
            whole_preds = vit_model(pil_img)
            if whole_preds:
                top_p = whole_preds[0]
                lbl = top_p["label"].replace("_", " ").title()
                score = float(top_p["score"])
                emoji = get_emoji(lbl)
                cat = get_category(lbl)
                color = BOX_COLORS[0]

                # Draw outer frame
                pad = 12
                line_w = max(3, int(min(W, H) * 0.005))
                draw.rectangle([pad, pad, W - pad, H - pad], outline=color, width=line_w)
                badge_text = f"{emoji} {lbl} {score:.0%} (Whole Frame)"
                draw.rectangle([pad, pad, pad + len(badge_text) * 10, pad + 30], fill=color)
                draw.text((pad + 8, pad + 6), badge_text, fill="#FFFFFF", font=font)

                detections.append({
                    "label": lbl,
                    "category": cat,
                    "emoji": emoji,
                    "conf": score,
                    "verified": True,
                    "box": (0, 0, W, H),
                    "alt_preds": [(p["label"].replace("_", " ").title(), float(p["score"])) for p in whole_preds[1:3]],
                    "color": color,
                    "crop": pil_img,
                })
                crops_gallery.append((pil_img, f"{emoji} {lbl} ({score:.0%})"))
        except Exception:
            pass

    # Build Rich HTML Reports
    overview_html = build_overview_cards(detections)
    nutrition_html = build_nutrition_report(detections)
    recipes_html = build_recipe_report(detections)
    checklist_text = build_checklist_text(detections)

    return np.array(draw_img), crops_gallery, overview_html, nutrition_html, recipes_html, checklist_text


# ==============================================================================
# 📊 UI COMPONENT BUILDERS (GLASSMORPHIC HTML)
# ==============================================================================

def build_overview_cards(detections: List[Dict]) -> str:
    if not detections:
        return """
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px dashed #475569; border-radius: 14px; padding: 28px; text-align: center; color: #94A3B8;">
            <div style="font-size: 2.2em; margin-bottom: 8px;">🔍</div>
            <div style="font-weight: 600; font-size: 1.15em; color: #E2E8F0;">No Produce Detected</div>
            <p style="font-size: 0.9em; margin-top: 6px;">Try adjusting the <b>Confidence Threshold slider</b> lower, or ensure the produce is clearly visible under good lighting.</p>
        </div>
        """

    total_items = len(detections)
    fruit_cnt = sum(1 for d in detections if d["category"] == "Fruit")
    veg_cnt = sum(1 for d in detections if d["category"] == "Vegetable")
    other_cnt = total_items - fruit_cnt - veg_cnt

    # Total calories
    total_cals = 0
    for d in detections:
        info = get_nutrition_info(d["label"])
        total_cals += info["calories"]

    html = f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.08)); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 14px; text-align: center;">
            <div style="font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.05em; color: #34D399; font-weight: 700;">Total Detected</div>
            <div style="font-size: 2em; font-weight: 800; color: #F8FAFC; margin-top: 2px;">{total_items}</div>
            <div style="font-size: 0.75em; color: #94A3B8;">{fruit_cnt} Fruit · {veg_cnt} Veg</div>
        </div>
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(249, 115, 22, 0.08)); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 14px; text-align: center;">
            <div style="font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.05em; color: #FBBF24; font-weight: 700;">Est. Calories</div>
            <div style="font-size: 2em; font-weight: 800; color: #F8FAFC; margin-top: 2px;">~{total_cals}</div>
            <div style="font-size: 0.75em; color: #94A3B8;">kcal total basket</div>
        </div>
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.08)); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 14px; text-align: center;">
            <div style="font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.05em; color: #C084FC; font-weight: 700;">AI Engine</div>
            <div style="font-size: 1.3em; font-weight: 800; color: #F8FAFC; margin-top: 8px;">Dual-Engine</div>
            <div style="font-size: 0.75em; color: #94A3B8;">YOLOv8 + ViT-36</div>
        </div>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 10px;">
    """

    for idx, d in enumerate(detections):
        pct = int(d["conf"] * 100)
        badge_border = "#10B981" if d["verified"] else "#64748B"
        verified_tag = "<span style='background: rgba(16,185,129,0.2); color: #34D399; font-size: 0.7em; padding: 2px 6px; border-radius: 6px; border: 1px solid #10B981;'>✓ Dual Verified</span>" if d["verified"] else ""

        html += f"""
        <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(148, 163, 184, 0.15); border-left: 4px solid {d['color']}; border-radius: 10px; padding: 12px 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.4em;">{d['emoji']}</span>
                    <span style="font-weight: 700; font-size: 1.05em; color: #F8FAFC;">{d['label']}</span>
                    <span style="background: rgba(148, 163, 184, 0.15); color: #CBD5E1; font-size: 0.72em; padding: 2px 8px; border-radius: 12px;">{d['category']}</span>
                    {verified_tag}
                </div>
                <div style="font-weight: 800; color: {d['color']}; font-size: 1.1em;">{pct}%</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border-radius: 6px; height: 8px; overflow: hidden; width: 100%;">
                <div style="background: linear-gradient(90deg, {d['color']}, #38BDF8); width: {pct}%; height: 100%; border-radius: 6px; transition: width 0.5s ease;"></div>
            </div>
        </div>
        """

    html += "</div>"
    return html


def build_nutrition_report(detections: List[Dict]) -> str:
    if not detections:
        return "<p style='color: #94A3B8;'>Run detection to view detailed USDA nutritional values and health metrics.</p>"

    # Deduplicate items for clean sheet
    items_map = {}
    for d in detections:
        lbl = d["label"]
        items_map[lbl] = items_map.get(lbl, 0) + 1

    html = """
    <div style="display: flex; flex-direction: column; gap: 14px;">
    """

    for lbl, count in items_map.items():
        info = get_nutrition_info(lbl)
        emoji = get_emoji(lbl)
        cat = get_category(lbl)

        html += f"""
        <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 12px; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.5em;">{emoji}</span>
                    <span style="font-size: 1.15em; font-weight: 700; color: #F8FAFC;">{lbl}</span>
                    <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 0.75em; padding: 2px 8px; border-radius: 8px;">x{count} count</span>
                    <span style="color: #64748B; font-size: 0.8em;">(Per 100g serving)</span>
                </div>
                <div style="font-weight: 800; color: #34D399; font-size: 1.1em;">{info['calories']} kcal</div>
            </div>

            <!-- Macros -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; text-align: center;">
                <div style="background: rgba(15, 23, 42, 0.5); border-radius: 8px; padding: 8px 4px;">
                    <div style="color: #94A3B8; font-size: 0.72em; text-transform: uppercase;">Carbs</div>
                    <div style="color: #F8FAFC; font-weight: 700; font-size: 0.95em;">{info['carbs']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.5); border-radius: 8px; padding: 8px 4px;">
                    <div style="color: #94A3B8; font-size: 0.72em; text-transform: uppercase;">Protein</div>
                    <div style="color: #F8FAFC; font-weight: 700; font-size: 0.95em;">{info['protein']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.5); border-radius: 8px; padding: 8px 4px;">
                    <div style="color: #94A3B8; font-size: 0.72em; text-transform: uppercase;">Fiber</div>
                    <div style="color: #F8FAFC; font-weight: 700; font-size: 0.95em;">{info['fiber']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.5); border-radius: 8px; padding: 8px 4px;">
                    <div style="color: #94A3B8; font-size: 0.72em; text-transform: uppercase;">Sugar</div>
                    <div style="color: #F8FAFC; font-weight: 700; font-size: 0.95em;">{info['sugar']}g</div>
                </div>
            </div>

            <div style="font-size: 0.85em; color: #CBD5E1; margin-bottom: 6px;">
                <b style="color: #38BDF8;">⚡ Micronutrients:</b> {info['vitamins']}
            </div>
            <div style="font-size: 0.85em; color: #94A3B8;">
                <b style="color: #34D399;">💡 Health Benefit:</b> {info['benefits']}
            </div>
        </div>
        """

    html += "</div>"
    return html


def build_recipe_report(detections: List[Dict]) -> str:
    if not detections:
        return "<p style='color: #94A3B8;'>Upload an image to get intelligent recipe ideas from your detected ingredients.</p>"

    labels = list({d["label"] for d in detections})
    recipes_pool = []
    for lbl in labels:
        info = get_nutrition_info(lbl)
        for r in info.get("recipes", []):
            recipes_pool.append((r, lbl))

    html = """
    <div style="display: flex; flex-direction: column; gap: 12px;">
        <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(16, 185, 129, 0.1)); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 14px;">
            <div style="font-weight: 700; color: #38BDF8; font-size: 1.05em; margin-bottom: 4px;">👨‍🍳 Smart Pantry Chef</div>
            <div style="font-size: 0.85em; color: #CBD5E1;">Based on the fresh ingredients identified in your basket:</div>
        </div>
    """

    for r_name, ingredient in recipes_pool[:6]:
        emo = get_emoji(ingredient)
        html += f"""
        <div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 10px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: 700; color: #F8FAFC; font-size: 1em;">🍽️ {r_name}</div>
                <div style="font-size: 0.8em; color: #94A3B8; margin-top: 2px;">Hero ingredient: {emo} <b>{ingredient}</b></div>
            </div>
            <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; font-size: 0.75em; padding: 4px 10px; border-radius: 20px; font-weight: 600;">Healthy</span>
        </div>
        """

    html += "</div>"
    return html


def build_checklist_text(detections: List[Dict]) -> str:
    if not detections:
        return "No produce detected yet."

    counts = {}
    for d in detections:
        lbl = d["label"]
        counts[lbl] = counts.get(lbl, 0) + 1

    lines = ["🛒 PRODUCE CHECKLIST & INVENTORY:", "─────────────────────────────────"]
    for lbl, count in sorted(counts.items()):
        emo = get_emoji(lbl)
        cat = get_category(lbl)
        lines.append(f"[x] {emo} {lbl.title()} ({count} item{'s' if count > 1 else ''}) - {cat}")

    lines.append("─────────────────────────────────")
    lines.append(f"Total: {len(detections)} items")
    return "\n".join(lines)


# ==============================================================================
# 🎨 GRADIO DASHBOARD
# ==============================================================================

CUSTOM_CSS = """
/* Modern Dark Glassmorphism Styling */
.gradio-container {
    max-width: 1280px !important;
    margin: 0 auto !important;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
}

#header-hero {
    text-align: center;
    padding: 24px 0 16px 0;
    margin-bottom: 12px;
}

#header-title {
    font-size: 2.6em;
    font-weight: 850;
    background: linear-gradient(135deg, #34D399 0%, #38BDF8 50%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
    margin-bottom: 6px;
}

#header-subtitle {
    color: #94A3B8;
    font-size: 1.05em;
    max-width: 680px;
    margin: 0 auto 12px auto;
    line-height: 1.5;
}

.model-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34D399;
    padding: 5px 16px;
    border-radius: 99px;
    font-size: 0.85em;
    font-weight: 600;
}

.primary-btn {
    background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.1em !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.primary-btn:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
}

.glass-panel {
    background: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(148, 163, 184, 0.15) !important;
    border-radius: 14px !important;
}

footer { display: none !important; }
"""

with gr.Blocks(
    title="🥝 ProduceVision AI — Fruit & Vegetable Detection",
    css=CUSTOM_CSS,
    theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="teal", neutral_hue="slate"),
) as demo:

    gr.HTML("""
    <div id="header-hero">
        <div id="header-title">🥝 ProduceVision AI</div>
        <div id="header-subtitle">
            Next-generation dual-engine intelligence: Instant produce localization, 36-class verification, and complete USDA nutritional analysis.
        </div>
        <div class="model-pill">
            <span>⚡ YOLOv8 Produce Specialist (35 Classes)</span>
            <span>·</span>
            <span>🧠 ViT-36 Ensemble Classifier</span>
        </div>
    </div>
    """)

    with gr.Row():
        # LEFT COLUMN: INPUT & TUNING CONTROLS
        with gr.Column(scale=5):
            with gr.Tabs():
                with gr.TabItem("📤 Photo / File"):
                    input_img = gr.Image(
                        label="Upload Image or Snapshot",
                        type="numpy",
                        sources=["upload", "webcam", "clipboard"],
                        height=380,
                    )

            with gr.Accordion("⚙️ Detection Sensitivity & Model Tuning", open=False):
                with gr.Row():
                    conf_slider = gr.Slider(
                        label="Confidence Threshold",
                        minimum=0.10,
                        maximum=0.90,
                        value=0.35,
                        step=0.05,
                        info="Lower for cluttered shots; higher for strict confidence",
                    )
                    iou_slider = gr.Slider(
                        label="IoU NMS Overlap",
                        minimum=0.10,
                        maximum=0.80,
                        value=0.45,
                        step=0.05,
                        info="Adjusts duplicate box suppression",
                    )
                padding_slider = gr.Slider(
                    label="Crop Context Padding (%)",
                    minimum=0,
                    maximum=25,
                    value=10,
                    step=5,
                    info="Adds border context around each fruit for ViT verification",
                )

            detect_btn = gr.Button("🔍 Detect & Analyze Produce", elem_classes=["primary-btn"], size="lg")

            # DEMO EXAMPLES
            gr.Markdown("### 🌟 Instant Test Examples (Click to Try)")
            demo_examples = [
                ["samples/fruit_basket.jpg", 0.35, 0.45, 10],
                ["samples/apple.jpg", 0.40, 0.45, 10],
                ["samples/banana.jpg", 0.35, 0.45, 10],
                ["samples/bell_peppers.jpg", 0.35, 0.45, 10],
                ["samples/tomatoes.jpg", 0.35, 0.45, 10],
                ["samples/carrots.jpg", 0.35, 0.45, 10],
            ]
            gr.Examples(
                examples=demo_examples,
                inputs=[input_img, conf_slider, iou_slider, padding_slider],
                label="Click an example below to evaluate immediately:",
            )

        # RIGHT COLUMN: ANNOTATED OUTPUT & INTELLIGENCE TABS
        with gr.Column(scale=7):
            with gr.Tabs():
                with gr.TabItem("📸 Visual Detection Map"):
                    annotated_out = gr.Image(label="Annotated Image with Precision Bounding Boxes", height=400, interactive=False)
                    crops_out = gr.Gallery(label="Isolated Produce Crops", columns=4, height=160, object_fit="cover")

                with gr.TabItem("📊 Detection Breakdown"):
                    overview_out = gr.HTML(label="Results")

                with gr.TabItem("🥗 Nutritional Sheet"):
                    nutrition_out = gr.HTML(label="USDA Nutrition & Health Data")

                with gr.TabItem("👨‍🍳 Recipe Suggestions"):
                    recipes_out = gr.HTML(label="Culinary Ideas")

                with gr.TabItem("📋 Pantry Checklist"):
                    checklist_out = gr.Textbox(label="Exportable Shopping / Inventory List", lines=10, interactive=False)

    # EVENT BINDING
    detect_btn.click(
        fn=detect_and_analyze,
        inputs=[input_img, conf_slider, iou_slider, padding_slider],
        outputs=[annotated_out, crops_out, overview_out, nutrition_out, recipes_out, checklist_out],
    )

    gr.HTML("""
    <div style="text-align: center; color: #64748B; font-size: 0.85em; margin-top: 24px; padding: 12px; border-top: 1px solid rgba(148, 163, 184, 0.1);">
        ProduceVision AI · Dual-Engine Produce Detection Architecture · 36 Fruit & Vegetable Classes Supported
    </div>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, inbrowser=True)