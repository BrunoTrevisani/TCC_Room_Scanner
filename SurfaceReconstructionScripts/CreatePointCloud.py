import math
import plotly.graph_objects as go

# Caminho do arquivo que você deseja ler
caminho_arquivo = "C:\\Users\\Bruno\\Documents\\TCC\\Software\\EspData.txt"

# Lista para armazenar os objetos
objetos_lista = []

# Abre o arquivo em modo de leitura
with open(caminho_arquivo, 'r') as arquivo:
    # Lê cada linha do arquivo
    for linha in arquivo:
        # Divide a linha em partes usando a vírgula como separador
        valores = linha.strip().split(',')

        if float(valores[0]) > 11:
            # Verifica se a linha possui três valores
            if len(valores) == 3:
                dist = float(valores[0]) - 12
                phi = math.radians(float(valores[2])+1)
                theta = math.radians(180-float(valores[1]) * 0.212)

                xValue = dist * math.sin(phi) * math.cos(theta)
                yValue = dist * math.sin(phi) * math.sin(theta)
                zValue = dist * math.cos(phi)
                # Cria um objeto com os valores e armazene-o na lista
                if yValue > 33e-15 and xValue > -260 and zValue > -1000 and zValue < 1000:
                    obj = {
                        'x': float(xValue),
                        'y': float(yValue),
                        'z': float(zValue)
                    }
                    objetos_lista.append(obj)

# Extrai as coordenadas dos objetos
x = [obj['x'] for obj in objetos_lista]
y = [obj['y'] for obj in objetos_lista]
z = [obj['z'] for obj in objetos_lista]

# Cria um gráfico 3D interativo
fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=5))])

# Defini rótulos dos eixos
fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))

# Exibi o gráfico
fig.show()
