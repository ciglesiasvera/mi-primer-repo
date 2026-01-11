-- Diseño de esquemas y patrones de consulta:
-- sql
-- PostgreSQL: Datos transaccionales críticos

CREATE TABLE suscripciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    plan_id INTEGER REFERENCES planes(id),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(20),
    precio_mensual DECIMAL(8,2),
    metodo_pago VARCHAR(50)
);

-- Cassandra: Eventos de reproducción (time-series)
CREATE KEYSPACE streaming WITH REPLICATION = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3
};

CREATE TABLE eventos_reproduccion (
    usuario_id UUID,
    contenido_id UUID,
    timestamp TIMESTAMP,
    duracion_reproducida INT,
    posicion_actual INT,
    dispositivo VARCHAR,
    calidad VARCHAR,
    PRIMARY KEY ((usuario_id, contenido_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Neo4j: Grafo de relaciones usuario-contenido
// Nodos principales
CREATE (u:Usuario {id: 1, nombre: "Ana"})
CREATE (c:Contenido {id: 100, titulo: "Serie Drama", genero: "Drama"})

// Relaciones
CREATE (u)-[:VIO {rating: 5, tiempo_completo: true}]->(c)
CREATE (u)-[:BUSCO_GENERO]->(:Genero {nombre: "Drama"})

// Query de recomendaciones
MATCH (u:Usuario {id: 1})-[:VIO]->(c1:Contenido)-[:DEL_GENERO]->(g:Genero)<-[:DEL_GENERO]-(c2:Contenido)
WHERE NOT (u)-[:VIO]->(c2)
RETURN c2.titulo, COUNT(*) as afinidad
ORDER BY afinidad DESC
LIMIT 10;

-- Redis: Caché de recomendaciones
// Hashes para recomendaciones por usuario
HSET recomendaciones:usuario:1 serie:100 0.95 serie:200 0.87 serie:150 0.82

// Sorted sets para trending
ZADD trending:series 154 serie:100
ZADD trending:series 128 serie:200

-- Elasticsearch: Búsqueda de contenido
PUT /contenido/_doc/100
{
  "titulo": "Serie Drama Completa",
  "genero": ["Drama", "Suspenso"],
  "actores": ["Actor A", "Actor B"],
  "descripcion": "Serie de drama intenso...",
  "rating_promedio": 4.5,
  "temporadas": 3
}

// Query de búsqueda
GET /contenido/_search
{
  "query": {
    "bool": {
      "must": [
        {"multi_match": {"query": "drama", "fields": ["titulo", "descripcion"]}},
        {"terms": {"genero": ["Drama", "Suspenso"]}}
      ],
      "filter": {"range": {"rating_promedio": {"gte": 4.0}}}
    }
  }
}