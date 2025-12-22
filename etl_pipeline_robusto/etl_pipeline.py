import logging
import pandas as pd
import sqlite3
import time

# ======================================================
# CONFIGURACIÓN DE LOGGING
# ======================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('etl_pipeline')


# ======================================================
# CLASE PIPELINE ETL ROBUSTO
# ======================================================
class RobustETLPipeline:
    def __init__(self, db_path='etl_database.db'):
        self.db_path = db_path
        self.logger = logging.getLogger('etl_pipeline')
        self.metrics = {
            'processed': 0,
            'errors': 0,
            'start_time': None
        }

    # --------------------------------------------------
    # ORQUESTADOR PRINCIPAL
    # --------------------------------------------------
    def run_pipeline(self):
        self.metrics['start_time'] = pd.Timestamp.now()
        self.logger.info("=== INICIANDO PIPELINE ETL ROBUSTO ===")

        try:
            data = self.extract_with_retry()
            transformed_data = self.transform_with_validation(data)
            self.load_with_transaction(transformed_data)
            self.metrics['processed'] = len(transformed_data)
            self.report_success()

        except Exception as e:
            self.metrics['errors'] += 1
            self.report_failure(e)
            raise

    # --------------------------------------------------
    # EXTRACCIÓN CON REINTENTOS
    # --------------------------------------------------
    def extract_with_retry(self):
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(f"Intento de extracción #{attempt}")

                # Simulación de extracción
                data = pd.DataFrame({
                    'id': range(1, 101),
                    'valor': [x * 1.1 for x in range(1, 101)],
                    'categoria': ['A', 'B', 'C'] * 33 + ['A']
                })

                self.logger.info(f"Extracción exitosa: {len(data)} registros")
                return data

            except Exception as e:
                self.logger.warning(f"Intento #{attempt} falló: {e}")
                if attempt == max_retries:
                    raise
                time.sleep(1)

    # --------------------------------------------------
    # TRANSFORMACIÓN CON VALIDACIONES
    # --------------------------------------------------
    def transform_with_validation(self, data):
        self.logger.info("Iniciando transformación")
        original_count = len(data)

        try:
            # Validación de nulos
            if data.isnull().any().any():
                nulls = data.isnull().sum()
                self.logger.warning(
                    f"Valores nulos encontrados: {nulls[nulls > 0].to_dict()}"
                )

            # Limpieza
            data_clean = data.dropna().copy()

            # Transformaciones
            data_clean['valor_cuadrado'] = data_clean['valor'] ** 2
            data_clean['categoria_normalizada'] = data_clean['categoria'].str.upper()

            # Validación lógica
            if (data_clean['valor_cuadrado'] < 0).any():
                raise ValueError("Valores negativos detectados en valor_cuadrado")

            self.logger.info(
                f"Transformación exitosa: {original_count} -> {len(data_clean)} registros"
            )
            return data_clean

        except Exception as e:
            self.logger.error(f"Error en transformación: {e}")
            raise

    # --------------------------------------------------
    # CARGA CON TRANSACCIONES
    # --------------------------------------------------
    def load_with_transaction(self, data):
        self.logger.info("Iniciando carga a base de datos")

        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute('BEGIN TRANSACTION')

                conn.execute('''
                    CREATE TABLE IF NOT EXISTS datos_transformados (
                        id INTEGER PRIMARY KEY,
                        valor REAL,
                        categoria TEXT,
                        valor_cuadrado REAL,
                        categoria_normalizada TEXT
                    )
                ''')

                # Estrategia replace
                conn.execute('DELETE FROM datos_transformados')

                data.to_sql(
                    'datos_transformados',
                    conn,
                    index=False,
                    if_exists='append'
                )

                conn.commit()
                self.logger.info(
                    f"Carga exitosa: {len(data)} registros insertados"
                )

            except Exception as e:
                self.logger.error(f"Error en carga, rollback ejecutado: {e}")
                raise

    # --------------------------------------------------
    # REPORTES
    # --------------------------------------------------
    def report_success(self):
        duration = pd.Timestamp.now() - self.metrics['start_time']
        self.logger.info("=== PIPELINE ETL COMPLETADO EXITOSAMENTE ===")
        self.logger.info(f"Duración total: {duration}")
        self.logger.info(f"Registros procesados: {self.metrics['processed']}")
        self.logger.info(f"Errores: {self.metrics['errors']}")

    def report_failure(self, error):
        duration = pd.Timestamp.now() - self.metrics['start_time']
        self.logger.error("=== PIPELINE ETL FALLÓ ===")
        self.logger.error(f"Duración hasta fallo: {duration}")
        self.logger.error(f"Error: {error}")


# ======================================================
# EJECUCIÓN
# ======================================================
if __name__ == "__main__":
    pipeline = RobustETLPipeline()
    pipeline.run_pipeline()

    # Verificación final
    with sqlite3.connect('etl_database.db') as conn:
        df_check = pd.read_sql(
            'SELECT COUNT(*) AS registros FROM datos_transformados',
            conn
        )
        print(f"\nRegistros en base de datos: {df_check.iloc[0, 0]}")
