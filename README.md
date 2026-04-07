# Geolocation from Street-View Images using Deep Learning

A deep learning system that predicts the **geographic coordinates (latitude/longitude)** of street-view images using transfer learning with three CNN architectures: **EfficientNetB2**, **ResNet152**, and **VGG19**.

The project was developed and tested on the city of **Covilhã, Portugal**, and is based on the research paper *"Where Am I? Image-based Geolocalization from Google Maps Data"*.

---

## How It Works

1. **Data collection** — Street-view images are collected and organized by their GPS coordinates (extracted from EXIF metadata).
2. **Model training** — A pre-trained CNN (EfficientNetB2, ResNet152, or VGG19) is fine-tuned to classify images into one of ~1484 geographic locations.
3. **Inference** — A query image is passed through the model, which predicts the most likely GPS location.
4. **Evaluation** — Predicted coordinates are compared to ground-truth GPS using geodesic distance (meters).

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
├── verificar_distancias.py                  # Analyze prediction distance metrics
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

## Models

| Architecture  | Input Size | Pre-trained on | Optimizer | Epochs |
|---------------|------------|----------------|-----------|--------|
| EfficientNetB2 | 260×260   | ImageNet       | Adagrad   | 1500   |
| ResNet152     | 224×224    | ImageNet       | Adagrad   | 500    |
| VGG19         | 224×224    | ImageNet       | Adagrad   | 500    |

All models use:
- **Transfer learning** with frozen base layers
- **Data augmentation**: rotation (±50°), zoom, shear, brightness, horizontal/vertical flips
- **Loss**: Sparse Categorical Cross-Entropy
- **Metrics**: Sparse Categorical Accuracy, Sparse Top-K Categorical Accuracy

---

## Evaluation Metrics

Prediction accuracy is measured by geodesic distance (meters) between predicted and actual GPS coordinates, across multiple thresholds:

| Threshold | Meaning                    |
|-----------|----------------------------|
| 5 m       | Extremely precise          |
| 10 m      | Street-level               |
| 20 m      | Building-level             |
| 50 m      | Block-level                |
| 100 m     | Neighborhood-level         |
| 250 m     | District-level             |
| 500 m     | City-quarter-level         |
| 1000 m    | City-level                 |
| 1500 m    | Regional-level             |

---

## Setup

### Requirements

- Windows 10/11
- [Anaconda](https://www.anaconda.com/) or Miniconda
- NVIDIA GPU with CUDA 11.3 support (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/projetoFinal_geolocation.git
cd projetoFinal_geolocation

# Create and activate the Conda environment
conda env create -f projeto.yml
conda activate Resnet
```

---

## Usage

### 1. Prepare the Dataset

Place your images in folders named by their GPS coordinates (`lat,lon`) or run the coordinate extractor:

```bash
python Get_image_coordinates.py
```

### 2. Train a Model

```bash
# EfficientNetB2
python EfficientNetB2.py

# ResNet152
python Restnet152.py

# VGG19
python VGG19.py
```

Trained models are saved as `.h5` files along with training history.

### 3. Test on a Single Image

```bash
python Testar_apenas_uma_imagem.py
```

Outputs an interactive HTML map showing the predicted vs. actual location.

### 4. Evaluate on the Full Test Set

```bash
python Testar_no_conjunto_de_teste.py
```

### 5. Analyze Distance Results

```bash
python verificar_distancias.py
```

---

## Key Dependencies

| Package             | Version   | Purpose                          |
|---------------------|-----------|----------------------------------|
| TensorFlow (GPU)    | 2.5.0     | Deep learning framework          |
| Keras               | (bundled) | Model API                        |
| OpenCV              | 4.5.5.64  | Image processing                 |
| Pillow              | 9.0.1     | Image I/O                        |
| NumPy               | 1.22.3    | Numerical computing              |
| Pandas              | 1.4.1     | Data manipulation                |
| Scikit-learn        | 1.0.2     | Data splitting and utilities     |
| GeoPy               | 2.2.0     | Geodesic distance computation    |
| GPSPhoto            | 2.2.3     | EXIF GPS extraction              |
| Folium              | 0.12.1    | Interactive map visualization    |
| Matplotlib          | 3.5.1     | Training history plots           |
| CUDA Toolkit        | 11.3.1    | GPU acceleration                 |
| cuDNN               | 8.2.1     | GPU deep learning primitives     |

---

## Reference

> *"Where Am I? Image-based Geolocalization from Google Maps Data"*
> Included as `_Where_Am_I__Image_based_Geolocalization_from_Google_Maps_Data_43395.pdf`

---

## License

This project is for academic and research purposes.
