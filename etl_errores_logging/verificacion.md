Ejercicio práctico para aplicar los conceptos aprendidos.
Ejercicio: Construir pipeline ETL con manejo de errores completo

Verificación: ¿Qué información debería incluir en los logs para facilitar el debugging? ¿Cómo decides entre continuar el pipeline con errores parciales vs detenerlo completamente?


1. ¿Qué información debería incluir en los logs para facilitar el debugging?
Respuesta:
- Nombre de la etapa (extract, transform, load)
- Timestamp de inicio y fin
- Cantidad de registros procesados
- Mensaje de error y stack trace si falla
- Identificador del proceso o ejecución
Esto permite reproducir, aislar y corregir fallos rápidamente.

2. ¿Cómo decides entre continuar el pipeline con errores parciales vs detenerlo completamente?
Respuesta:
- Detener el pipeline cuando el error afecta:
  - Integridad de datos
  - Consistencia del resultado
  - Confiabilidad del output final
- Continuar con errores parciales cuando:
  - El error es aislado
  - Existe tolerancia al fallo
  - Los datos no críticos pueden reprocesarse luego
La decisión depende del impacto del error en el negocio y del nivel de criticidad de los datos.