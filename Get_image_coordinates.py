from GPSPhoto import gpsphoto
import os

from GPSPhoto import gpsphoto
from PIL import Image
from PIL import ImageOps

directory = r'C:\\Users\\Utilizador\\Desktop\\Imagens_covilha'
DR = r'C:\\Users\\Utilizador\\Desktop\\geo_covilha\\'

exif = {}
for filename in os.listdir(directory):

    img_directory = directory + '\\' + str(filename)
    img = Image.open(img_directory)
    print(img_directory)
    latitude = format(gpsphoto.getGPSData(img_directory)['Latitude'], '.4f')
    longitude = format(gpsphoto.getGPSData(img_directory)['Longitude'], '.4f')
    border = (0, 280, 0, 280)  # left, top, right, bottom
    img_cropped = ImageOps.crop(img, border)
    if not os.path.exists(DR + str(latitude) + ',' + str(longitude)):
        os.mkdir(DR + str(latitude) + ',' + str(longitude))
    download_path = DR + str(latitude) + ',' + str(longitude) + '\\' + str(filename)
    img_cropped = img_cropped.save(download_path)
