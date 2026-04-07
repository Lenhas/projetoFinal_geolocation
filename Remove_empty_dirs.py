import os
import shutil

folder_path = r'C:\\Users\\Utilizador\\Desktop\\geo_covilha3\\'
lista = os.listdir(folder_path)
lista_5 = []
lista_5_3 = []
for folder in lista:
    if len(os.listdir(folder_path + folder)) < 2:  # Check if the folder is empty
        shutil.rmtree(folder_path + folder)  # If so, delete it
