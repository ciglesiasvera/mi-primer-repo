# Crear archivo test_analisis.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Crear datos de ejemplo
datos = {'x': np.random.randn(100), 'y': np.random.randn(100)}
df = pd.DataFrame(datos)

# Análisis básico
print("Estadísticas básicas:")
print(df.describe())

# Gráfico simple
plt.scatter(df['x'], df['y'])
plt.title('Primer gráfico con Python')
plt.savefig('primer_grafico.png')
print("Gráfico guardado como primer_grafico.png")