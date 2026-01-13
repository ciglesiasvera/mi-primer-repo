Verificación: 

1. ¿Cuándo usarías carga completa vs carga incremental?
Respuesta:
- Carga completa (full load):
Se utiliza cuando el volumen de datos es pequeño o mediano, cuando se necesita reconstruir completamente una tabla, o cuando no existe un identificador confiable de cambios (por ejemplo, al iniciar un sistema o tras una corrección masiva de datos).

- Carga incremental:
Se usa en sistemas productivos con grandes volúmenes de datos, donde solo se cargan registros nuevos o modificados (usando id, timestamp, etc.). Reduce tiempo de carga, consumo de recursos y riesgo operativo.

2. ¿Qué factores influyen en el tamaño óptimo de batch para carga de datos?
Respuesta:
- Capacidad de memoria y CPU del sistema destino
- Latencia y ancho de banda (en cargas remotas)
- Tipo de almacenamiento (BD relacional vs Parquet/columnar)
- Requisitos de rendimiento vs estabilidad

Un batch pequeño es más seguro pero más lento; uno grande es más rápido pero puede causar fallos o bloqueos si el sistema no lo soporta.

Resumen:
- Full load = simple y costosa
- Incremental = eficiente y escalable
- Batch size = equilibrio entre rendimiento y estabilidad