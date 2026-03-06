docker start neo4j-cds

docker ps

http://localhost:7474

username: neo4j
password: <your password>

"NEO4J_AUTH=neo4j/password"

MATCH (g:Gene)-[r:ASSOCIATED_WITH]->(d:Disease)
RETURN g,r,d
LIMIT 50;

MATCH (g:Gene {id:"100174880"})-[r:ASSOCIATED_WITH]->(d:Disease)
RETURN g,r,d
LIMIT 25;

MATCH ()-[r:ASSOCIATED_WITH]->()
RETURN count(r)
count(r)
22712145