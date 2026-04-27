import numpy as np
import matplotlib.pyplot as plt

tabela = []
x = []
y = []

print("preencha a tabela da seguinte maneira: x y ou x;y")

def inputTabel():
    while True:
        xy = input() # entrada de dados da tabela
        if xy == "":
            break
        sep = xy.replace(" ", ";").split(";")
        x.append(float(sep[0]))
        y.append(float(sep[1]))
        tabela.append([float(sep[0]), float(sep[1])])
    calcStats(tabela)

def calcStats(pares):
    if len(pares) < 2:
        return "impossível calcular com poucos dados"
    somaX = sum(x)
    somaY = sum(y)
    somaXY = sum(x*y for x,y in tabela)
    somaX2 = sum(x**2 for x in x)
    somaY2 = sum(y**2 for y in y)

    n = len(tabela)
    mediaX = somaX / n
    mediaY = somaY / n
    mediaXY = somaXY /n

    varX = sum(((x-mediaX)**2) for x in x) / n
    varY = sum(((y-mediaY)**2) for y in y) / n
    stdX = np.sqrt(varX)
    stdY = np.sqrt(varY)

    r = (n * somaXY - somaX * somaY) / np.sqrt((n * somaX2 - somaX**2) * (n * somaY2 - somaY**2))
    r2 = (r**2)*100
    b = (n * somaXY - somaX * somaY) / (n * somaX2 - somaX ** 2)
    a = mediaY - b * mediaX

    y_reta = [a + b * x for x in x]

    print(f"número de elementos da tabela: {n}")
    print(f"Somatório de X = {somaX}") # somas
    print(f"Somatório de Y = {somaY}")
    print(f"Somatório do produto de XY = {somaXY}")
    print(f"Somatório de X² = {somaX2}")
    print(f"Somatório de Y² = {somaY2}")

    print(f"Desvio padrão de X = {stdX}") # desvio padrão
    print(f"Desvio padrão de Y = {stdY}")

    print(f"Média de X = {mediaX}") # media
    print(f"Média de Y = {mediaY}")
    print(f"Média do produto de XY = {mediaXY}")

    print(f"Coeficiente de correlação de Pierson r = {r:.8f}") # coeficiente de Pierson
    print(f"Coeficiente de determinação R² = {r2:.2f}%")
    print(f"valor de a = {a}, valor de b = {b}")
    print(f"reta -> y = {a} + {b}x")

    graph(y_reta, x, y, a, b, r, r2)

def graph(reta, x, y, a, b, r, r2):
    plt.figure(figsize=(10, 6))

    # pares que usuário digitou
    plt.scatter(x, y, color='blue', label = 'Dados Reais', alpha=0.6)

    # reta de regressão
    plt.plot(x, reta, color='red', linewidth=2, label=f'Reta: y = {a:.2f} + {b:.2f}x')

    # informações
    plt.title(f"Regressão Linear (R² = {r2:.2f}%)")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.text(min(x), max(y), f'r = {r:.8f}\nR² = {r2:.2f}', 
         bbox=dict(facecolor='white', alpha=0.5))

    plt.show()


inputTabel()