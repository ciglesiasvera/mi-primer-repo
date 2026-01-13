import pandas as pd
from db import get_engine

def cargar_a_postgresql(df, tabla, engine):
    try:
        df.to_sql(
            tabla,
            engine,
            if_exists="append",
            index=False,
            chunksize=1000
        )
        print(f"Cargados {len(df)} registros en la tabla '{tabla}'")
    except Exception as e:
        print(f"Error en la carga: {e}")

def main():
    # DataFrame de ejemplo
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "nombre": ["Ana", "Juan", "María"],
        "edad": [30, 25, 40]
    })

    engine = get_engine()
    cargar_a_postgresql(df, "clientes", engine)

if __name__ == "__main__":
    main()
