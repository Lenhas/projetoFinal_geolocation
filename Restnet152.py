import pickle

import tensorflow.keras.applications.resnet
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

img_height, image_width = (224, 224)
batch_size = 1
train_data_dir = r"C:\\Users\\Utilizador\\Desktop\\geo_covilha"
classes = "resnet152_covilha_1500epochs_lr0.01_4batch_noVal_4dec"
model_name = "resnet152_covilha_1500epochs_lr0.01_4batch_noVal_4dec.h5"
model_history = "resnet152_covilha_1500epochs_lr0.01_4batch_noVal_4dec_history"

# augmentação das imagens
train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input,
                                   shear_range=0.7,
                                   zoom_range=0.7,
                                   rotation_range=50,
                                   width_shift_range=0.7,
                                   height_shift_range=0.7,
                                   horizontal_flip=True,
                                   vertical_flip=True,
                                   validation_split=0.40,
                                   brightness_range=(0.2, 0.8),
                                   fill_mode='nearest',
                                   )
####
# Dividir em conjunto de treino e validação
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    seed=47,
    target_size=(img_height, image_width),
    batch_size=batch_size,
    class_mode='sparse',
    subset='training',
    shuffle=True
)

valid_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, image_width),
    batch_size=batch_size,
    class_mode="sparse",
    subset='validation')

x, y = train_generator.next()

print(x.shape)

print(train_generator.class_indices.keys())
a = list(train_generator.class_indices.keys())
# Guardar classes num ficheiro através do pickle
with open(classes, "wb") as fp:  # Pickling
    pickle.dump(a, fp)

base_model = tensorflow.keras.applications.resnet.ResNet152(include_top=False, weights="imagenet")
x = base_model.output
x = GlobalAveragePooling2D()(x)

x = Dense(1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False
# treinar o modelo
model.compile(optimizer=tensorflow.keras.optimizers.Adagrad(learning_rate=0.01), loss="sparse_categorical_crossentropy",
              metrics=['sparse_categorical_accuracy', 'sparse_top_k_categorical_accuracy'])
history = model.fit(train_generator, validation_data=valid_generator, epochs=500, batch_size=batch_size)

# guardar o modelo
model.save(model_name)

print(history.history.keys())
b = history.history
# guardar a historia do modelo para desenhar gráficos
with open(model_history, "wb") as fp:  # Pickling
    pickle.dump(b, fp)
