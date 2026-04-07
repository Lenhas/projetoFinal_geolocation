import pickle
import webbrowser

import folium
import numpy as np
from PIL import Image
from tensorflow import keras

classes = "test_effb2_covilha_500epochs_4dec"
model_name = "effb2_covilha_500epochs_lr0.01_4batch_40val_4dec.h5"
lats = []
lons = []
with open(classes, "rb") as fp:
    a = pickle.load(fp)
resnet_model = keras.models.load_model(model_name)
img_dir = "C:\\Users\\Utilizador\\Desktop\\Imagens_covilha2\\BBDP4646.JPG"

img = Image.open(img_dir)
img_resize = img.resize((260, 260))
img = np.expand_dims(img_resize, axis=0)

pred = resnet_model.predict(img)
np.sort(pred)
pred2 = np.sort(pred, axis=1)
value = 0
for x in range(1484):
    print(pred2[0][x])
    if pred[0][x] > value:
        value = pred[0][x]

print(value)
print()
print(pred[0][np.argmax(pred)])

print(np.argmax(pred))
# pred = np.delete(pred, np.argmax(pred))  # TOP 2
# pred = np.delete(pred,np.argmax(pred)) #TOP 3
# output_class = a[np.argmax(pred)]

output_class = a[np.argmax(pred)]
print("The PREDICTED class is", output_class)

lat = float(str(output_class).split(",")[0])
lon = float(str(output_class).split(",")[1])
print(lat, lon)
lats.append(lat)
lons.append(lon)

m = folium.Map(location=[lat, lon], zoom_start=15);
folium.Marker(location=[lats[0], lons[0]]).add_to(m)
m.save("mymap.html")
webbrowser.open("mymap.html", new=2)
