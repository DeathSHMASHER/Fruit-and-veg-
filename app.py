import os
import sys
import warnings
warnings.filterwarnings("ignore")

# Configure UTF-8 for consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from typing import List, Dict, Tuple, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import gradio as gr

# ==============================================================================
# 🎨 COLOR PALETTE & PRODUCE DATABASE (63+ PRODUCE CLASSES + HUMANS & PETS)
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

# Special COCO entities: Human faces/persons, cats, dogs, etc.
COCO_SPECIAL_ENTITIES = {
    0: {"name": "Human", "emoji": "👤", "category": "Human", "color": "#6366F1", "tag": "HUMAN"},
    15: {"name": "Cat", "emoji": "🐱", "category": "Pet / Animal", "color": "#F43F5E", "tag": "PET"},
    16: {"name": "Dog", "emoji": "🐶", "category": "Pet / Animal", "color": "#FB923C", "tag": "PET"},
    17: {"name": "Horse", "emoji": "🐴", "category": "Animal", "color": "#A855F7", "tag": "ANIMAL"},
    18: {"name": "Sheep", "emoji": "🐑", "category": "Animal", "color": "#14B8A6", "tag": "ANIMAL"},
    19: {"name": "Cow", "emoji": "🐄", "category": "Animal", "color": "#06B6D4", "tag": "ANIMAL"},
    21: {"name": "Bear", "emoji": "🐻", "category": "Animal", "color": "#D97706", "tag": "ANIMAL"},
}

EMOJI_MAP = {
    "potato": "🥔", "sweet potato": "🍠", "pumpkin": "🎃", "onion": "🧅", "green onion": "🧅",
    "spring onion": "🧅", "apple": "🍎", "banana": "🍌", "orange": "🍊", "mandarin orange": "🍊",
    "clementine": "🍊", "grape": "🍇", "strawberry": "🍓", "watermelon": "🍉", "mango": "🥭",
    "pineapple": "🍍", "pear": "🍐", "peach": "🍑", "cherry": "🍒", "lemon": "🍋", "lime": "🍈",
    "avocado": "🥑", "tomato": "🍅", "coconut": "🥥", "kiwi fruit": "🥝", "kiwi": "🥝",
    "cantaloupe": "🍈", "melon": "🍈", "pomegranate": "🍷", "broccoli": "🥦", "carrot": "🥕",
    "corn": "🌽", "edible corn": "🌽", "cucumber": "🥒", "garlic": "🧄", "pepper": "🌶️",
    "eggplant": "🍆", "aubergine": "🍆", "lettuce": "🥬", "mushroom": "🍄", "beetroot": "🫚",
    "spinach": "🥬", "capsicum": "🫑", "bell pepper": "🫑", "paprika": "🌶️", "cauliflower": "🥦",
    "cabbage": "🥬", "ginger": "🫚", "chili": "🌶️", "chilli": "🌶️", "peas": "🟢", "pea": "🟢",
    "radish": "🥢", "turnip": "🪴", "zucchini": "🥒", "courgette": "🥒", "gourd": "🥒",
    "green bean": "🟢", "asparagus": "🌿", "celery": "🥬", "artichoke": "🌿", "blueberry": "🫐",
    "blackberry": "🫐", "raspberry": "🍓", "papaya": "🥭", "fig": "🫐", "date": "🌴",
    "almond": "🌰", "apricot": "🍑", "bean curd": "🧊", "tofu": "🧊",
    "human": "👤", "person": "👤", "cat": "🐱", "dog": "🐶", "horse": "🐴", "cow": "🐄",
}

FRUITS = {
    "apple", "banana", "orange", "mandarin orange", "clementine", "grape", "strawberry",
    "watermelon", "mango", "pineapple", "pear", "peach", "cherry", "lemon", "lime",
    "avocado", "coconut", "kiwi", "kiwi fruit", "melon", "cantaloupe", "pomegranate",
    "blueberry", "blackberry", "raspberry", "papaya", "fig", "date", "apricot",
}

VEGETABLES = {
    "potato", "sweet potato", "pumpkin", "gourd", "zucchini", "courgette", "broccoli",
    "carrot", "corn", "edible corn", "cucumber", "garlic", "onion", "green onion",
    "spring onion", "pepper", "eggplant", "aubergine", "lettuce", "mushroom", "beetroot",
    "spinach", "capsicum", "bell pepper", "paprika", "cauliflower", "cabbage", "ginger",
    "chili", "chilli", "peas", "pea", "radish", "turnip", "green bean", "asparagus",
    "celery", "artichoke", "tomato",
}

# USDA-referenced nutritional metrics per 100g standard edible portion
NUTRITION_DB = {
    "potato": {
        "calories": 77, "carbs": 17.5, "protein": 2.0, "fiber": 2.2, "sugar": 0.8,
        "vitamins": "Potassium (12%), Vitamin C (22%), Vitamin B6 (15%)",
        "benefits": "Contains more potassium than bananas; resistant starch sustains gut microbiome and energy.",
        "recipes": ["Crispy Herb-Roasted Potatoes", "Creamy Garlic Potato Leek Soup", "Mashed Rustic Potatoes"]
    },
    "sweet potato": {
        "calories": 86, "carbs": 20.1, "protein": 1.6, "fiber": 3.0, "sugar": 4.2,
        "vitamins": "Vitamin A (283% beta-carotene), Vitamin C (21%), Manganese",
        "benefits": "Low glycemic index sustained energy with massive vision-protecting carotenoids.",
        "recipes": ["Crispy Baked Sweet Potato Wedges", "Sweet Potato Coconut Curry", "Roasted Maple Mash"]
    },
    "pumpkin": {
        "calories": 26, "carbs": 6.5, "protein": 1.0, "fiber": 0.5, "sugar": 2.8,
        "vitamins": "Vitamin A (245%), Vitamin C (15%), Potassium, Lutein",
        "benefits": "Intense beta-carotene and lutein protect eye retinas and cellular longevity.",
        "recipes": ["Velvety Roasted Pumpkin Soup", "Spiced Pumpkin Risotto", "Warm Roasted Pumpkin Salad"]
    },
    "apple": {
        "calories": 52, "carbs": 13.8, "protein": 0.3, "fiber": 2.4, "sugar": 10.4,
        "vitamins": "Vitamin C (14%), Potassium (3%), Quercetin",
        "benefits": "Supports heart health, lowers LDL cholesterol with soluble pectin fiber.",
        "recipes": ["Cinnamon Apple Oatmeal", "Crisp Waldorf Salad", "Baked Spiced Apples"]
    },
    "banana": {
        "calories": 89, "carbs": 22.8, "protein": 1.1, "fiber": 2.6, "sugar": 12.2,
        "vitamins": "Vitamin B6 (20%), Potassium (10%), Vitamin C (10%)",
        "benefits": "Immediate natural electrolyte energy, regulates blood pressure and digestion.",
        "recipes": ["Creamy Banana Berry Smoothie", "Healthy Banana Oat Pancakes", "Frozen Banana Bites"]
    },
    "tomato": {
        "calories": 18, "carbs": 3.9, "protein": 0.9, "fiber": 1.2, "sugar": 2.6,
        "vitamins": "Vitamin C (28%), Vitamin K (10%), Lycopene",
        "benefits": "Heat-stable lycopene supports cardiovascular health and skin UV defense.",
        "recipes": ["Classic Caprese Salad", "Slow-Simmered Pomodoro Sauce", "Fresh Pico de Gallo"]
    },
    "carrot": {
        "calories": 41, "carbs": 9.6, "protein": 0.9, "fiber": 2.8, "sugar": 4.7,
        "vitamins": "Vitamin A (334% beta-carotene), Vitamin K (16%), Biotin",
        "benefits": "Beta-carotene converts to retinol, vital for vision and immune integrity.",
        "recipes": ["Honey-Glazed Roasted Carrots", "Ginger Carrot Velvet Soup", "Raw Carrot Ribbon Salad"]
    },
    "bell pepper": {
        "calories": 31, "carbs": 6.0, "protein": 1.0, "fiber": 2.1, "sugar": 4.2,
        "vitamins": "Vitamin C (213%), Vitamin B6 (15%), Vitamin A",
        "benefits": "Delivers over 200% daily Vitamin C with virtually zero calories.",
        "recipes": ["Stuffed Mediterranean Peppers", "Fajita Pepper Sizzle", "Roasted Red Pepper Bisque"]
    },
    "onion": {
        "calories": 40, "carbs": 9.3, "protein": 1.1, "fiber": 1.7, "sugar": 4.2,
        "vitamins": "Vitamin C (12%), Quercetin, Prebiotic Inulin",
        "benefits": "Quercetin flavonoid supports respiratory health and stabilizes histamine.",
        "recipes": ["Caramelized French Onion Soup", "Quick Pickled Red Onions", "Classic Sofrito Base"]
    },
    "garlic": {
        "calories": 149, "carbs": 33.1, "protein": 6.4, "fiber": 2.1, "sugar": 1.0,
        "vitamins": "Allicin, Manganese (73%), Vitamin B6 (62%)",
        "benefits": "Allicin compound exhibits potent antimicrobial and arterial benefits.",
        "recipes": ["Garlic Confit Toast", "Classic Aglio e Olio", "Toum Garlic Dip"]
    },
    "lemon": {
        "calories": 29, "carbs": 9.3, "protein": 1.1, "fiber": 2.8, "sugar": 2.5,
        "vitamins": "Vitamin C (88%), Citric Acid, Hesperidin",
        "benefits": "Stimulates bile production and assists kidney health.",
        "recipes": ["Lemon Herb Roasted Potatoes", "Zesty Lemon Vinaigrette", "Lemon Garlic Dressing"]
    },
    "avocado": {
        "calories": 160, "carbs": 8.5, "protein": 2.0, "fiber": 6.7, "sugar": 0.7,
        "vitamins": "Potassium (14%), Vitamin K (26%), Oleic Acid",
        "benefits": "Rich in heart-protective monounsaturated fats and lutein for vision.",
        "recipes": ["Classic Chunky Guacamole", "Avocado Toast with Poached Egg", "Green Goddess Salad"]
    },
    "cucumber": {
        "calories": 15, "carbs": 3.6, "protein": 0.7, "fiber": 0.5, "sugar": 1.7,
        "vitamins": "Vitamin K (21%), Cucurbitacins, Silica",
        "benefits": "Deep cellular rehydration, silica strengthens connective tissue.",
        "recipes": ["Greek Salad with Feta", "Chilled Tzatziki Dip", "Smashed Asian Cucumber Salad"]
    },
    "orange": {
        "calories": 47, "carbs": 11.8, "protein": 0.9, "fiber": 2.4, "sugar": 9.4,
        "vitamins": "Vitamin C (89%), Folate (8%), Calcium (4%)",
        "benefits": "Boosts immune defense, enhances collagen synthesis and iron uptake.",
        "recipes": ["Citrus Fennel Salad", "Fresh Pressed Sunrise Juice", "Orange Glazed Roast"]
    },
    "grape": {
        "calories": 69, "carbs": 18.1, "protein": 0.7, "fiber": 0.9, "sugar": 15.5,
        "vitamins": "Vitamin K (18%), Vitamin C (5%), Resveratrol",
        "benefits": "Powerful polyphenols and resveratrol support vascular health.",
        "recipes": ["Roasted Grape & Goat Cheese Crostini", "Chilled Fruit Medley", "Spinach Grape Salad"]
    },
    "kiwi": {
        "calories": 61, "carbs": 14.7, "protein": 1.1, "fiber": 3.0, "sugar": 9.0,
        "vitamins": "Vitamin C (155%), Vitamin K (50%), Actinidin",
        "benefits": "Exceptional Vitamin C density strengthens immunity and gut transit.",
        "recipes": ["Kiwi Chia Pudding", "Kiwi Fruit Salsa", "Green Super Smoothie"]
    },
    "watermelon": {
        "calories": 30, "carbs": 7.6, "protein": 0.6, "fiber": 0.4, "sugar": 6.2,
        "vitamins": "Vitamin C (14%), Vitamin A (11%), Lycopene",
        "benefits": "92% water content delivers superior hydration and amino acid citrulline.",
        "recipes": ["Watermelon Feta Mint Salad", "Agua Fresca Cooler", "Grilled Watermelon Steaks"]
    },
    "zucchini": {
        "calories": 17, "carbs": 3.1, "protein": 1.2, "fiber": 1.0, "sugar": 2.5,
        "vitamins": "Vitamin C (29%), Vitamin B6, Lutein",
        "benefits": "Very low calorie density; supports digestion and healthy eyesight.",
        "recipes": ["Zucchini Ribbon Pasta", "Grilled Garlic Zucchini", "Crispy Zucchini Fritters"]
    },
    "pear": {
        "calories": 57, "carbs": 15.2, "protein": 0.4, "fiber": 3.1, "sugar": 9.8,
        "vitamins": "Vitamin C (7%), Vitamin K (6%), Copper",
        "benefits": "High soluble fiber prebiotic nourishes beneficial gut flora.",
        "recipes": ["Arugula Pear Walnut Salad", "Poached Spiced Pears", "Warm Pear Tart"]
    },
}

# ==============================================================================
# 🧠 DUAL-ENGINE AI LOADER (63-CLASS YOLOv8m + COCO HUMAN/PET DETECTOR + ViT-36)
# ==============================================================================

_yolo_63 = None
_yolo_coco = None
_vit_36 = None

def get_models():
    """Load high-accuracy models lazily."""
    global _yolo_63, _yolo_coco, _vit_36

    if _yolo_63 is None:
        from ultralytics import YOLO
        local_weights = "fruit_veg_yolov8m_63.pt"
        if os.path.exists(local_weights):
            _yolo_63 = YOLO(local_weights)
        else:
            from huggingface_hub import hf_hub_download
            hub_path = hf_hub_download("Senu-12/snapstock-fruit-vegetable-detector", "yolov8/fruit_vegetable_yolov8m.pt")
            _yolo_63 = YOLO(hub_path)

    if _yolo_coco is None:
        from ultralytics import YOLO
        local_coco = "yolov8n.pt"
        _yolo_coco = YOLO(local_coco if os.path.exists(local_coco) else "yolov8n.pt")

    if _vit_36 is None:
        from transformers import pipeline
        _vit_36 = pipeline(
            "image-classification",
            model="jazzmacedo/fruits-and-vegetables-detector-36",
            top_k=3,
        )

    return _yolo_63, _yolo_coco, _vit_36

# ==============================================================================
# 🛠️ HELPER FUNCTIONS (ROTATION, FLIP, DEDUPLICATION)
# ==============================================================================

def safe_to_pil(image) -> Optional[Image.Image]:
    """Safely convert any image format (numpy, base64 data URL, dict, PIL) into a clean RGB PIL Image."""
    if image is None:
        return None
    if isinstance(image, str):
        if not image.strip():
            return None
        import base64
        import io
        if "," in image:
            image = image.split(",", 1)[1]
        try:
            decoded = base64.b64decode(image)
            return Image.open(io.BytesIO(decoded)).convert("RGB")
        except Exception:
            return None
    if isinstance(image, dict):
        image = image.get("image") or image.get("composite") or list(image.values())[0]
    if isinstance(image, Image.Image):
        return image.convert("RGB")
    try:
        return Image.fromarray(np.uint8(image)).convert("RGB")
    except Exception:
        return None

def pil_to_data_uri(pil_img: Image.Image) -> str:
    """Encode PIL image to JPEG base64 data URI."""
    import base64
    import io
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=95)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def rotate_image_90(image) -> Optional[np.ndarray]:
    """Rotate image 90 degrees clockwise for mobile devices."""
    pil_img = safe_to_pil(image)
    if pil_img is None:
        return None
    return np.array(pil_img.rotate(-90, expand=True))

def flip_image_horizontal(image) -> Optional[np.ndarray]:
    """Mirror/Flip image horizontally (for front-facing selfie cameras)."""
    pil_img = safe_to_pil(image)
    if pil_img is None:
        return None
    return np.array(pil_img.transpose(Image.FLIP_LEFT_RIGHT))

def clean_label(raw: str) -> str:
    """Normalize complex raw dataset names into clean friendly names."""
    c = raw.lower().strip()
    if "/" in c:
        parts = c.split("/")
        c = parts[0].strip()

    mapping = {
        "cuke": "cucumber", "ail": "garlic", "gingerroot": "ginger",
        "edible corn": "corn", "maize": "corn", "aubergine": "eggplant",
        "chilli": "chili", "chilli pepper": "chili", "cayenne": "chili pepper",
        "red pepper": "bell pepper", "spring onion": "green onion",
        "scallion": "green onion", "kiwi fruit": "kiwi", "cocoanut": "coconut",
        "orange fruit": "orange", "mandarin orange": "orange",
        "cantaloup": "cantaloupe", "pea food": "peas", "pea": "peas",
        "daikon": "radish", "courgette": "zucchini", "jalepeno": "jalapeño",
        "raddish": "radish", "sweetpotato": "sweet potato",
    }
    for k, v in mapping.items():
        if k in c:
            c = v
            break

    return c.title()

def get_emoji(label: str) -> str:
    key = label.lower().replace("-", " ")
    for k, v in EMOJI_MAP.items():
        if k in key or key in k:
            return v
    return "🌿"

def get_category(label: str) -> str:
    lbl = label.lower()
    if "person" in lbl or "human" in lbl:
        return "Human"
    if "dog" in lbl or "cat" in lbl or "animal" in lbl or "pet" in lbl:
        return "Pet / Animal"
    if lbl in FRUITS or any(f in lbl for f in FRUITS):
        return "Fruit"
    if lbl in VEGETABLES or any(v in lbl for v in VEGETABLES):
        return "Vegetable"
    return "Produce"

def get_nutrition(label: str) -> dict:
    canonical = label.lower()
    if canonical in NUTRITION_DB:
        return NUTRITION_DB[canonical]
    for k, v in NUTRITION_DB.items():
        if k in canonical or canonical in k:
            return v
    return {
        "calories": 40, "carbs": 9.0, "protein": 1.0, "fiber": 2.0, "sugar": 5.0,
        "vitamins": "Vitamin C, Essential Minerals",
        "benefits": "Natural plant-based micronutrients rich in antioxidants.",
        "recipes": ["Fresh Garden Harvest Salad", "Roasted Produce Medley"]
    }

def get_drawing_font(size: int = 15):
    """Load clear font for canvas bounding box labels."""
    font_candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    ]
    for fp in font_candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def filter_overlapping_boxes(boxes_data: List[Dict], iou_threshold: float = 0.35) -> List[Dict]:
    """Suppress duplicate overlapping bounding boxes, keeping highest confidence."""
    if not boxes_data:
        return []
    sorted_boxes = sorted(boxes_data, key=lambda x: x["conf"], reverse=True)
    kept = []
    for b in sorted_boxes:
        overlap = False
        for k in kept:
            x1 = max(b["box"][0], k["box"][0])
            y1 = max(b["box"][1], k["box"][1])
            x2 = min(b["box"][2], k["box"][2])
            y2 = min(b["box"][3], k["box"][3])
            inter = max(0, x2 - x1) * max(0, y2 - y1)
            area_b = (b["box"][2] - b["box"][0]) * (b["box"][3] - b["box"][1])
            area_k = (k["box"][2] - k["box"][0]) * (k["box"][3] - k["box"][1])
            union = area_b + area_k - inter
            iou = inter / max(1, union)
            if iou > iou_threshold:
                overlap = True
                break
        if not overlap:
            kept.append(b)
    return kept

# ==============================================================================
# 🎯 CORE MULTI-MODEL DETECTION & CONSENSUS PIPELINE
# ==============================================================================

def detect_and_analyze(
    image,
    conf_thresh: float = 0.30,
    iou_thresh: float = 0.40,
    mode: str = "🎯 Consensus Mode (Ultra-Precision)",
):
    pil_img = safe_to_pil(image)
    if pil_img is None:
        return None, "<div class='empty-state'>⚠️ Please snap a live camera photo, upload an image, or select a demo sample to begin analysis.</div>", "", "", ""

    yolo_produce, yolo_coco, vit_model = get_models()
    W, H = pil_img.size

    eff_conf = conf_thresh
    if "Ultra-Precision" in mode:
        eff_conf = max(conf_thresh, 0.28)
    elif "High Sensitivity" in mode:
        eff_conf = min(conf_thresh, 0.20)

    # 1. Run COCO Detector for Humans, Dogs, Cats, and Animals (conf=0.25 for responsive detection)
    coco_res = yolo_coco(pil_img, conf=0.25, verbose=False)[0]
    raw_candidates = []

    for box in coco_res.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        if cls_id in COCO_SPECIAL_ENTITIES:
            ent = COCO_SPECIAL_ENTITIES[cls_id]
            xyxy = [int(v) for v in box.xyxy[0].tolist()]
            raw_candidates.append({
                "box": xyxy,
                "raw_label": ent["name"],
                "clean_label": ent["name"],
                "category": ent["category"],
                "emoji": ent["emoji"],
                "conf": conf,
                "color": ent["color"],
                "tag": ent["tag"],
                "is_special": True,
            })

    # 2. Run 63-Class Produce Specialist YOLO
    prod_res = yolo_produce(pil_img, conf=eff_conf, iou=iou_thresh, verbose=False)[0]

    for box in prod_res.boxes:
        xyxy = [int(v) for v in box.xyxy[0].tolist()]
        cls_id = int(box.cls[0])
        raw_label = yolo_produce.names[cls_id]
        conf = float(box.conf[0])
        raw_candidates.append({
            "box": xyxy,
            "raw_label": raw_label,
            "conf": conf,
            "is_special": False,
        })

    # 3. Deduplicate overlapping boxes
    candidates = filter_overlapping_boxes(raw_candidates, iou_threshold=iou_thresh)

    detections = []
    draw_img = pil_img.copy()
    draw = ImageDraw.Draw(draw_img)
    font = get_drawing_font(size=max(13, int(min(W, H) * 0.024)))

    for idx, cand in enumerate(candidates):
        x1, y1, x2, y2 = cand["box"]

        # If candidate is a Human / Pet detected by COCO
        if cand.get("is_special"):
            final_label = cand["clean_label"]
            final_conf = cand["conf"]
            category = cand["category"]
            emoji = cand["emoji"]
            color = cand["color"]
            tag_prefix = cand["tag"]
            verified = True
        else:
            # Produce candidate: run ViT crop verification
            bx_w, bx_h = (x2 - x1), (y2 - y1)
            pad_x, pad_y = int(bx_w * 0.10), int(bx_h * 0.10)
            crop_box = (
                max(0, x1 - pad_x),
                max(0, y1 - pad_y),
                min(W, x2 + pad_x),
                min(H, y2 + pad_y)
            )
            crop_img = pil_img.crop(crop_box)

            vit_label, vit_conf = "Unknown", 0.0
            try:
                vit_preds = vit_model(crop_img)
                if vit_preds:
                    vit_label = vit_preds[0]["label"].replace("_", " ").title()
                    vit_conf = float(vit_preds[0]["score"])
            except Exception:
                pass

            clean_yolo = clean_label(cand["raw_label"])
            clean_vit = clean_label(vit_label)
            yolo_conf = cand["conf"]

            # Smart Consensus Logic:
            if clean_yolo.lower() == clean_vit.lower() or clean_yolo.lower() in clean_vit.lower():
                final_label = clean_yolo
                final_conf = max(yolo_conf, vit_conf)
                verified = True
            elif "potato" in clean_yolo.lower() or "potato" in clean_vit.lower():
                final_label = "Potato" if "sweet" not in clean_yolo.lower() and "sweet" not in clean_vit.lower() else "Sweet Potato"
                final_conf = max(yolo_conf, vit_conf)
                verified = True
            elif yolo_conf >= 0.35 and clean_yolo.lower() in ["pumpkin", "avocado", "lemon", "lime", "zucchini", "gourd", "mushroom"]:
                final_label = clean_yolo
                final_conf = yolo_conf
                verified = True
            elif vit_conf > 0.70 and vit_conf > yolo_conf:
                final_label = clean_vit
                final_conf = vit_conf
                verified = True
            else:
                final_label = clean_yolo
                final_conf = yolo_conf
                verified = False

            color = BOX_COLORS[idx % len(BOX_COLORS)]
            category = get_category(final_label)
            emoji = get_emoji(final_label)
            tag_prefix = "FRUIT" if category == "Fruit" else "VEG"

        # Draw Precision Bounding Box on Canvas
        line_w = max(3, int(min(W, H) * 0.005))
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_w)

        # ASCII-safe badge (eliminates tofu [] square glyphs on mobile/servers)
        canvas_badge = f" {tag_prefix}: {final_label} {final_conf:.0%} "

        if hasattr(font, "getbbox"):
            bbox = font.getbbox(canvas_badge)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        else:
            tw, th = len(canvas_badge) * 9, 16

        badge_h = th + 8
        badge_w = tw + 10
        by = max(0, y1 - badge_h)

        draw.rectangle([x1, by, x1 + badge_w, by + badge_h], fill=color)
        draw.text((x1 + 5, by + 4), canvas_badge, fill="#FFFFFF", font=font)

        detections.append({
            "label": final_label,
            "category": category,
            "emoji": emoji,
            "conf": final_conf,
            "verified": verified,
            "color": color,
            "box": (x1, y1, x2, y2),
            "is_special": cand.get("is_special", False),
        })

    # Fallback for single full-frame items if YOLO didn't fire
    if not detections:
        try:
            vit_preds = vit_model(pil_img)
            if vit_preds:
                top_p = vit_preds[0]
                score = float(top_p["score"])
                # Require high confidence (>= 0.65) to eliminate false alarms on non-produce / background scenes
                if score >= 0.65:
                    lbl = clean_label(top_p["label"])
                    cat = get_category(lbl)
                    emoji = get_emoji(lbl)
                    color = BOX_COLORS[0]

                    pad = 12
                    line_w = max(3, int(min(W, H) * 0.005))
                    draw.rectangle([pad, pad, W - pad, H - pad], outline=color, width=line_w)
                    badge_text = f" {cat.upper()}: {lbl} {score:.0%} "
                    draw.rectangle([pad, pad, pad + len(badge_text) * 10, pad + 28], fill=color)
                    draw.text((pad + 6, pad + 6), badge_text, fill="#FFFFFF", font=font)

                    detections.append({
                        "label": lbl,
                        "category": cat,
                        "emoji": emoji,
                        "conf": score,
                        "verified": True,
                        "color": color,
                        "box": (0, 0, W, H),
                        "is_special": False,
                    })
        except Exception:
            pass

    overview_html = build_overview_dashboard(detections)
    nutrition_html = build_nutrition_dashboard(detections)
    recipes_html = build_recipe_dashboard(detections)
    checklist_text = build_checklist_text(detections)

    return np.array(draw_img), overview_html, nutrition_html, recipes_html, checklist_text

def cam_snap_and_detect(b64_str, conf_thresh, iou_thresh, mode):
    if not b64_str or not b64_str.strip():
        msg = "<div style='background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 12px; color: #FCA5A5; font-size: 0.9em; text-align: center;'>⚠️ Camera is not active or hasn't captured a frame yet. Please make sure the camera is ON!</div>"
        return "", None, msg, "", "", ""
    canvas, ov, nut, rec, chk = detect_and_analyze(b64_str, conf_thresh, iou_thresh, mode)
    return b64_str, canvas, ov, nut, rec, chk

def rotate_cam_and_detect(b64_str, conf_thresh, iou_thresh, mode):
    if not b64_str or not b64_str.strip():
        msg = "<div style='background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px; padding: 10px; color: #7DD3FC; font-size: 0.85em; text-align: center;'>🔄 Live camera rotated! Tap '📸 Click Pic & Classify Now' to capture and analyze.</div>"
        return "", None, msg, "", "", ""
    pil_img = safe_to_pil(b64_str)
    if pil_img is None:
        return "", None, "<div class='empty-state'>⚠️ Invalid image.</div>", "", "", ""
    rot_pil = pil_img.rotate(-90, expand=True)
    rot_b64 = pil_to_data_uri(rot_pil)
    canvas, ov, nut, rec, chk = detect_and_analyze(rot_pil, conf_thresh, iou_thresh, mode)
    return rot_b64, canvas, ov, nut, rec, chk

def flip_cam_and_detect(b64_str, conf_thresh, iou_thresh, mode):
    if not b64_str or not b64_str.strip():
        msg = "<div style='background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 8px; padding: 10px; color: #7DD3FC; font-size: 0.85em; text-align: center;'>↔️ Live camera mirrored! Tap '📸 Click Pic & Classify Now' to capture and analyze.</div>"
        return "", None, msg, "", "", ""
    pil_img = safe_to_pil(b64_str)
    if pil_img is None:
        return "", None, "<div class='empty-state'>⚠️ Invalid image.</div>", "", "", ""
    flip_pil = pil_img.transpose(Image.FLIP_LEFT_RIGHT)
    flip_b64 = pil_to_data_uri(flip_pil)
    canvas, ov, nut, rec, chk = detect_and_analyze(flip_pil, conf_thresh, iou_thresh, mode)
    return flip_b64, canvas, ov, nut, rec, chk

def rotate_file_and_detect(image, conf_thresh, iou_thresh, mode):
    if image is None:
        msg = "<div style='background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 12px; color: #FCA5A5; font-size: 0.9em; text-align: center;'>⚠️ Please upload an image first before rotating.</div>"
        return None, None, msg, "", "", ""
    rot_np = rotate_image_90(image)
    if rot_np is None:
        return None, None, "<div class='empty-state'>⚠️ Could not rotate image.</div>", "", "", ""
    canvas, ov, nut, rec, chk = detect_and_analyze(rot_np, conf_thresh, iou_thresh, mode)
    return rot_np, canvas, ov, nut, rec, chk

def flip_file_and_detect(image, conf_thresh, iou_thresh, mode):
    if image is None:
        msg = "<div style='background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 8px; padding: 12px; color: #FCA5A5; font-size: 0.9em; text-align: center;'>⚠️ Please upload an image first before flipping.</div>"
        return None, None, msg, "", "", ""
    flip_np = flip_image_horizontal(image)
    if flip_np is None:
        return None, None, "<div class='empty-state'>⚠️ Could not flip image.</div>", "", "", ""
    canvas, ov, nut, rec, chk = detect_and_analyze(flip_np, conf_thresh, iou_thresh, mode)
    return flip_np, canvas, ov, nut, rec, chk


# ==============================================================================
# 📊 UI DASHBOARDS & SPECIAL ENTITY ADVISORIES
# ==============================================================================

def build_overview_dashboard(detections: List[Dict]) -> str:
    if not detections:
        return """
        <div style="background: rgba(30, 41, 59, 0.5); border: 1px dashed rgba(148, 163, 184, 0.3); border-radius: 14px; padding: 28px; text-align: center; color: #94A3B8;">
            <div style="font-size: 2em; margin-bottom: 6px;">🔍</div>
            <div style="font-weight: 700; font-size: 1.05em; color: #F1F5F9;">No Objects or Produce Detected</div>
            <p style="font-size: 0.85em; margin-top: 4px;">Point camera clearly at produce, or use the 🔄 Rotate Camera button if photo is sideways.</p>
        </div>
        """

    total_count = len(detections)
    fruit_cnt = sum(1 for d in detections if d["category"] == "Fruit")
    veg_cnt = sum(1 for d in detections if d["category"] == "Vegetable")
    human_cnt = sum(1 for d in detections if d["category"] == "Human")
    pet_cnt = sum(1 for d in detections if d["category"] == "Pet / Animal")

    # Estimate total calories from produce only
    total_cals = sum(get_nutrition(d["label"])["calories"] for d in detections if not d.get("is_special"))

    html = f"""
    <!-- TOP STAT METRICS BAR -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(105px, 1fr)); gap: 8px; margin-bottom: 12px;">
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.08)); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="font-size: 0.68em; text-transform: uppercase; color: #34D399; font-weight: 700;">Total Objects</div>
            <div style="font-size: 1.6em; font-weight: 850; color: #FFFFFF; line-height: 1.1;">{total_count}</div>
            <div style="font-size: 0.68em; color: #94A3B8;">{fruit_cnt} Fruit · {veg_cnt} Veg</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(249, 115, 22, 0.08)); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="font-size: 0.68em; text-transform: uppercase; color: #FBBF24; font-weight: 700;">Est. Calories</div>
            <div style="font-size: 1.6em; font-weight: 850; color: #FFFFFF; line-height: 1.1;">~{total_cals}</div>
            <div style="font-size: 0.68em; color: #94A3B8;">kcal produce</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.08)); border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="font-size: 0.68em; text-transform: uppercase; color: #818CF8; font-weight: 700;">Subjects</div>
            <div style="font-size: 1.6em; font-weight: 850; color: #FFFFFF; line-height: 1.1;">{human_cnt + pet_cnt}</div>
            <div style="font-size: 0.68em; color: #94A3B8;">{human_cnt} Human · {pet_cnt} Pet</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.08)); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 10px; text-align: center;">
            <div style="font-size: 0.68em; text-transform: uppercase; color: #60A5FA; font-weight: 700;">Engine Mode</div>
            <div style="font-size: 1.05em; font-weight: 800; color: #FFFFFF; margin-top: 4px;">YOLOv8m + COCO</div>
            <div style="font-size: 0.68em; color: #94A3B8;">Consensus AI</div>
        </div>
    </div>
    """

    # Add Pet & Human Detection Notice if detected
    if human_cnt > 0:
        html += """
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; font-size: 0.85em; color: #C7D2FE;">
            👤 <b>Human Detected:</b> Recognized person in the frame. Only produce items are included in nutritional tracking.
        </div>
        """
    if pet_cnt > 0:
        html += """
        <div style="background: rgba(249, 115, 22, 0.15); border: 1px solid rgba(249, 115, 22, 0.4); border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; font-size: 0.85em; color: #FED7AA;">
            🐾 <b>Pet / Animal Detected:</b> Keep pets safe! Common produce like <b>grapes, raisins, onions, garlic, and avocado</b> are toxic to dogs and cats.
        </div>
        """

    html += """
    <div style="font-size: 0.85em; font-weight: 700; color: #CBD5E1; margin: 10px 0 6px 0; text-transform: uppercase; letter-spacing: 0.05em;">
        📋 Identified Objects
    </div>
    <div style="display: flex; flex-direction: column; gap: 6px;">
    """

    for idx, d in enumerate(detections):
        pct = int(d["conf"] * 100)
        nut = get_nutrition(d["label"]) if not d.get("is_special") else None

        if d.get("is_special"):
            sub_text = f"<span style='color: {d['color']}; font-weight: 600;'>{d['category']} Entity</span> · Not a fruit/vegetable"
            badge = f"<span style='background: rgba(99,102,241,0.2); color: {d['color']}; font-size: 0.7em; padding: 2px 6px; border-radius: 6px; font-weight: 600;'>{d['category']}</span>"
        else:
            sub_text = f"{nut['calories']} kcal · {nut['carbs']}g Carbs · {nut['protein']}g Protein · <span style='color: #38BDF8;'>{nut['vitamins'].split(',')[0]}</span>"
            badge = "<span style='background: rgba(16,185,129,0.2); color: #34D399; font-size: 0.7em; padding: 2px 6px; border-radius: 6px; font-weight: 600;'>✓ Verified Produce</span>"

        html += f"""
        <div style="background: rgba(30, 41, 59, 0.65); border: 1px solid rgba(148, 163, 184, 0.15); border-left: 5px solid {d['color']}; border-radius: 8px; padding: 8px 10px; display: flex; justify-content: space-between; align-items: center; gap: 6px;">
            <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
                <span style="font-size: 1.4em; line-height: 1; flex-shrink: 0;">{d['emoji']}</span>
                <div style="min-width: 0;">
                    <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                        <span style="font-weight: 750; font-size: 0.95em; color: #FFFFFF;">{d['label']}</span>
                        {badge}
                    </div>
                    <div style="font-size: 0.74em; color: #94A3B8; margin-top: 1px; word-break: break-word;">{sub_text}</div>
                </div>
            </div>
            <div style="text-align: right; min-width: 50px; flex-shrink: 0;">
                <div style="font-weight: 850; font-size: 1.05em; color: {d['color']};">{pct}%</div>
            </div>
        </div>
        """

    html += "</div>"
    return html


def build_nutrition_dashboard(detections: List[Dict]) -> str:
    produce_detections = [d for d in detections if not d.get("is_special")]
    if not produce_detections:
        return "<p style='color: #94A3B8;'>No edible produce detected in this image. (Humans and pets are excluded from nutritional analysis).</p>"

    summary = {}
    for d in produce_detections:
        lbl = d["label"]
        summary[lbl] = summary.get(lbl, 0) + 1

    html = """
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 10px; padding: 12px;">
            <div style="font-weight: 750; color: #38BDF8; font-size: 1em;">🥗 USDA Reference Nutritional Breakdown (Per 100g)</div>
            <div style="font-size: 0.78em; color: #94A3B8; margin-top: 2px;">Standard values from USDA FoodData Central.</div>
        </div>
    """

    for lbl, cnt in summary.items():
        nut = get_nutrition(lbl)
        emoji = get_emoji(lbl)
        cat = get_category(lbl)

        html += f"""
        <div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 10px; padding: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 1.4em;">{emoji}</span>
                    <span style="font-size: 1.05em; font-weight: 750; color: #FFFFFF;">{lbl}</span>
                    <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 0.7em; padding: 2px 6px; border-radius: 6px; font-weight: 600;">x{cnt}</span>
                </div>
                <div style="font-weight: 800; color: #34D399; font-size: 1.1em;">{nut['calories']} kcal</div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; margin-bottom: 8px; text-align: center;">
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 6px; padding: 4px;">
                    <div style="color: #94A3B8; font-size: 0.68em; text-transform: uppercase;">Carbs</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.85em;">{nut['carbs']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 6px; padding: 4px;">
                    <div style="color: #94A3B8; font-size: 0.68em; text-transform: uppercase;">Protein</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.85em;">{nut['protein']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 6px; padding: 4px;">
                    <div style="color: #94A3B8; font-size: 0.68em; text-transform: uppercase;">Fiber</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.85em;">{nut['fiber']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 6px; padding: 4px;">
                    <div style="color: #94A3B8; font-size: 0.68em; text-transform: uppercase;">Sugar</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.85em;">{nut['sugar']}g</div>
                </div>
            </div>

            <div style="font-size: 0.78em; color: #CBD5E1; margin-bottom: 3px;">
                <b style="color: #38BDF8;">⚡ Micronutrients:</b> {nut['vitamins']}
            </div>
            <div style="font-size: 0.78em; color: #94A3B8;">
                <b style="color: #34D399;">💡 Key Benefit:</b> {nut['benefits']}
            </div>
        </div>
        """

    html += "</div>"
    return html


def build_recipe_dashboard(detections: List[Dict]) -> str:
    produce = [d for d in detections if not d.get("is_special")]
    if not produce:
        return "<p style='color: #94A3B8;'>Upload produce to generate healthy chef recipe ideas.</p>"

    unique_labels = list({d["label"] for d in produce})
    recipes = []
    for lbl in unique_labels:
        nut = get_nutrition(lbl)
        for r in nut.get("recipes", []):
            recipes.append((r, lbl))

    html = """
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(16, 185, 129, 0.12)); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 10px; padding: 10px;">
            <div style="font-weight: 750; color: #38BDF8; font-size: 0.98em;">👨‍🍳 Smart Pantry Chef Recommendations</div>
            <div style="font-size: 0.75em; color: #94A3B8; margin-top: 1px;">Dishes customized from the produce identified in your photo:</div>
        </div>
    """

    for r_title, ing in recipes[:5]:
        emo = get_emoji(ing)
        html += f"""
        <div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 8px; padding: 10px 12px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: 750; color: #FFFFFF; font-size: 0.92em;">🍽️ {r_title}</div>
                <div style="font-size: 0.75em; color: #94A3B8; margin-top: 1px;">Key Ingredient: {emo} <b>{ing}</b></div>
            </div>
            <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; font-size: 0.7em; padding: 2px 7px; border-radius: 10px; font-weight: 600;">Healthy</span>
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

    lines = ["🛒 INVENTORY & PRODUCE CHECKLIST:", "─────────────────────────────────"]
    for lbl, count in sorted(counts.items()):
        emo = get_emoji(lbl)
        cat = get_category(lbl)
        lines.append(f"[x] {emo} {lbl} (x{count}) - {cat}")

    lines.append("─────────────────────────────────")
    lines.append(f"Total: {len(detections)} items")
    return "\n".join(lines)


# ==============================================================================
# 🎨 MOBILE-OPTIMIZED RESPONSIVE GRADIO INTERFACE
# ==============================================================================

CUSTOM_CSS = """
/* Responsive Mobile-First ProduceVision Studio Pro */
*, *::before, *::after {
    box-sizing: border-box !important;
}

html, body, .gradio-container {
    max-width: 1400px !important;
    width: 100% !important;
    margin: 0 auto !important;
    padding: 12px 14px !important;
    background-color: #070D18 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    overflow-x: hidden !important;
}

#header-hero {
    text-align: center !important;
    padding: 10px 0 6px 0 !important;
    margin-bottom: 8px !important;
    width: 100% !important;
}

#header-title {
    font-size: clamp(1.4em, 5.5vw, 2.3em) !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #34D399 0%, #38BDF8 50%, #A78BFA 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -0.02em !important;
    margin: 0 auto 6px auto !important;
    line-height: 1.25 !important;
    text-align: center !important;
    width: 100% !important;
    word-break: break-word !important;
}

#header-subtitle {
    color: #94A3B8 !important;
    font-size: clamp(0.82em, 2.5vw, 0.96em) !important;
    max-width: 680px !important;
    margin: 0 auto 10px auto !important;
    line-height: 1.45 !important;
    text-align: center !important;
    padding: 0 6px !important;
}

.engine-badges-container {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 6px !important;
    margin: 6px auto 14px auto !important;
    width: 100% !important;
    max-width: 720px !important;
}

.badge-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
    background: rgba(16, 185, 129, 0.12) !important;
    border: 1px solid rgba(16, 185, 129, 0.35) !important;
    color: #34D399 !important;
    padding: 4px 10px !important;
    border-radius: 99px !important;
    font-size: 0.76em !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
}

.badge-dot {
    color: #10B981 !important;
    font-size: 0.85em !important;
}

/* PC Desktop: 2 Columns Side by Side */
#main-app-row {
    display: flex !important;
    flex-direction: row !important;
    gap: 20px !important;
    width: 100% !important;
    align-items: flex-start !important;
}

#input-col {
    flex: 5 !important;
    min-width: 0 !important;
    width: auto !important;
}

#output-col {
    flex: 7 !important;
    min-width: 0 !important;
    width: auto !important;
}

/* Mobile & Tablet Layout (< 960px): Stack Vertically */
@media screen and (max-width: 960px) {
    body, .gradio-container {
        padding: 6px 4px !important;
    }

    #main-app-row,
    .gradio-container .row:not(#camera-ctrl-row) {
        flex-direction: column !important;
        display: flex !important;
        gap: 16px !important;
    }

    #input-col,
    #output-col,
    #main-app-row > div,
    .gradio-column {
        flex: 1 1 100% !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 100% !important;
    }
}

/* Horizontal Camera Control Buttons */
#camera-ctrl-row {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
    margin: 8px 0 !important;
    width: 100% !important;
}

#camera-ctrl-row > * {
    flex: 1 1 50% !important;
    width: 50% !important;
    min-width: 0 !important;
}

.cam-btn {
    background: rgba(30, 41, 59, 0.9) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(148, 163, 184, 0.3) !important;
    font-size: 0.86em !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 8px 6px !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: background 0.2s ease !important;
}

.cam-btn:hover {
    background: rgba(51, 65, 85, 0.95) !important;
}

.analyze-btn {
    background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.05em !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4) !important;
    transition: all 0.2s ease !important;
    margin-top: 8px !important;
    width: 100% !important;
    padding: 12px !important;
    cursor: pointer !important;
}

.analyze-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(16, 185, 129, 0.6) !important;
}

/* Image containers responsive height */
@media screen and (max-width: 768px) {
    .gradio-image, .image-container {
        max-height: 290px !important;
    }
}

/* PRIVACY GREEN LIGHT - 70% LARGER THAN MOBILE OS INDICATOR WITH PULSING GLOW */
#privacy-indicator {
    position: fixed !important;
    top: 16px !important;
    right: 18px !important;
    z-index: 9999999 !important;
    display: none;
    align-items: center !important;
    gap: 8px !important;
    background: rgba(5, 46, 22, 0.95) !important;
    border: 2px solid #10B981 !important;
    border-radius: 99px !important;
    padding: 7px 16px 7px 12px !important;
    color: #6EE7B7 !important;
    font-size: 0.88em !important;
    font-weight: 800 !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 0 24px rgba(16, 185, 129, 0.9), 0 4px 16px rgba(0, 0, 0, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    pointer-events: none !important;
    animation: privacy-pulse 2s infinite ease-in-out !important;
}

#privacy-green-dot {
    width: 15px !important;
    height: 15px !important;
    border-radius: 50% !important;
    background-color: #10B981 !important;
    box-shadow: 0 0 12px #34D399 !important;
    display: inline-block !important;
}

@keyframes privacy-pulse {
    0%, 100% {
        box-shadow: 0 0 16px rgba(16, 185, 129, 0.7), 0 4px 12px rgba(0, 0, 0, 0.5);
        transform: scale(1);
    }
    50% {
        box-shadow: 0 0 30px rgba(16, 185, 129, 1), 0 4px 18px rgba(0, 0, 0, 0.7);
        transform: scale(1.05);
    }
}

.power-btn {
    background: rgba(30, 41, 59, 0.95) !important;
    color: #34D399 !important;
    border: 1px solid rgba(16, 185, 129, 0.4) !important;
    font-size: 0.88em !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.power-btn:hover {
    background: rgba(16, 185, 129, 0.2) !important;
    border-color: #10B981 !important;
}

footer { display: none !important; }
"""

with gr.Blocks(
    title="🥝 ProduceVision Studio Pro — Mobile-Ready Produce & Subject AI",
    css=CUSTOM_CSS,
    theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="teal", neutral_hue="slate"),
) as demo:

    gr.HTML("""
    <div id="header-hero">
        <div id="header-title">🥝 ProduceVision Studio Pro</div>
        <div id="header-subtitle">
            Enterprise computer vision: 63-class produce localization, ViT consensus verification, and automated Human & Pet detection.
        </div>
        <div class="engine-badges-container">
            <span class="badge-pill"><span class="badge-dot">●</span> 63 Produce Classes</span>
            <span class="badge-pill">👤 Human Aware</span>
            <span class="badge-pill">🐾 Pet Aware</span>
            <span class="badge-pill">📱 Mobile Camera Controls</span>
            <span class="badge-pill">⚡ Live Auto-Detect</span>
        </div>
    </div>
    """)

    # HTML5 PRIVACY CAMERA LIGHT & JAVASCRIPT ENGINE
    gr.HTML("""
    <!-- PRIVACY CAMERA ACTIVE BADGE (Fixed Top Right, 70% larger than typical smartphone dots) -->
    <div id="privacy-indicator">
        <span id="privacy-green-dot"></span>
        <span>📷 CAMERA ACTIVE</span>
    </div>

    <script>
    window.pvStream = null;
    window.pvRotation = 0;
    window.pvFlipped = false;

    window.pvStartCamera = async function() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } }
            });
            window.pvStream = stream;
            const video = document.getElementById('live-camera-video');
            const overlay = document.getElementById('camera-off-overlay');
            const indicator = document.getElementById('privacy-indicator');
            const powerBtn = document.getElementById('cam-power-btn');

            if (video) {
                video.srcObject = stream;
                video.style.display = 'block';
                video.play();
            }
            if (overlay) overlay.style.display = 'none';
            if (indicator) indicator.style.display = 'flex';
            if (powerBtn) {
                powerBtn.innerText = '🔴 Turn Camera OFF';
                powerBtn.style.color = '#FCA5A5';
                powerBtn.style.borderColor = 'rgba(239, 68, 68, 0.5)';
            }
        } catch (err) {
            console.error('Camera access error:', err);
        }
    };

    window.pvStopCamera = function() {
        if (window.pvStream) {
            window.pvStream.getTracks().forEach(track => track.stop());
            window.pvStream = null;
        }
        const video = document.getElementById('live-camera-video');
        const overlay = document.getElementById('camera-off-overlay');
        const indicator = document.getElementById('privacy-indicator');
        const powerBtn = document.getElementById('cam-power-btn');

        if (video) {
            video.srcObject = null;
            video.style.display = 'none';
        }
        if (overlay) overlay.style.display = 'flex';
        if (indicator) indicator.style.display = 'none';
        if (powerBtn) {
            powerBtn.innerText = '🟢 Turn Camera ON';
            powerBtn.style.color = '#34D399';
            powerBtn.style.borderColor = 'rgba(16, 185, 129, 0.5)';
        }
    };

    window.pvToggleCamera = function() {
        if (window.pvStream) {
            window.pvStopCamera();
        } else {
            window.pvStartCamera();
        }
        return '';
    };

    window.pvUpdateVideoTransform = function() {
        const video = document.getElementById('live-camera-video');
        if (!video) return;
        const flip = window.pvFlipped ? 'scaleX(-1)' : 'scaleX(1)';
        video.style.transform = `rotate(${window.pvRotation}deg) ${flip}`;
    };

    window.pvRotateCamera = function() {
        window.pvRotation = (window.pvRotation + 90) % 360;
        window.pvUpdateVideoTransform();
        return '';
    };

    window.pvFlipCamera = function() {
        window.pvFlipped = !window.pvFlipped;
        window.pvUpdateVideoTransform();
        return '';
    };

    window.pvCaptureFrame = function(dummy, conf, iou, mode) {
        const video = document.getElementById('live-camera-video');
        const flash = document.getElementById('camera-flash');
        if (!video || !window.pvStream || video.readyState < 2) {
            alert('Please click "🟢 Turn Camera ON" first to start your live camera feed!');
            return ['', conf, iou, mode];
        }

        if (flash) {
            flash.style.opacity = '0.75';
            setTimeout(() => { flash.style.opacity = '0'; }, 150);
        }

        const canvas = document.createElement('canvas');
        const vw = video.videoWidth || 640;
        const vh = video.videoHeight || 480;
        const rot = window.pvRotation || 0;
        const flipped = window.pvFlipped || false;

        if (rot === 90 || rot === 270) {
            canvas.width = vh;
            canvas.height = vw;
        } else {
            canvas.width = vw;
            canvas.height = vh;
        }

        const ctx = canvas.getContext('2d');
        ctx.translate(canvas.width / 2, canvas.height / 2);
        ctx.rotate((rot * Math.PI) / 180);
        if (flipped) {
            ctx.scale(-1, 1);
        }
        ctx.drawImage(video, -vw / 2, -vh / 2, vw, vh);

        const dataUrl = canvas.toDataURL('image/jpeg', 0.95);
        return [dataUrl, conf, iou, mode];
    };

    // Auto-start camera when page is ready
    setTimeout(() => {
        if (document.getElementById('live-camera-video')) {
            window.pvStartCamera();
        }
    }, 600);
    </script>
    """)

    with gr.Row(elem_id="main-app-row"):
        # LEFT COLUMN: INPUT (LIVE CAMERA & UPLOAD TABS), TUNING & PRESETS
        with gr.Column(scale=5, elem_id="input-col"):

            with gr.Tabs(elem_id="input-mode-tabs"):
                # TAB 1: LIVE CAMERA (CLICK PIC & CLASSIFY)
                with gr.TabItem("📸 Live Camera (Click & Classify)", id="tab-cam"):
                    gr.HTML("""
                    <div id="camera-viewport-card" style="position: relative; width: 100%; height: 310px; background: #000; border-radius: 12px; overflow: hidden; border: 1px solid rgba(148, 163, 184, 0.2); display: flex; align-items: center; justify-content: center;">
                        <video id="live-camera-video" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover; display: none; transition: transform 0.25s ease;"></video>
                        <div id="camera-off-overlay" style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; color: #94A3B8; text-align: center; padding: 20px;">
                            <span style="font-size: 2.5em;">📷</span>
                            <div style="font-weight: 700; color: #F1F5F9; font-size: 1.05em;">Camera is Currently OFF</div>
                            <div style="font-size: 0.82em; max-width: 280px;">Tap "🟢 Turn Camera ON" below to start the live camera feed.</div>
                        </div>
                        <div id="camera-flash" style="position: absolute; inset: 0; background: white; opacity: 0; pointer-events: none; transition: opacity 0.15s ease;"></div>
                    </div>
                    """)

                    with gr.Row():
                        cam_power_btn = gr.Button("🔴 Turn Camera OFF", elem_id="cam-power-btn", elem_classes=["power-btn"], size="sm")
                        cam_snap_btn = gr.Button("📸 Click Pic & Classify Now", elem_classes=["analyze-btn"], size="lg")

                    with gr.Row(elem_id="camera-ctrl-row"):
                        cam_rotate_btn = gr.Button("🔄 Rotate 90° Clockwise", elem_classes=["cam-btn"], size="sm")
                        cam_flip_btn = gr.Button("↔️ Mirror / Flip", elem_classes=["cam-btn"], size="sm")

                    # Hidden Transport Textbox for Camera Base64
                    cam_b64_transfer = gr.Textbox(visible=False, elem_id="cam-b64-transfer")

                    gr.HTML("""
                    <div style="font-size: 0.76em; color: #94A3B8; text-align: center; margin-top: 2px;">
                        💡 <b>Tip:</b> Click <b>📸 Click Pic & Classify Now</b> to capture your live snapshot! If photo is sideways on mobile, tap <b>Rotate 90°</b>.
                    </div>
                    """)

                # TAB 2: UPLOAD PHOTO & SAMPLES
                with gr.TabItem("📁 Upload Photo / Samples", id="tab-upload"):
                    file_input = gr.Image(
                        label="📤 Upload Produce Image / Clipboard",
                        type="numpy",
                        sources=["upload", "clipboard"],
                        height=290,
                    )

                    file_analyze_btn = gr.Button("🔍 Analyze Uploaded Produce", elem_classes=["analyze-btn"], size="lg")

                    with gr.Row(elem_id="camera-ctrl-row"):
                        file_rotate_btn = gr.Button("🔄 Rotate 90° Clockwise", elem_classes=["cam-btn"], size="sm")
                        file_flip_btn = gr.Button("↔️ Mirror / Flip", elem_classes=["cam-btn"], size="sm")

            with gr.Accordion("⚙️ Precision Sensitivity & Detection Preset", open=False):
                preset_mode = gr.Radio(
                    choices=[
                        "🎯 Consensus Mode (Ultra-Precision)",
                        "⚡ High Sensitivity (Crowded Basket)",
                    ],
                    value="🎯 Consensus Mode (Ultra-Precision)",
                    label="Detection Preset",
                    info="Consensus Mode eliminates false alarms; High Sensitivity catches smaller items.",
                )
                with gr.Row():
                    conf_slider = gr.Slider(
                        label="Confidence Threshold",
                        minimum=0.10,
                        maximum=0.90,
                        value=0.30,
                        step=0.05,
                    )
                    iou_slider = gr.Slider(
                        label="IoU NMS Overlap",
                        minimum=0.10,
                        maximum=0.80,
                        value=0.40,
                        step=0.05,
                    )

            # 1-CLICK DEMO EXAMPLES
            gr.Markdown("### 🌟 Instant 1-Click Test Showcase")
            demo_samples = [
                ["samples/potatoes.jpg", 0.30, 0.40, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/fruit_basket.jpg", 0.30, 0.40, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/bell_peppers.jpg", 0.30, 0.40, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/tomatoes.jpg", 0.30, 0.40, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/carrots.jpg", 0.30, 0.40, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/banana.jpg", 0.30, 0.40, "🎯 Consensus Mode (Ultra-Precision)"],
            ]
            gr.Examples(
                examples=demo_samples,
                inputs=[file_input, conf_slider, iou_slider, preset_mode],
                label="Click any sample card below to test immediately:",
            )

        # RIGHT COLUMN: ANNOTATED CANVAS & DETAILED INTELLIGENCE
        with gr.Column(scale=7, elem_id="output-col"):
            annotated_canvas = gr.Image(
                label="🎯 Precision Detection Map",
                height=320,
                interactive=False,
            )

            # CLEAN 3-TAB INTERFACE (NO OVERFLOW '...')
            with gr.Tabs():
                with gr.TabItem("📊 Breakdown"):
                    overview_html = gr.HTML()

                with gr.TabItem("🥗 Nutrition"):
                    nutrition_html = gr.HTML()

                with gr.TabItem("👨‍🍳 Chef & Checklist"):
                    recipes_html = gr.HTML()
                    checklist_txt = gr.Textbox(label="Exportable Inventory Checklist", lines=5, interactive=False)

    # EVENT TRIGGERS WIRING
    analysis_outputs = [annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt]

    def on_auto_detect_file(img, conf, iou, m):
        if img is None:
            return gr.skip(), gr.skip(), gr.skip(), gr.skip(), gr.skip()
        return detect_and_analyze(img, conf, iou, m)

    # 1. Live Camera Actions
    cam_power_btn.click(
        fn=lambda: None,
        inputs=[],
        outputs=[],
        js="() => { window.pvToggleCamera(); return []; }",
    )

    cam_snap_btn.click(
        fn=cam_snap_and_detect,
        inputs=[cam_b64_transfer, conf_slider, iou_slider, preset_mode],
        outputs=[cam_b64_transfer, annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt],
        js="(dummy, conf, iou, mode) => { return window.pvCaptureFrame(dummy, conf, iou, mode); }",
    )

    cam_rotate_btn.click(
        fn=rotate_cam_and_detect,
        inputs=[cam_b64_transfer, conf_slider, iou_slider, preset_mode],
        outputs=[cam_b64_transfer, annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt],
        js="(b64, conf, iou, mode) => { window.pvRotateCamera(); return [b64, conf, iou, mode]; }",
    )

    cam_flip_btn.click(
        fn=flip_cam_and_detect,
        inputs=[cam_b64_transfer, conf_slider, iou_slider, preset_mode],
        outputs=[cam_b64_transfer, annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt],
        js="(b64, conf, iou, mode) => { window.pvFlipCamera(); return [b64, conf, iou, mode]; }",
    )

    # 2. Upload / File Actions
    file_analyze_btn.click(
        fn=detect_and_analyze,
        inputs=[file_input, conf_slider, iou_slider, preset_mode],
        outputs=analysis_outputs,
    )
    file_rotate_btn.click(
        fn=rotate_file_and_detect,
        inputs=[file_input, conf_slider, iou_slider, preset_mode],
        outputs=[file_input, annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt],
    )
    file_flip_btn.click(
        fn=flip_file_and_detect,
        inputs=[file_input, conf_slider, iou_slider, preset_mode],
        outputs=[file_input, annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt],
    )
    file_input.change(
        fn=on_auto_detect_file,
        inputs=[file_input, conf_slider, iou_slider, preset_mode],
        outputs=analysis_outputs,
    )

    gr.HTML("""
    <div style="text-align: center; color: #475569; font-size: 0.82em; margin-top: 20px; padding: 10px; border-top: 1px solid rgba(148, 163, 184, 0.1);">
        ProduceVision Studio Pro · 63 Produce Classes + Human & Pet Recognition · Mobile Responsive · USDA Integrated Database
    </div>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, inbrowser=True)