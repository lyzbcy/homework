from py2neo import Graph

g = Graph("bolt://localhost:7687", auth=("neo4j", "tangyudiadid0"))

labels = ['Disease', 'Drug', 'Symptom', 'Producer', 'Food', 'Check', 'Department', 'Component', 'Location', 'PatientAttribute', 'AdverseReaction', 'Precaution']

for label in labels:
    try:
        g.schema.create_index(label, "name")
        print(f"Created index for {label}")
    except Exception as e:
        print(f"Error creating index for {label}: {e}")
