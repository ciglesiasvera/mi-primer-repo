import logging
import time
from functools import wraps

import pandas as pd
import numpy as np
from typing import Dict, Any

# -----------------------------
# CONFIGURACIÓN DE LOGGING
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_ecommerce.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('etl_ecommerce')


def log_etapa(etapa):
    """Decorator para logging de etapas del pipeline"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Iniciando {etapa}")
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"{etapa} completada en {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"{etapa} falló en {duration:.2f}s: {e}")
                raise
        return wrapper
    return decorator


# -----------------------------
# PIPELINE ETL
# -----------------------------
class ETLPipeline:
    def __init__(self):
        self.errores = []

    @log_etapa("extracción de datos")
    def extract(self) -> pd.DataFrame:
        if np.random.random() < 0.1:
            raise ConnectionError("Error de conexión a la fuente de datos")

        df = pd.DataFrame({
            'orden_id': range(1, 101),
            'cliente_id': np.random.randint(1, 21, 100),
            'producto': np.random.choice(['A', 'B', 'C', 'D'], 100),
            'cantidad': np.random.randint(1, 6, 100),
            'precio': np.round(np.random.uniform(10, 200, 100), 2)
        })

        logger.info(f"Extraídos {len(df)} registros")
        return df

    @log_etapa("transformación de datos")
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValueError("Dataset vacío")

        df = df.copy()
        df['total'] = df['cantidad'] * df['precio']
        df['categoria_precio'] = pd.cut(
            df['precio'],
            bins=[0, 50, 100, 200],
            labels=['Bajo', 'Medio', 'Alto']
        )

        if df['total'].isnull().any():
            raise ValueError("Error en cálculo de totales")

        logger.info("Transformaciones aplicadas correctamente")
        return df

    @log_etapa("carga de datos")
    def load(self, df: pd.DataFrame) -> bool:
        if np.random.random() < 0.05:
            raise Exception("Error de conexión a base de datos")

        logger.info(f"Cargados {len(df)} registros")
        return True

    def ejecutar_pipeline(self) -> Dict[str, Any]:
        logger.info("Iniciando pipeline ETL completo")

        try:
            datos = self.extract()
            datos = self.transform(datos)
            self.load(datos)

            return {
                'exito': True,
                'registros_procesados': len(datos),
                'errores': self.errores
            }

        except Exception as e:
            self.errores.append(str(e))
            logger.error(f"Pipeline fallido: {e}")

            return {
                'exito': False,
                'error_principal': str(e),
                'errores': self.errores
            }


# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == "__main__":
    pipeline = ETLPipeline()
    resultado = pipeline.ejecutar_pipeline()

    print("\nResultado del pipeline")
    print(f"Éxito: {resultado['exito']}")

    if resultado['exito']:
        print(f"Registros procesados: {resultado['registros_procesados']}")
    else:
        print(f"Error principal: {resultado['error_principal']}")

    print(f"Errores registrados: {len(resultado['errores'])}")
