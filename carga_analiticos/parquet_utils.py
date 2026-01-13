def cargar_a_parquet(df, ruta_archivo):
    try:
        df.to_parquet(
            ruta_archivo,
            engine="pyarrow",
            compression="snappy",  # Balance óptimo velocidad / tamaño
            index=False
        )
        print(f"Datos guardados correctamente en {ruta_archivo}")
        return True
    except Exception as e:
        print(f"Error guardando Parquet: {e}")
        return False
