import pandas as pd
import numpy as np
from parquet_utils import cargar_a_parquet

def main():
    # Simulación de dataset analítico
    df = pd.DataFrame({
        "pedido_id": range(1, 11),
        "cliente_id": np.random.randint(1, 5, 10),
        "producto": np.random.choice(["A", "B", "C", "D"], 10),
        "precio": np.random.uniform(50, 500, 10).round(2),
        "fecha": pd.date_range("2024-01-01", periods=10)
    })

    ruta = "data/ventas.parquet"
    cargar_a_parquet(df, ruta)

if __name__ == "__main__":
    main()
