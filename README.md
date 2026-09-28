---
title: FruitnVeg
emoji: 🥝
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 6.8.0
app_file: app.py
pinned: false
---

# 🥝 ProduceVision Studio Pro — Enterprise Fruit & Vegetable AI

> **High-Precision 63-Class Produce Localization · ViT-36 Consensus Verification · Zero-Tofu Clean Canvas · USDA Nutritional Intelligence**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8m-63_Produce_Classes-brightgreen)
![HuggingFace](https://img.shields.io/badge/HuggingFace-ViT--36--Ensemble-orange)
![Gradio](https://img.shields.io/badge/UI-Gradio_6-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ What's New & Upgraded

| Feature | Description |
|---------|-------------|
| ⚡ **63-Class YOLOv8m Specialist** | Upgraded to high-capacity YOLOv8 Medium covering 63 distinct fruits, vegetables, squashes, and root crops (potatoes, pumpkins, avocados, zucchini, mushrooms, etc.). |
| 🛡️ **Dual-Engine Consensus** | Cross-validates every candidate detection against ViT-36 to eliminate false classifications (e.g. potatoes never mislabeled as pears). |
| 🏷️ **Clean High-DPI Canvas** | Replaced unrendered font glyphs with ASCII-safe high-contrast badges (`[Veg] Potato 95%`). |
| 🎚️ **Precision Sensitivity Controls** | Fine-tune **Confidence Threshold**, **IoU NMS Overlap**, and preset modes (`🎯 Consensus Mode` vs `⚡ High Sensitivity`). |
| 🥗 **USDA Nutritional Analytics** | Real-time calorie and macronutrient breakdown (Carbs, Protein, Fiber, Sugars) + Key Vitamins & Health benefits. |
| 👨‍🍳 **Smart Pantry Chef** | Recommends instant healthy recipes based on the fresh ingredients detected in your image. |
| 📋 **Exportable Checklist** | Auto-generates a clean produce inventory / shopping checklist with item counts. |
| 🌟 **1-Click Test Showcase** | 6 built-in demo photos (Potatoes, Fruit Basket, Bell Peppers, Tomatoes, Carrots, Bananas). |
| 📷 **Webcam & Clipboard Support** | Take live snapshots via webcam, paste from clipboard, or drag-and-drop. |

---

## 🔧 How the Dual-Engine Works

```
                        User Photo / Webcam / Demo
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │  YOLOv8 Produce Specialist (best.pt) │
                 │  Fast localization of produce boxes  │
                 └──────────────────┬───────────────────┘
                                    │
                         [Extracted Item Crops]
                          (with Context Padding)
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │    ViT-36 High-Fidelity Classifier   │
                 │    Cross-validates candidate labels   │
                 └──────────────────┬───────────────────┘
                                    │
                        [Smart Ensemble Decision]
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
[Annotated Visual Map]      [USDA Nutrition Sheet]     [Smart Recipe & Pantry]
(Boxes + Confidence +       (Calories, Carbs,          (Healthy Culinary Ideas
 Crops Gallery)              Vitamins & Benefits)       + Exportable Checklist)
```

---

## 📋 Supported Classes (36 Total)

**Fruits:**
> Apple · Banana · Coconut · Grape · Green Orange · Kiwi · Lemon · Mango · Melon · Orange · Peach · Pear · Pineapple · Pomegranate · Strawberry · Watermelon

**Vegetables & Herbs:**
> Beetroot · Bell Pepper (Capsicum) · Bitter Gourd · Bottle Gourd · Broccoli · Cabbage · Carrot · Cauliflower · Chilli Pepper · Corn (Maize) · Cucumber · Eggplant · Garlic · Ginger · Jalapeño · Lettuce · Okra · Onion · Paprika · Peas · Potato · Radish · Soy Beans · Spinach · Sweetcorn · Sweet Potato · Tomato · Turnip

---

## 🚀 Quick Start

### 1 — Clone the Repository
```bash
git clone https://github.com/DeathSHMASHER/Fruit-and-veg-.git
cd Fruit-and-veg-
```

### 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### 3 — Launch the Application
- **Windows (Double-click or run):**
  ```cmd
  run_app.bat
  ```
  *or*
  ```cmd
  py -3.13 app.py
  ```

Your browser opens automatically at **http://localhost:7860** 🎉

---

## 💡 Pro Tips for Best Accuracy

- **Single or Multiple Items**: Works on isolated single fruits as well as multi-item market baskets.
- **Cluttered Images**: If produce items are overlapping, slide the **Confidence Threshold** down to `0.25–0.30` and adjust **IoU NMS** to `0.40`.
- **Lighting**: Bright, natural lighting produces the highest confidence scores.
