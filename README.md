# Where Am I? — Image-based Geolocalization from Google Maps Data

**Universidade da Beira Interior (UBI) — Departamento de Informática**
**Autor:** José Marques | **Orientador:** Hugo Proença | **Ano:** 2022

---

## Descrição

Sistema de **geolocalização baseado em imagem** que, dada uma fotografia, prevê as **coordenadas GPS (latitude, longitude)** do local onde foi tirada. O problema é tratado como um problema de **classificação de imagens**, onde cada classe corresponde a um par de coordenadas arredondado a 4 casas decimais (precisão de ~10 metros de raio).

A área de cobertura é a **cidade da Covilhã**, Portugal (centro e arredores da Universidade da Beira Interior), com um conjunto de dados recolhido manualmente com telemóvel.

---

## Dataset

- **Total de imagens:** 2967 fotografias da Covilhã
- **Conjunto de treino:** 2739 imagens (usadas em diferentes rácios)
- **Conjunto de teste:** 228 imagens (fixo ao longo de todos os testes)
- **Número de classes:** 1484 pares de coordenadas distintos
- **Resolução de coordenadas:** 4 casas decimais → ~10 metros de raio por classe
- **Recolha:** manual, com aplicação móvel que armazena GPS nas meta-informações EXIF

> O conjunto de dados é pequeno face aos modelos do estado da arte, que utilizam milhões de imagens. Para compensar, recorreu-se a **data augmentation** (rotação, zoom, shear, brilho, flip horizontal e vertical).

---

## Arquiteturas Testadas

| Modelo         | Input    | Épocas | Batch | Learning Rate | Std Dev    |
|----------------|----------|--------|-------|---------------|------------|
| ResNet152      | 224×224  | 500    | 19    | 0.002         | 413.53 m   |
| VGG19          | 224×224  | 500    | 19    | 0.002         | 517.30 m   |
| EfficientNetB2 | 260×260  | 500    | 19    | 0.002         | 480.65 m   |
| EfficientNetB2 | 260×260  | 1500   | 19    | 0.002         | 388.16 m   |

Todos os modelos usam:
- **Transfer learning** com pesos ImageNet (camadas base congeladas)
- **Otimizador:** Adagrad
- **Loss:** Sparse Categorical Cross-Entropy
- **Métricas:** Sparse Categorical Accuracy, Top-5 Accuracy

---

## Resultados

### Comparação dos Modelos Iniciais (Conjunto de Teste — 228 imagens)

| Distância  | ResNet152 | VGG19  | EffNetB2 (500ep) | EffNetB2 (1500ep) |
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

> A **EfficientNetB2** foi a arquitectura que melhor se adaptou às limitações do tamanho do conjunto de dados e foi selecionada para otimização.

---

### Otimização do Learning Rate (EfficientNetB2, 500 épocas)

| Learning Rate | < 5 m  | < 10 m | < 25 m | < 50 m | < 100 m | Std Dev    |
|---------------|--------|--------|--------|--------|---------|------------|
| 0.002         | 29.07% | 41.85% | 44.49% | 51.54% | 59.03%  | 480.65 m   |
| **0.01**      | **40.09%** | **57.27%** | **65.20%** | **75.33%** | **79.30%** | **312.94 m** |
| 0.1           | 37.44% | 55.07% | 61.23% | 69.16% | 74.89%  | 349.36 m   |
| 0.25          | 38.77% | 52.86% | 57.27% | 65.20% | 69.60%  | 339.01 m   |

> **Conclusão:** Learning rate de **0.01** produziu os melhores resultados.

---

### Otimização do Batch Size (EfficientNetB2, lr=0.01, 500 épocas)

| Batch Size | < 5 m  | < 10 m | < 25 m | < 50 m | < 100 m | Std Dev    |
|------------|--------|--------|--------|--------|---------|------------|
| **4**      | **38.77%** | **56.39%** | **61.23%** | **72.69%** | **78.85%** | **285.35 m** |
| 10         | 38.77% | 55.77% | 62.11% | 73.13% | 77.97%  | 296.97 m   |
| 24         | 38.77% | 54.19% | 60.79% | 71.81% | 75.77%  | 307.27 m   |
| 32         | 39.21% | 54.19% | 61.67% | 72.25% | 75.77%  | 355.33 m   |

> **Conclusão:** Batch size menor → menor desvio padrão. **Batch size 4** foi o melhor.

---

### Tamanho do Conjunto de Validação (EfficientNetB2, lr=0.01, batch=4, rácio 60/40)

| Distância  | Percentagem |
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

### Modelo Final — Resultados (EfficientNetB2, lr=0.01, batch=1, 500 épocas, sem validação)

| Distância  | Percentagem |
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

> O modelo final prevê a localização dentro de **61.23% dos casos a menos de 10 metros** e **100% dos casos a menos de 1500 metros**.

---

### Teste com Imagens Parciais (recortadas)

Para validar a importância da abrangência visual da imagem, testou-se o modelo final com versões recortadas das imagens de teste:

| Distância  | Imagens Completas | Imagens Parciais |
|------------|-------------------|------------------|
| < 5 m      | 42.29%            | 0.00%            |
| < 10 m     | 61.23%            | 0.00%            |
| < 20 m     | 66.08%            | 0.88%            |
| < 50 m     | 77.09%            | 3.98%            |
| < 100 m    | 80.62%            | 7.08%            |
| < 250 m    | 84.58%            | 31.86%           |
| < 500 m    | 89.87%            | 54.42%           |
| < 800 m    | 95.15%            | 78.32%           |
| < 1000 m   | 96.92%            | 81.86%           |
| < 1500 m   | 100.00%           | 95.13%           |
| **Std Dev**| **274.56 m**      | **439.48 m**     |

> Imagens com poucos detalhes discriminativos (muito próximas ou muito recortadas) degradam significativamente o desempenho.

---

## Limitações do Modelo

1. **Imagens muito próximas** — poucos detalhes discriminativos para identificar a localização
2. **Imagens muito abrangentes** — múltiplas características de zonas diferentes confundem o modelo
3. **Imagens noturnas** — dataset sem exemplos noturnos
4. **Fora da área de cobertura** — qualquer imagem fora da Covilhã produzirá previsões incorretas

---

## Estrutura do Projeto

```
projetoFinal_geolocation/
│
├── EfficientNetB2.py                        # Treino com EfficientNetB2
├── Restnet152.py                            # Treino com ResNet152
├── VGG19.py                                 # Treino com VGG19
│
├── Testar_apenas_uma_imagem.py              # Prever localização de uma imagem
├── Testar_no_conjunto_de_teste.py           # Avaliar no conjunto de teste completo
├── verificar_distancias.py                  # Análise das métricas de distância
│
├── Get_image_coordinates.py                 # Extrair GPS das meta-informações EXIF
├── get_image_coordinates_quadradasja.py     # Variante da extração GPS
├── Remove_empty_dirs.py                     # Remover diretórios vazios
├── remove_same_name.py                      # Remover ficheiros duplicados
│
├── projeto.yml                              # Definição do ambiente Conda
└── distancias_effb2_covilha_1500epochs_*   # Resultados pré-calculados (pickle)
```

---

## Instalação

### Requisitos

- Windows 10/11
- [Anaconda](https://www.anaconda.com/) ou Miniconda
- GPU NVIDIA com suporte CUDA 11.3 (recomendado)

### Configuração do Ambiente

```bash
git clone https://github.com/Lenhas/projetoFinal_geolocation.git
cd projetoFinal_geolocation

conda env create -f projeto.yml
conda activate Resnet
```

---

## Utilização

### 1. Preparar o Dataset

Coloca as imagens em pastas com o nome das coordenadas GPS (`lat,lon`) ou extrai as coordenadas automaticamente:

```bash
python Get_image_coordinates.py
```

### 2. Treinar um Modelo

```bash
python EfficientNetB2.py   # Melhor resultado
python Restnet152.py
python VGG19.py
```

### 3. Testar numa Imagem

```bash
python Testar_apenas_uma_imagem.py
```

Gera um mapa HTML interativo com a localização prevista vs. real.

### 4. Avaliar no Conjunto de Teste

```bash
python Testar_no_conjunto_de_teste.py
```

### 5. Analisar Distâncias

```bash
python verificar_distancias.py
```

---

## Trabalho Futuro

- Expandir a área de cobertura para Portugal ou o mundo
- Adicionar imagens noturnas ao dataset
- Aumentar o dataset com imagens de múltiplas fontes públicas

---

## Tecnologias

| Pacote             | Versão    | Uso                              |
|--------------------|-----------|----------------------------------|
| TensorFlow (GPU)   | 2.5.0     | Framework de deep learning       |
| OpenCV             | 4.5.5.64  | Processamento de imagem          |
| Pillow             | 9.0.1     | I/O de imagens                   |
| NumPy              | 1.22.3    | Computação numérica              |
| Pandas             | 1.4.1     | Manipulação de dados             |
| Scikit-learn       | 1.0.2     | Divisão de dados e utilitários   |
| GeoPy              | 2.2.0     | Cálculo de distância geodésica   |
| GPSPhoto           | 2.2.3     | Extração de GPS do EXIF          |
| Folium             | 0.12.1    | Visualização em mapa interativo  |
| CUDA Toolkit       | 11.3.1    | Aceleração GPU                   |
| cuDNN              | 8.2.1     | Primitivas GPU para deep learning|

---

## Referência

> *"Where Am I? Image-based Geolocalization from Google Maps Data"*
> José Marques, orientado por Hugo Proença — Universidade da Beira Interior, 2022

---

## Licença

Projeto académico — Universidade da Beira Interior.
