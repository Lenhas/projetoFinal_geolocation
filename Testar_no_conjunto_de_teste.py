import os
import pickle

import numpy as np
from GPSPhoto import gpsphoto
from PIL import Image
from geopy.distance import geodesic
from tensorflow import keras

distancias = []
classes = "test_effb2_covilha_500epochs_4dec"
model_name = "effb2_covilha_500epochs_lr0.01_4batch_40val_4dec.h5"
with open(classes, "rb") as fp:
    a = pickle.load(fp)
# load the model we saved
resnet_model = keras.models.load_model(model_name)

directory = 'C:\\Users\\Utilizador\\Desktop\\Imagens_covilha2'

for filename in os.listdir(directory):
    try:
        full_path_val = directory + '\\' + filename

        img = Image.open(full_path_val)
        img_resize = img.resize((260, 260))
        img = np.expand_dims(img_resize, axis=0)

        latitude = format(gpsphoto.getGPSData(full_path_val)['Latitude'])
        longitude = format(gpsphoto.getGPSData(full_path_val)['Longitude'])
        loc = str(latitude) + ',' + str(longitude)

        pred = resnet_model.predict(img)

        output_class = a[np.argmax(pred)]
        print("The PREDICTED class is", output_class)
        distancia = geodesic(str(output_class), loc).meters
        print("the REAL class is", loc)
        print("Distancia :", distancia)
        distancias.append(distancia)
    except:
        print("error")

with open("distancias_effb2_covilha_500epochs_lr0.01_4batch_40val_4dec", "wb") as fp:  # Pickling
    pickle.dump(distancias, fp)
