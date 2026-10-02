# Gateway Service Migrations

The Gateway service is a stateless API reverse-proxy / routing layer. It does not own relational database tables.
Database schemas are owned and migrated by the individual domain microservices:
- `services/identity`
- `services/clinical`
- `services/knowledge`
- `services/therapeutic`
- `services/ai`
