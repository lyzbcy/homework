from py2neo import Graph

g = Graph("bolt://localhost:7687", auth=("neo4j", "tangyudiadid0"))
print("Clearing database...")
g.run("MATCH (n) DETACH DELETE n")
print("Database cleared.")
