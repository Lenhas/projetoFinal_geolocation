import os

from GPSPhoto import gpsphoto
from PIL import Image

directory = r'C:\\Users\\Utilizador\\Desktop\\Imagens_covilha3'
DR = r'C:\\Users\\Utilizador\\Desktop\\geo_covilha\\'

exif = {}
for filename in os.listdir(directory):

    img_directory = directory + '\\' + str(filename)
    img = Image.open(img_directory)
    print(img_directory)
    latitude = format(gpsphoto.getGPSData(img_directory)['Latitude'], '.4f')
    longitude = format(gpsphoto.getGPSData(img_directory)['Longitude'], '.4f')
    if not os.path.exists(DR + str(latitude) + ',' + str(longitude)):
        os.mkdir(DR + str(latitude) + ',' + str(longitude))
    download_path = DR + str(latitude) + ',' + str(longitude) + '\\' + str(filename)
    img = img.save(download_path)
