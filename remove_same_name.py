import os

directory = r"C:\Users\Utilizador\Desktop\Imagens_covilha2"
directory_geo = r"C:\Users\Utilizador\Desktop\Imagens_covilha"

for filename in os.listdir(directory):
    path = directory_geo + "\\" + filename
    os.remove(path)
