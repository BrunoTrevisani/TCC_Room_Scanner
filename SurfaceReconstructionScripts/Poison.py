import math
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d

# Caminho do arquivo que você deseja ler
#caminho_arquivo = "C:\\Users\\Bruno\\Documents\\TCC\\Software\\Arquive\\EspData_old.txt"
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
                theta = math.radians(180-float(valores[1]) * 0.283)

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

x = [obj['x'] for obj in objetos_lista]
y = [obj['y'] for obj in objetos_lista]
z = [obj['z'] for obj in objetos_lista]

vetor_x = [obj['x'] for obj in objetos_lista]
vetor_y = [obj['y'] for obj in objetos_lista]
vetor_z = [obj['z'] for obj in objetos_lista]

# Cria arrays NumPy para as coordenadas x, y, z e vetores
x_array = np.array(x, dtype='float64')
y_array = np.array(y, dtype='float64')
z_array = np.array(z, dtype='float64')
vetor_x_array = -np.array(vetor_x, dtype='float64')
vetor_y_array = -np.array(vetor_y, dtype='float64')
vetor_z_array = -np.array(vetor_z, dtype='float64')

# Cria uma nuvem de pontos Open3D
point_cloud = o3d.geometry.PointCloud()

# Adiciona os arrays ao point_cloud
point_cloud.points = o3d.utility.Vector3dVector(np.column_stack((x_array, y_array, z_array)))

# Adiciona os vetores (se você quiser) como atributos
point_cloud.normals = o3d.utility.Vector3dVector(np.column_stack((vetor_x_array, vetor_y_array, vetor_z_array)))

# Constrói malha pelo método de Poisson a partir da nuvem de pontos com um detalhamento de nível 15
with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=15)

# Personaliza densidades de malha para melhor visualização
densities = np.asarray(densities)
density_colors = plt.get_cmap('plasma')((densities - densities.min()) / (densities.max() - densities.min()))
density_colors = density_colors[:, :3]
density_mesh = o3d.geometry.TriangleMesh()
density_mesh.vertices = mesh.vertices
density_mesh.triangles = mesh.triangles
density_mesh.triangle_normals = mesh.triangle_normals
density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)

o3d.visualization.draw_geometries([density_mesh],
                                  zoom=0.664,
                                  front=[-0.4761, -0.4698, -0.7434],
                                  lookat=[1.8900, 3.2596, 0.9284],
                                  up=[0.2304, -0.8825, 0.4101])