# Cloud-native Trino (prestosql) + Hive + Minio + Flowise
## Technologies:
### Query Engine is `Trino (PrestoSQL)`
### Metadata Store is `Apache Hive`
### Object Storage is `Minio (S3 compatable)`
### AI tool is `Flowise AI`

## Get things running
1. Clone repo
2. Install docker + docker-compose
3. Run `docker-compose --compatibility up`
4. Done! Checkout the service endpoints:

Trino: `http://localhost:8080/ui/` (username can be anything) <br>
Minio: `http://localhost:9001/` (username: `minio_access_key`, password: `minio_secret_key`)<br>
Flowise： `http://localhost:3000/`



 
