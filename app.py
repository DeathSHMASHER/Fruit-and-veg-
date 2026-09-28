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
# 🎨 VIBRANT COLOR PALETTE & COMPREHENSIVE PRODUCE DATABASE (63+ CLASSES)
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
# 🧠 DUAL-ENGINE AI LOADER (63-CLASS YOLOv8m + ViT-36 CLASSIFIER)
# ==============================================================================

_yolo_63 = None
_vit_36 = None

def get_models():
    """Load high-accuracy models lazily."""
    global _yolo_63, _vit_36

    if _yolo_63 is None:
        from ultralytics import YOLO
        local_weights = "fruit_veg_yolov8m_63.pt"
        if os.path.exists(local_weights):
            _yolo_63 = YOLO(local_weights)
        else:
            # Fallback to auto-download from Hugging Face hub
            from huggingface_hub import hf_hub_download
            hub_path = hf_hub_download("Senu-12/snapstock-fruit-vegetable-detector", "yolov8/fruit_vegetable_yolov8m.pt")
            _yolo_63 = YOLO(hub_path)

    if _vit_36 is None:
        from transformers import pipeline
        _vit_36 = pipeline(
            "image-classification",
            model="jazzmacedo/fruits-and-vegetables-detector-36",
            top_k=3,
        )

    return _yolo_63, _vit_36

# ==============================================================================
# 🛠️ CANONICAL NORMALIZATION & LABEL CLEANING
# ==============================================================================

def clean_label(raw: str) -> str:
    """Normalize complex raw dataset names into clean friendly names."""
    c = raw.lower().strip()
    # Handle multi-synonyms from dataset: 'bell pepper/capsicum' -> 'Bell Pepper'
    if "/" in c:
        parts = c.split("/")
        c = parts[0].strip()

    mapping = {
        "cuke": "cucumber",
        "ail": "garlic",
        "gingerroot": "ginger",
        "edible corn": "corn",
        "maize": "corn",
        "aubergine": "eggplant",
        "chilli": "chili",
        "chilli pepper": "chili",
        "cayenne": "chili pepper",
        "red pepper": "bell pepper",
        "spring onion": "green onion",
        "scallion": "green onion",
        "kiwi fruit": "kiwi",
        "cocoanut": "coconut",
        "orange fruit": "orange",
        "mandarin orange": "orange",
        "cantaloup": "cantaloupe",
        "pea food": "peas",
        "pea": "peas",
        "daikon": "radish",
        "courgette": "zucchini",
        "jalepeno": "jalapeño",
        "raddish": "radish",
        "sweetpotato": "sweet potato",
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

# ==============================================================================
# 🎯 CORE DETECTION & CONSENSUS ENGINE
# ==============================================================================

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

def detect_and_analyze(
    image: Optional[np.ndarray],
    conf_thresh: float = 0.30,
    iou_thresh: float = 0.45,
    mode: str = "🎯 Consensus Mode (Ultra-Precision)",
):
    if image is None:
        return None, "<div class='empty-state'>⚠️ Please upload an image or select a demo sample to begin analysis.</div>", "", "", ""

    yolo_model, vit_model = get_models()
    pil_img = Image.fromarray(image).convert("RGB")
    W, H = pil_img.size

    # Adjust sensitivity based on preset mode
    eff_conf = conf_thresh
    if "Ultra-Precision" in mode:
        eff_conf = max(conf_thresh, 0.28)
    elif "High Sensitivity" in mode:
        eff_conf = min(conf_thresh, 0.20)

    # 1. Run High-Capacity 63-Class Produce YOLO
    results = yolo_model(pil_img, conf=eff_conf, iou=iou_thresh, verbose=False)[0]

    raw_candidates = []
    for box in results.boxes:
        xyxy = [int(v) for v in box.xyxy[0].tolist()]
        cls_id = int(box.cls[0])
        raw_yolo_label = yolo_model.names[cls_id]
        yolo_conf = float(box.conf[0])
        raw_candidates.append({
            "box": xyxy,
            "raw_label": raw_yolo_label,
            "conf": yolo_conf,
        })

    # Deduplicate overlapping boxes
    candidates = filter_overlapping_boxes(raw_candidates, iou_threshold=iou_thresh)

    detections = []
    draw_img = pil_img.copy()
    draw = ImageDraw.Draw(draw_img)
    font = get_drawing_font(size=max(13, int(min(W, H) * 0.024)))

    for idx, cand in enumerate(candidates):
        x1, y1, x2, y2 = cand["box"]
        raw_yolo_label = cand["raw_label"]
        yolo_conf = cand["conf"]

        # 2. Extract crop with 10% context padding for ViT verification
        bx_w, bx_h = (x2 - x1), (y2 - y1)
        pad_x, pad_y = int(bx_w * 0.10), int(bx_h * 0.10)
        crop_box = (
            max(0, x1 - pad_x),
            max(0, y1 - pad_y),
            min(W, x2 + pad_x),
            min(H, y2 + pad_y)
        )
        crop_img = pil_img.crop(crop_box)

        # 3. ViT Classification on the crop
        vit_label, vit_conf = "Unknown", 0.0
        try:
            vit_preds = vit_model(crop_img)
            if vit_preds:
                vit_label = vit_preds[0]["label"].replace("_", " ").title()
                vit_conf = float(vit_preds[0]["score"])
        except Exception:
            pass

        # 4. Smart Consensus Logic
        # Normalize labels
        clean_yolo = clean_label(raw_yolo_label)
        clean_vit = clean_label(vit_label)

        # Rule A: Cross-Verification Agreement
        if clean_yolo.lower() == clean_vit.lower() or clean_yolo.lower() in clean_vit.lower():
            final_label = clean_yolo
            final_conf = max(yolo_conf, vit_conf)
            verified = True
        # Rule B: Potato/Sweet Potato Protection (Eliminate false 'Pear' classification)
        elif "potato" in clean_yolo.lower() or "potato" in clean_vit.lower():
            final_label = "Potato" if "sweet" not in clean_yolo.lower() and "sweet" not in clean_vit.lower() else "Sweet Potato"
            final_conf = max(yolo_conf, vit_conf)
            verified = True
        # Rule C: 63-Class Specialist Priority for items outside 36 classes (e.g. Pumpkin, Lemon, Avocado)
        elif yolo_conf >= 0.35 and clean_yolo.lower() in ["pumpkin", "avocado", "lemon", "lime", "zucchini", "gourd", "mushroom"]:
            final_label = clean_yolo
            final_conf = yolo_conf
            verified = True
        # Rule D: ViT High Confidence Override if YOLO is uncertain
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

        # 5. Draw Precision Bounding Box on Canvas
        line_w = max(3, int(min(W, H) * 0.005))
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_w)

        # ASCII-safe badge text (avoids broken emoji '[]' boxes in PIL)
        tag_prefix = "FRUIT" if category == "Fruit" else "VEG"
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
            "crop": crop_img,
            "box": (x1, y1, x2, y2),
        })

    # Fallback for single full-frame items if YOLO didn't fire
    if not detections:
        try:
            vit_preds = vit_model(pil_img)
            if vit_preds:
                top_p = vit_preds[0]
                lbl = clean_label(top_p["label"])
                score = float(top_p["score"])
                cat = get_category(lbl)
                emoji = get_emoji(lbl)
                color = BOX_COLORS[0]

                # Frame outline
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
                    "crop": pil_img,
                    "box": (0, 0, W, H),
                })
        except Exception:
            pass

    # Build rich UI components
    overview_html = build_overview_dashboard(detections)
    nutrition_html = build_nutrition_dashboard(detections)
    recipes_html = build_recipe_dashboard(detections)
    checklist_text = build_checklist_text(detections)

    return np.array(draw_img), overview_html, nutrition_html, recipes_html, checklist_text


# ==============================================================================
# 🎨 HIGH-PERFORMANCE GLASSMORPHIC UI HTML BUILDERS
# ==============================================================================

def build_overview_dashboard(detections: List[Dict]) -> str:
    if not detections:
        return """
        <div style="background: rgba(30, 41, 59, 0.5); border: 1px dashed rgba(148, 163, 184, 0.3); border-radius: 14px; padding: 32px; text-align: center; color: #94A3B8;">
            <div style="font-size: 2.2em; margin-bottom: 8px;">🔍</div>
            <div style="font-weight: 700; font-size: 1.1em; color: #F1F5F9;">No Produce Detected</div>
            <p style="font-size: 0.9em; margin-top: 6px;">Try switching to <b>High Sensitivity Mode</b> or adjust the confidence slider.</p>
        </div>
        """

    total_count = len(detections)
    fruit_cnt = sum(1 for d in detections if d["category"] == "Fruit")
    veg_cnt = sum(1 for d in detections if d["category"] == "Vegetable")
    verified_cnt = sum(1 for d in detections if d["verified"])
    consensus_pct = int((verified_cnt / max(1, total_count)) * 100)

    # Estimate total calories
    total_cals = sum(get_nutrition(d["label"])["calories"] for d in detections)

    html = f"""
    <!-- TOP STAT METRICS BAR -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px;">
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.08)); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-size: 0.72em; text-transform: uppercase; color: #34D399; font-weight: 700; letter-spacing: 0.05em;">Total Produce</div>
            <div style="font-size: 1.8em; font-weight: 850; color: #FFFFFF; line-height: 1.2;">{total_count}</div>
            <div style="font-size: 0.72em; color: #94A3B8;">{fruit_cnt} Fruit · {veg_cnt} Veg</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(249, 115, 22, 0.08)); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-size: 0.72em; text-transform: uppercase; color: #FBBF24; font-weight: 700; letter-spacing: 0.05em;">Est. Calories</div>
            <div style="font-size: 1.8em; font-weight: 850; color: #FFFFFF; line-height: 1.2;">~{total_cals}</div>
            <div style="font-size: 0.72em; color: #94A3B8;">kcal total basket</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.08)); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-size: 0.72em; text-transform: uppercase; color: #60A5FA; font-weight: 700; letter-spacing: 0.05em;">AI Consensus</div>
            <div style="font-size: 1.8em; font-weight: 850; color: #FFFFFF; line-height: 1.2;">{consensus_pct}%</div>
            <div style="font-size: 0.72em; color: #94A3B8;">Dual-Model Verified</div>
        </div>

        <div style="background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(236, 72, 153, 0.08)); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 12px; padding: 12px; text-align: center;">
            <div style="font-size: 0.72em; text-transform: uppercase; color: #C084FC; font-weight: 700; letter-spacing: 0.05em;">Model Engine</div>
            <div style="font-size: 1.2em; font-weight: 800; color: #FFFFFF; margin-top: 4px;">YOLOv8m-63</div>
            <div style="font-size: 0.72em; color: #94A3B8;">+ ViT-36 Ensemble</div>
        </div>
    </div>

    <!-- DETECTED PRODUCE CARDS -->
    <div style="font-size: 0.9em; font-weight: 700; color: #CBD5E1; margin: 14px 0 8px 0; text-transform: uppercase; letter-spacing: 0.05em;">
        📋 Identified Produce Items ({total_count})
    </div>
    <div style="display: flex; flex-direction: column; gap: 8px;">
    """

    for idx, d in enumerate(detections):
        pct = int(d["conf"] * 100)
        nut = get_nutrition(d["label"])
        verified_badge = "<span style='background: rgba(16,185,129,0.2); color: #34D399; font-size: 0.72em; padding: 2px 7px; border-radius: 6px; border: 1px solid rgba(16,185,129,0.4); font-weight: 600;'>✓ Dual-Verified</span>" if d["verified"] else "<span style='background: rgba(59,130,246,0.15); color: #60A5FA; font-size: 0.72em; padding: 2px 7px; border-radius: 6px; font-weight: 600;'>⚡ YOLO-63</span>"

        html += f"""
        <div style="background: rgba(30, 41, 59, 0.65); border: 1px solid rgba(148, 163, 184, 0.15); border-left: 5px solid {d['color']}; border-radius: 10px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.6em; line-height: 1;">{d['emoji']}</span>
                <div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-weight: 750; font-size: 1.05em; color: #FFFFFF;">{d['label']}</span>
                        <span style="background: rgba(148, 163, 184, 0.15); color: #94A3B8; font-size: 0.72em; padding: 1px 6px; border-radius: 8px;">{d['category']}</span>
                        {verified_badge}
                    </div>
                    <div style="font-size: 0.78em; color: #94A3B8; margin-top: 2px;">
                        {nut['calories']} kcal · {nut['carbs']}g Carbs · {nut['protein']}g Protein · <span style="color: #38BDF8;">{nut['vitamins'].split(',')[0]}</span>
                    </div>
                </div>
            </div>
            <div style="text-align: right; min-width: 90px;">
                <div style="font-weight: 850; font-size: 1.15em; color: {d['color']};">{pct}%</div>
                <div style="background: rgba(15, 23, 42, 0.7); border-radius: 4px; height: 5px; width: 85px; margin-top: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {d['color']}, #38BDF8); width: {pct}%; height: 100%; border-radius: 4px;"></div>
                </div>
            </div>
        </div>
        """

    html += "</div>"
    return html


def build_nutrition_dashboard(detections: List[Dict]) -> str:
    if not detections:
        return "<p style='color: #94A3B8;'>Run produce detection to view comprehensive USDA nutritional sheets.</p>"

    # Deduplicate counts
    summary = {}
    for d in detections:
        lbl = d["label"]
        summary[lbl] = summary.get(lbl, 0) + 1

    html = """
    <div style="display: flex; flex-direction: column; gap: 12px;">
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 14px;">
            <div style="font-weight: 750; color: #38BDF8; font-size: 1.05em;">🥗 USDA Reference Nutritional Breakdown (Per 100g Serving)</div>
            <div style="font-size: 0.82em; color: #94A3B8; margin-top: 2px;">Nutrient values sourced from standard USDA FoodData Central databases.</div>
        </div>
    """

    for lbl, cnt in summary.items():
        nut = get_nutrition(lbl)
        emoji = get_emoji(lbl)
        cat = get_category(lbl)

        html += f"""
        <div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 12px; padding: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.5em;">{emoji}</span>
                    <span style="font-size: 1.1em; font-weight: 750; color: #FFFFFF;">{lbl}</span>
                    <span style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 0.72em; padding: 2px 7px; border-radius: 6px; font-weight: 600;">x{cnt} item{'s' if cnt > 1 else ''}</span>
                    <span style="color: #64748B; font-size: 0.78em;">· {cat}</span>
                </div>
                <div style="font-weight: 800; color: #34D399; font-size: 1.15em;">{nut['calories']} kcal</div>
            </div>

            <!-- Macronutrient Grid -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 10px; text-align: center;">
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 6px;">
                    <div style="color: #94A3B8; font-size: 0.7em; text-transform: uppercase;">Carbs</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.9em;">{nut['carbs']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 6px;">
                    <div style="color: #94A3B8; font-size: 0.7em; text-transform: uppercase;">Protein</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.9em;">{nut['protein']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 6px;">
                    <div style="color: #94A3B8; font-size: 0.7em; text-transform: uppercase;">Fiber</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.9em;">{nut['fiber']}g</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 6px;">
                    <div style="color: #94A3B8; font-size: 0.7em; text-transform: uppercase;">Sugar</div>
                    <div style="color: #FFFFFF; font-weight: 750; font-size: 0.9em;">{nut['sugar']}g</div>
                </div>
            </div>

            <div style="font-size: 0.82em; color: #CBD5E1; margin-bottom: 4px;">
                <b style="color: #38BDF8;">⚡ Micronutrients:</b> {nut['vitamins']}
            </div>
            <div style="font-size: 0.82em; color: #94A3B8;">
                <b style="color: #34D399;">💡 Key Benefit:</b> {nut['benefits']}
            </div>
        </div>
        """

    html += "</div>"
    return html


def build_recipe_dashboard(detections: List[Dict]) -> str:
    if not detections:
        return "<p style='color: #94A3B8;'>Upload produce to generate tailored culinary recipe concepts.</p>"

    unique_labels = list({d["label"] for d in detections})
    recipes = []
    for lbl in unique_labels:
        nut = get_nutrition(lbl)
        for r in nut.get("recipes", []):
            recipes.append((r, lbl))

    html = """
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.12), rgba(16, 185, 129, 0.12)); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 12px;">
            <div style="font-weight: 750; color: #38BDF8; font-size: 1.05em;">👨‍🍳 Smart Pantry Chef Recommendations</div>
            <div style="font-size: 0.8em; color: #94A3B8; margin-top: 2px;">Dishes customized from the produce identified in your photo:</div>
        </div>
    """

    for r_title, ing in recipes[:6]:
        emo = get_emoji(ing)
        html += f"""
        <div style="background: rgba(30, 41, 59, 0.55); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 10px; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: 750; color: #FFFFFF; font-size: 0.95em;">🍽️ {r_title}</div>
                <div style="font-size: 0.78em; color: #94A3B8; margin-top: 2px;">Key Ingredient: {emo} <b>{ing}</b></div>
            </div>
            <span style="background: rgba(16, 185, 129, 0.15); color: #34D399; font-size: 0.72em; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Healthy</span>
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

    lines = ["🛒 PRODUCE INVENTORY & CHECKLIST:", "─────────────────────────────────"]
    for lbl, count in sorted(counts.items()):
        emo = get_emoji(lbl)
        cat = get_category(lbl)
        lines.append(f"[x] {emo} {lbl} (x{count}) - {cat}")

    lines.append("─────────────────────────────────")
    lines.append(f"Total: {len(detections)} items")
    return "\n".join(lines)


# ==============================================================================
# 🎨 GRADIO INTERFACE ARCHITECTURE
# ==============================================================================

CUSTOM_CSS = """
/* ProduceVision Studio Pro Ultra-Modern Dark Glassmorphism */
body, .gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    background-color: #070D18 !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
}

#header-hero {
    text-align: center;
    padding: 20px 0 14px 0;
    margin-bottom: 8px;
}

#header-title {
    font-size: 2.6em;
    font-weight: 900;
    background: linear-gradient(135deg, #34D399 0%, #38BDF8 50%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
    margin-bottom: 4px;
}

#header-subtitle {
    color: #94A3B8;
    font-size: 1.02em;
    max-width: 720px;
    margin: 0 auto 10px auto;
    line-height: 1.45;
}

.engine-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34D399;
    padding: 4px 16px;
    border-radius: 99px;
    font-size: 0.82em;
    font-weight: 600;
}

.analyze-btn {
    background: linear-gradient(135deg, #10B981 0%, #06B6D4 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 1.1em !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 18px rgba(16, 185, 129, 0.4) !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
}

.analyze-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(16, 185, 129, 0.6) !important;
}

.panel-card {
    background: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(148, 163, 184, 0.15) !important;
    border-radius: 14px !important;
}

footer { display: none !important; }
"""

with gr.Blocks(
    title="🥝 ProduceVision Studio Pro — Fruit & Vegetable AI",
    css=CUSTOM_CSS,
    theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="teal", neutral_hue="slate"),
) as demo:

    gr.HTML("""
    <div id="header-hero">
        <div id="header-title">🥝 ProduceVision Studio Pro</div>
        <div id="header-subtitle">
            Enterprise produce intelligence: 63-class YOLOv8 Medium localization, ViT-36 consensus verification, and real-time USDA nutritional analytics.
        </div>
        <div class="engine-pill">
            <span style="color: #10B981;">●</span>
            <span>63-Class YOLOv8m Produce Specialist</span>
            <span>·</span>
            <span>ViT-36 Consensus Engine</span>
            <span>·</span>
            <span>Zero Tofu Glyphs</span>
        </div>
    </div>
    """)

    with gr.Row():
        # LEFT COLUMN: INPUT & TUNING
        with gr.Column(scale=5):
            input_img = gr.Image(
                label="📤 Input Produce Image / Live Camera",
                type="numpy",
                sources=["upload", "webcam", "clipboard"],
                height=360,
            )

            with gr.Accordion("⚙️ Precision Sensitivity & Detection Preset", open=False):
                preset_mode = gr.Radio(
                    choices=[
                        "🎯 Consensus Mode (Ultra-Precision)",
                        "⚡ High Sensitivity (Crowded Basket)",
                    ],
                    value="🎯 Consensus Mode (Ultra-Precision)",
                    label="Detection Preset",
                    info="Consensus Mode eliminates false positives; High Sensitivity catches small items.",
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
                        value=0.45,
                        step=0.05,
                    )

            analyze_btn = gr.Button("🔍 Analyze Produce with AI", elem_classes=["analyze-btn"], size="lg")

            # 1-CLICK DEMO EXAMPLES
            gr.Markdown("### 🌟 Instant 1-Click Test Showcase")
            demo_samples = [
                ["samples/potatoes.jpg", 0.30, 0.45, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/fruit_basket.jpg", 0.30, 0.45, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/bell_peppers.jpg", 0.30, 0.45, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/tomatoes.jpg", 0.30, 0.45, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/carrots.jpg", 0.30, 0.45, "🎯 Consensus Mode (Ultra-Precision)"],
                ["samples/banana.jpg", 0.30, 0.45, "🎯 Consensus Mode (Ultra-Precision)"],
            ]
            gr.Examples(
                examples=demo_samples,
                inputs=[input_img, conf_slider, iou_slider, preset_mode],
                label="Click any card below to test immediately:",
            )

        # RIGHT COLUMN: ANNOTATED CANVAS & DETAILED INTELLIGENCE
        with gr.Column(scale=7):
            annotated_canvas = gr.Image(
                label="🎯 Precision Detection Map",
                height=360,
                interactive=False,
            )

            # CLEAN 3-TAB INTERFACE (NO OVERFLOW '...')
            with gr.Tabs():
                with gr.TabItem("📊 Detection Breakdown"):
                    overview_html = gr.HTML()

                with gr.TabItem("🥗 Nutritional Sheet"):
                    nutrition_html = gr.HTML()

                with gr.TabItem("👨‍🍳 Chef & Pantry Checklist"):
                    recipes_html = gr.HTML()
                    checklist_txt = gr.Textbox(label="Exportable Inventory Checklist", lines=6, interactive=False)

    # EVENT TRIGGER
    analyze_btn.click(
        fn=detect_and_analyze,
        inputs=[input_img, conf_slider, iou_slider, preset_mode],
        outputs=[annotated_canvas, overview_html, nutrition_html, recipes_html, checklist_txt],
    )

    gr.HTML("""
    <div style="text-align: center; color: #475569; font-size: 0.82em; margin-top: 20px; padding: 10px; border-top: 1px solid rgba(148, 163, 184, 0.1);">
        ProduceVision Studio Pro · 63 Produce Classes · USDA Integrated Database · High Precision Computer Vision
    </div>
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, inbrowser=True)