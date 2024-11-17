import math
import plotly.graph_objects as go
import numpy as np
import open3d as o3d

# Caminho do arquivo que você deseja ler
caminho_arquivo = "C:\\Users\\Bruno\\Documents\\TCC\\Software\\EspData.txt"

# Lista para armazenar os objetos
objetos_lista = []
steps = 600

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
                theta = math.radians(180-float(valores[1]) * 0.283)

                xValue = dist * math.sin(phi) * math.cos(theta)
                yValue = dist * math.sin(phi) * math.sin(theta)
                zValue = dist * math.cos(phi)
                # Cria um objeto com os valores e armazena na lista
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

# Cria uma nuvem de pontos Open3D
point_cloud = o3d.geometry.PointCloud()

# Criar arrays NumPy para as coordenadas x, y, z e vetores
x_array = np.array(x, dtype='float64')
y_array = np.array(y, dtype='float64')
z_array = np.array(z, dtype='float64')

# Adiciona os arrays ao point_cloud
point_cloud.points = o3d.utility.Vector3dVector(np.column_stack((x_array, y_array, z_array)))

# Gera uma malha a partir da nuvem de pontos
tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(point_cloud)

# Gera superfície pelo método A-Shapes
alpha = 12
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
    point_cloud, alpha, tetra_mesh, pt_map)
mesh.compute_vertex_normals()

o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)