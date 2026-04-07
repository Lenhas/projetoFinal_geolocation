import pickle

import numpy as np

with open("distancias_effb2_covilha_1500epochs_lr0.01_4batch_noVal_4dec", "rb") as fp:
    distancias = pickle.load(fp)
print(len(distancias))
print(distancias)

media = 0;
m5, m10, m20, m50, m100, m250, m500, m800, m1000, m1500 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

for d in distancias:
    media += d;
    print(d)
    if d < 5:
        m5 += 1
        m10 += 1
        m20 += 1
        m50 += 1
        m100 += 1
        m250 += 1
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 10:
        m10 += 1
        m20 += 1
        m50 += 1
        m100 += 1
        m250 += 1
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 20:
        m20 += 1
        m50 += 1
        m100 += 1
        m250 += 1
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 50.0:
        m50 += 1
        m100 += 1
        m250 += 1
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 100.0:
        m100 += 1
        m250 += 1
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 250.0:
        m250 += 1
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 500.0:
        m500 += 1
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 800.0:
        m800 += 1
        m1000 += 1
        m1500 += 1
        continue
    if d < 1000.0:
        m1000 += 1
        m1500 += 1
        continue
    if d < 1500.0:
        m1500 += 1

print(m100)
print("Percentagens de acertos:")
print("Com tolerancia de 5m", format((m5 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 10m", format((m10 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 20m", format((m20 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 50m", format((m50 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 100m", format((m100 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 250m", format((m250 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 500m", format((m500 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 800m", format((m800 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 1000m", format((m1000 / len(distancias) * 100), '.2f'), '%')
print("Com tolerancia de 1500m", format((m1500 / len(distancias) * 100), '.2f'), '%')

# print("Desvio Padrao: ",format(media/len(distancias),'.2f'),'m')
print("Desvio Padrao: ", np.std(distancias), 'm')
print("variancia: ", np.var(distancias), 'm')
