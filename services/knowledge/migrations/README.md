# Knowledge Service — No Alembic Migrations

The Knowledge service uses **Neo4j** (a graph database), which is schema-less.
Migrations are managed via Cypher constraints applied at startup in `app/core/database.py`.

To inspect or manage the graph schema, connect to the Neo4j browser at:
  http://localhost:7474
  Credentials: neo4j / zayvora_dev_password (local dev)
