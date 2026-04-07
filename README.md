# Where Am I? — Image-based Geolocalization from Google Maps Data

**Universidade da Beira Interior (UBI) — Department of Computer Science**
**Author:** José Marques | **Supervisor:** Hugo Proença | **Year:** 2022

---

## Overview

An **image-based geolocalization system** that, given a photograph, predicts the **GPS coordinates (latitude, longitude)** of the location where it was taken. The problem is framed as an **image classification task**, where each class corresponds to a GPS coordinate pair rounded to 4 decimal places (~10 metre radius precision).

The coverage area is the **city of Covilhã**, Portugal (city centre and surroundings of Universidade da Beira Interior), using a dataset collected manually with a mobile phone.

---

## Dataset

- **Total images:** 2967 photographs of Covilhã
- **Training set:** 2739 images (used in different split ratios across experiments)
- **Test set:** 228 images (fixed across all experiments)
- **Number of classes:** 1484 distinct coordinate pairs
- **Coordinate precision:** 4 decimal places → ~10 metre radius per class
- **Collection method:** manual, using a mobile app that stores GPS data in image EXIF metadata

> The dataset is small compared to state-of-the-art models that use millions of images. To compensate, **data augmentation** was applied (rotation, zoom, shear, brightness, horizontal and vertical flips).

---

## Architectures Tested

| Model          | Input    | Epochs | Batch | Learning Rate | Std Dev    |
|----------------|----------|--------|-------|---------------|------------|
| ResNet152      | 224×224  | 500    | 19    | 0.002         | 413.53 m   |
| VGG19          | 224×224  | 500    | 19    | 0.002         | 517.30 m   |
| EfficientNetB2 | 260×260  | 500    | 19    | 0.002         | 480.65 m   |
| EfficientNetB2 | 260×260  | 1500   | 19    | 0.002         | 388.16 m   |

All models use:
- **Transfer learning** with ImageNet pre-trained weights (frozen base layers)
- **Optimizer:** Adagrad
- **Loss:** Sparse Categorical Cross-Entropy
- **Metrics:** Sparse Categorical Accuracy, Top-5 Accuracy

---

## Results

### Initial Model Comparison (Test Set — 228 images)

| Distance   | ResNet152 | VGG19  | EffNetB2 (500ep) | EffNetB2 (1500ep) |
|------------|-----------|--------|------------------|-------------------|
| < 5 m      | 0.00%     | 14.54% | 29.07%           | 33.48%            |
| < 10 m     | 0.88%     | 20.26% | 41.85%           | 48.02%            |
| < 20 m     | 1.76%     | 23.79% | 44.49%           | 54.19%            |
| < 50 m     | 4.41%     | 27.75% | 51.54%           | 64.76%            |
| < 100 m    | 7.93%     | 33.92% | 59.03%           | 69.16%            |
| < 250 m    | 18.06%    | 42.73% | 65.64%           | 74.89%            |
| < 500 m    | 41.85%    | 58.59% | 76.65%           | 84.14%            |
| < 800 m    | 65.20%    | 75.77% | 83.70%           | 90.31%            |
| < 1000 m   | 81.06%    | 82.38% | 88.11%           | 92.07%            |
| < 1500 m   | 95.59%    | 95.59% | 96.92%           | 98.24%            |
| **Std Dev**| 413.53 m  | 517.30 m | 480.65 m       | 388.16 m          |

> **EfficientNetB2** best adapted to the dataset size constraints and was selected for further optimization.

---

### Learning Rate Optimization (EfficientNetB2, 500 epochs)

| Learning Rate | < 5 m  | < 10 m | < 25 m | < 50 m | < 100 m | Std Dev    |
|---------------|--------|--------|--------|--------|---------|------------|
| 0.002         | 29.07% | 41.85% | 44.49% | 51.54% | 59.03%  | 480.65 m   |
| **0.01**      | **40.09%** | **57.27%** | **65.20%** | **75.33%** | **79.30%** | **312.94 m** |
| 0.1           | 37.44% | 55.07% | 61.23% | 69.16% | 74.89%  | 349.36 m   |
| 0.25          | 38.77% | 52.86% | 57.27% | 65.20% | 69.60%  | 339.01 m   |

> **Conclusion:** A learning rate of **0.01** yielded the best results.

---

### Batch Size Optimization (EfficientNetB2, lr=0.01, 500 epochs)

| Batch Size | < 5 m  | < 10 m | < 25 m | < 50 m | < 100 m | Std Dev    |
|------------|--------|--------|--------|--------|---------|------------|
| **4**      | **38.77%** | **56.39%** | **61.23%** | **72.69%** | **78.85%** | **285.35 m** |
| 10         | 38.77% | 55.77% | 62.11% | 73.13% | 77.97%  | 296.97 m   |
| 24         | 38.77% | 54.19% | 60.79% | 71.81% | 75.77%  | 307.27 m   |
| 32         | 39.21% | 54.19% | 61.67% | 72.25% | 75.77%  | 355.33 m   |

> **Conclusion:** Smaller batch size → lower standard deviation. **Batch size 4** performed best.

---

### Validation Set Size (EfficientNetB2, lr=0.01, batch=4, 60/40 split)

| Distance   | Percentage  |
|------------|-------------|
| < 5 m      | 36.56%      |
| < 10 m     | 52.42%      |
| < 20 m     | 58.15%      |
| < 50 m     | 70.93%      |
| < 100 m    | 74.45%      |
| < 250 m    | 81.50%      |
| < 500 m    | 87.67%      |
| < 800 m    | 93.39%      |
| < 1000 m   | 95.15%      |
| < 1500 m   | 99.56%      |
| **Std Dev**| **321.49 m**|

---

### Final Model Results (EfficientNetB2, lr=0.01, batch=1, 500 epochs, no validation set)

| Distance   | Percentage  |
|------------|-------------|
| < 5 m      | **42.29%**  |
| < 10 m     | **61.23%**  |
| < 20 m     | **66.08%**  |
| < 50 m     | **77.09%**  |
| < 100 m    | **80.62%**  |
| < 250 m    | **84.58%**  |
| < 500 m    | **89.87%**  |
| < 800 m    | **95.15%**  |
| < 1000 m   | **96.92%**  |
| < 1500 m   | **100.00%** |
| **Std Dev**| **274.56 m**|

> The final model predicts the location within **61.23% of cases to under 10 metres** and **100% of cases to under 1500 metres**.

---

### Partial Image Test (cropped images)

To validate the importance of image coverage, the final model was tested on cropped versions of the test images:

| Distance   | Full Images | Partial Images |
|------------|-------------|----------------|
| < 5 m      | 42.29%      | 0.00%          |
| < 10 m     | 61.23%      | 0.00%          |
| < 20 m     | 66.08%      | 0.88%          |
| < 50 m     | 77.09%      | 3.98%          |
| < 100 m    | 80.62%      | 7.08%          |
| < 250 m    | 84.58%      | 31.86%         |
| < 500 m    | 89.87%      | 54.42%         |
| < 800 m    | 95.15%      | 78.32%         |
| < 1000 m   | 96.92%      | 81.86%         |
| < 1500 m   | 100.00%     | 95.13%         |
| **Std Dev**| **274.56 m**| **439.48 m**   |

> Images with too few discriminative features (too close or heavily cropped) significantly degrade performance.

---

## Model Limitations

1. **Images taken too close** — insufficient discriminative details to confidently assign a class
2. **Images taken too far** — multiple features from different locations confuse the model
3. **Nighttime images** — the dataset contains no night examples
4. **Outside coverage area** — any image from outside Covilhã will always produce incorrect predictions

---

## Project Structure

```
projetoFinal_geolocation/
│
├── EfficientNetB2.py                        # Train with EfficientNetB2
├── Restnet152.py                            # Train with ResNet152
├── VGG19.py                                 # Train with VGG19
│
├── Testar_apenas_uma_imagem.py              # Predict location for a single image
├── Testar_no_conjunto_de_teste.py           # Evaluate on the full test set
├── verificar_distancias.py                  # Analyse distance prediction metrics
│
├── Get_image_coordinates.py                 # Extract GPS from image EXIF metadata
├── get_image_coordinates_quadradasja.py     # Variant of GPS extraction
├── Remove_empty_dirs.py                     # Remove empty directories from dataset
├── remove_same_name.py                      # Remove duplicate filenames
│
├── projeto.yml                              # Conda environment definition
└── distancias_effb2_covilha_1500epochs_*   # Pre-computed evaluation results (pickle)
```

---

## Setup

### Requirements

- Windows 10/11
- [Anaconda](https://www.anaconda.com/) or Miniconda
- NVIDIA GPU with CUDA 11.3 support (recommended)

### Installation

```bash
git clone https://github.com/Lenhas/projetoFinal_geolocation.git
cd projetoFinal_geolocation

conda env create -f projeto.yml
conda activate Resnet
```

---

## Usage

### 1. Prepare the Dataset

Place images in folders named by GPS coordinates (`lat,lon`) or extract coordinates automatically:

```bash
python Get_image_coordinates.py
```

### 2. Train a Model

```bash
python EfficientNetB2.py   # Best results
python Restnet152.py
python VGG19.py
```

### 3. Test on a Single Image

```bash
python Testar_apenas_uma_imagem.py
```

Outputs an interactive HTML map showing predicted vs. actual location.

### 4. Evaluate on the Full Test Set

```bash
python Testar_no_conjunto_de_teste.py
```

### 5. Analyse Distance Results

```bash
python verificar_distancias.py
```

---

## Future Work

- Expand coverage area to Portugal or worldwide
- Add nighttime images to the dataset
- Increase dataset size using publicly available geotagged image sources

---

## Dependencies

| Package            | Version   | Purpose                          |
|--------------------|-----------|----------------------------------|
| TensorFlow (GPU)   | 2.5.0     | Deep learning framework          |
| OpenCV             | 4.5.5.64  | Image processing                 |
| Pillow             | 9.0.1     | Image I/O                        |
| NumPy              | 1.22.3    | Numerical computing              |
| Pandas             | 1.4.1     | Data manipulation                |
| Scikit-learn       | 1.0.2     | Data splitting and utilities     |
| GeoPy              | 2.2.0     | Geodesic distance computation    |
| GPSPhoto           | 2.2.3     | EXIF GPS extraction              |
| Folium             | 0.12.1    | Interactive map visualisation    |
| CUDA Toolkit       | 11.3.1    | GPU acceleration                 |
| cuDNN              | 8.2.1     | GPU deep learning primitives     |

---

## Reference

> *"Where Am I? Image-based Geolocalization from Google Maps Data"*
> José Marques, supervised by Hugo Proença — Universidade da Beira Interior, 2022

---

## License

Academic project — Universidade da Beira Interior.
