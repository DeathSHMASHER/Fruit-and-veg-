---
title: FruitnVeg
emoji: 🥝
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.49.0
app_file: app.py
pinned: false
---

# 🥝 ProduceVision Studio Pro — Enterprise Fruit & Vegetable AI

> **High-Precision 63-Class Produce Localization · ViT-36 Consensus Verification · Human & Pet Aware · Mobile-Optimized Camera with 90° Rotation & Flip · USDA Nutritional Intelligence**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8m-63_Produce_Classes-brightgreen)
![COCO](https://img.shields.io/badge/YOLOv8n-Human_&_Pet_Aware-indigo)
![HuggingFace](https://img.shields.io/badge/HuggingFace-ViT--36--Ensemble-orange)
![Gradio](https://img.shields.io/badge/UI-Gradio_6.8-yellow)
![Mobile](https://img.shields.io/badge/Mobile-Responsive_%26_Camera_Rotate-teal)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Overview & Key Capabilities

**ProduceVision Studio Pro** is an enterprise-grade computer vision and dietary intelligence platform. Built with a **Multi-Model Consensus Architecture**, it seamlessly localizes, identifies, and categorizes produce across cluttered grocery baskets, kitchen countertops, and live mobile camera feeds with industry-leading precision and ultra-low error rates.

In addition to detecting **63 distinct fruit and vegetable varieties**, the system features dedicated **Human and Pet Recognition**, preventing people and household animals from ever being misclassified as produce while providing instant pet-toxic food safety advisories.

---

## 📱 Mobile Compatibility & Camera Controls

ProduceVision Studio Pro is engineered from the ground up for smartphone browsers (iOS Safari, Android Chrome, Firefox Mobile) as well as desktop displays:

1. **Fluid Responsive UI**:
   - Dynamic viewport sizing with zero horizontal overflow.
   - Stacks controls, live viewfinder, bounding box canvases, and nutrition dashboards into a clean, mobile-first touch layout.

2. **🟢 Prominent Green Camera Privacy Indicator**:
   - Pinned to the top-right corner of the screen, featuring a pulsing emerald green aura and `📷 CAMERA ACTIVE` badge.
   - Designed **70% larger than standard mobile OS privacy dots** for immediate, unmistakable user visibility.
   - Automatically illuminates when the camera is streaming and turns off when the camera stream is halted.

3. **🔴 Camera Power Toggle (`Turn Camera OFF / ON`)**:
   - Hardware-level stream control: tapping **`🔴 Turn Camera OFF`** physically halts camera tracks (`track.stop()`) and frees device hardware, guaranteeing zero data capture.
   - Tapping **`🟢 Turn Camera ON`** re-initializes the live viewfinder instantly.

4. **🔄 Zero-Reload 90° Clockwise Rotation & ↔️ Mirror/Flip**:
   - Live hardware video feed rotates and mirrors smoothly via hardware-accelerated CSS transforms.
   - Eliminates page reloading, stream dropouts, and loading spinners.
   - Captures frames with exact user-configured orientation and mirroring directly into the AI classification pipeline.

5. **⚡ Instant Frame Snap & Classify**:
   - Tapping **`📸 Click Pic & Classify Now`** fires an authentic camera shutter animation and transfers native resolution frames to the dual-engine AI pipeline with zero lag.
   - Works seamlessly with uploaded images, camera snapshots, or clipboard pastes.

---

## 🛡️ Multi-Entity Awareness: Humans, Dogs, and Cats

Traditional produce detectors often misclassify background humans, fingers, or nearby pets as strange produce items. ProduceVision Studio Pro eliminates this issue with integrated COCO multi-entity recognition:

- **👤 Human & Face Detection (`[HUMAN]: Human 95%`)**:
  - Automatically identifies humans and faces in the frame.
  - People are labeled with distinct indigo badges and tracked in the `Subjects` counter.
  - **Zero Nutritional Contamination**: Humans are strictly excluded from produce calorie, carbohydrate, and recipe calculations.

- **🐶 Dog & 🐱 Cat Detection (`[PET]: Dog 94%`, `[PET]: Cat 92%`)**:
  - Detects pets and animals with vibrant coral badges.
  - **Pet Safety Advisory**: When pets are detected alongside produce, the system displays an automatic warning alerting owners about foods toxic to dogs and cats (e.g., *grapes, raisins, onions, garlic, and avocado*).

- **Livestock & Farm Animals**:
  - Distinguishes horses, sheep, cows, and other common animals in agricultural environments.

---

## 🧠 Low-Error Dual-Engine Consensus Pipeline

To achieve the lowest possible error rate, candidate objects undergo a multi-stage verification pipeline:

```
                            User Image / Mobile Camera / Clipboard
                                              │
                        ┌─────────────────────┴─────────────────────┐
                        ▼                                           ▼
          ┌───────────────────────────┐               ┌───────────────────────────┐
          │   COCO Multi-Entity YOLO  │               │   63-Class Produce YOLO   │
          │   Detects Humans & Pets   │               │   Detects Fruits & Vegs   │
          └─────────────┬─────────────┘               └─────────────┬─────────────┘
                        │                                           │
                        │                                [Candidate Bounding Boxes]
                        │                                           │
                        │                                [10% Context-Padded Crops]
                        │                                           │
                        │                                           ▼
                        │                             ┌───────────────────────────┐
                        │                             │    ViT-36 Cross-Validator │
                        │                             │    Classifies image crop  │
                        │                             └─────────────┬─────────────┘
                        │                                           │
                        │                             ┌─────────────┴─────────────┐
                        │                             │   Consensus Decision:     │
                        │                             │   • Agree: Boost confidence
                        │                             │   • Disagree: Cross-validate
                        │                             │   • Strict Gating: Reject 
                        │                             │     non-produce backgrounds
                        │                             └─────────────┬─────────────┘
                        ▼                                           ▼
        ┌───────────────────────────────────────────────────────────────────────────┐
        │                 Non-Maximum Suppression (IoU Deduplication)              │
        └─────────────────────────────────────┬─────────────────────────────────────┘
                                              │
                                              ▼
                    ┌───────────────────────────────────────────────────┐
                    │            Final High-DPI Annotated Canvas        │
                    │        ASCII-Safe Badges (Zero Tofu Font Bugs)    │
                    └─────────────────────────┬─────────────────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
         [Detection Breakdown]     [USDA Nutrition Sheet]     [Chef Pantry & Checklist]
         • Verified item count     • Calories, Carbs, Protein • Instant healthy recipes
         • Subject summary         • Micronutrients & health  • Auto-generated checklist
         • Pet toxicity advisory   • Per 100g USDA reference    for grocery tracking
```

### Why Error Rates Are Minimized:
1. **Context-Padded Crop Extraction**: Crops include a 10% outer border so leaf stems and natural textures are preserved for ViT verification.
2. **Specialized Class Handling**: Items unique to the 63-class model (such as *potatoes, pumpkins, avocados, zucchini, and mushrooms*) are protected from false downgrades.
3. **Strict Fallback Confidence Gating**: If no candidate produce boxes are detected, the full-frame fallback requires `≥ 65%` classification confidence. Random background scenes (desks, walls, furniture) are safely rejected rather than forced into produce categories.
4. **Clean Canvas Badge Rendering**: Uses ASCII-safe text labels (`[FRUIT]: Apple 98%`, `[VEG]: Potato 94%`, `[HUMAN]: Human 96%`), eliminating unrendered square box glyphs (`[]`) across mobile browsers and server environments.

---

## 🥗 Supported Produce Classes (63 Total)

### 🍎 Fruits & Berries (28 Varieties)
> Apple · Apricot · Avocado · Banana · Blackberry · Blueberry · Cantaloupe · Cherry · Clementine · Coconut · Date · Fig · Grape · Kiwi · Lemon · Lime · Mandarin Orange · Mango · Melon · Orange · Papaya · Peach · Pear · Pineapple · Pomegranate · Raspberry · Strawberry · Watermelon

### 🥦 Vegetables, Squashes, Roots & Herbs (35 Varieties)
> Artichoke · Asparagus · Aubergine (Eggplant) · Beetroot · Bell Pepper (Capsicum) · Bitter Gourd · Bottle Gourd · Broccoli · Cabbage · Carrot · Cauliflower · Celery · Chilli Pepper · Corn (Maize) · Courgette (Zucchini) · Cucumber · Garlic · Ginger · Green Bean · Green Onion (Scallion) · Jalapeño · Lettuce · Mushroom · Okra · Onion · Paprika · Peas · Potato · Pumpkin · Radish · Soy Beans · Spinach · Sweetcorn · Sweet Potato · Tomato · Turnip

---

## 📊 Nutritional Intelligence & Chef Recommendations

- **USDA Reference Values**: Every recognized fruit and vegetable links to USDA FoodData Central metrics per 100g serving:
  - Calories (kcal), Carbohydrates (g), Dietary Fiber (g), Protein (g), and Natural Sugars (g).
  - Key Micronutrients (e.g., *Potassium, Vitamin C, Beta-Carotene, Lycopene, Allicin*).
  - Health & Metabolic benefits.
- **Smart Pantry Chef**: Proposes tailored, healthy recipes derived from the ingredients spotted in the frame (e.g., *Crispy Herb-Roasted Potatoes, Stuffed Mediterranean Peppers, Arugula Pear Salad*).
- **Exportable Inventory Checklist**: Generates a clean text inventory list ready to copy into shopping apps or notes.

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### 1 — Clone the Repository
```bash
git clone https://github.com/DeathSHMASHER/Fruit-and-veg-.git
cd Fruit-and-veg-
```

### 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### 3 — Run the Application

#### On Windows (Double-click or run):
```cmd
run_app.bat
```
*or in PowerShell / Command Prompt:*
```cmd
py -3.13 app.py
```

#### On Linux / macOS:
```bash
python3 app.py
```

The application will launch and automatically open your default browser at:
👉 **`http://localhost:7860`**

---

## 🎛️ Sensitivity Controls & Presets

- **🎯 Consensus Mode (Ultra-Precision)**: Enforces dual-model verification with a minimum confidence floor of `0.28`. Ideal for clean lighting and minimizing false positives.
- **⚡ High Sensitivity (Crowded Basket)**: Drops detection floor to `0.20` and optimizes overlap thresholds to catch occluded or partially visible items in deep baskets.
- **Confidence Threshold Slider (`0.10` – `0.90`)**: Directly adjust sensitivity in real time.
- **IoU NMS Overlap Slider (`0.10` – `0.80`)**: Fine-tune duplicate bounding box suppression.

---

## 🌐 Cloud Deployment (Hugging Face Spaces)

This repository is pre-configured for direct deployment on Hugging Face Spaces using the Gradio SDK.

```bash
# Push directly to Hugging Face Spaces using the included helper script:
py -3.13 upload_to_hf.py <YOUR_HF_WRITE_TOKEN>
```

Live Space URL:
🔗 **https://huggingface.co/spaces/NEwBEE67/FruitnVeg**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
