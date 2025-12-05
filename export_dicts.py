from py2neo import Graph
import os

class DictExporter:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "tangyudiadid0"))
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.dict_dir = os.path.join(cur_dir, 'dict')
        if not os.path.exists(self.dict_dir):
            os.makedirs(self.dict_dir)

    def export_entity(self, label, filename):
        query = f"MATCH (n:{label}) RETURN n.name"
        data = self.g.run(query).data()
        names = set([d['n.name'] for d in data if d['n.name']])
        
        file_path = os.path.join(self.dict_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(names))
        print(f"Exported {len(names)} {label} to {filename}")

    def export_all(self):
        self.export_entity('Disease', 'disease.txt')
        self.export_entity('Department', 'department.txt')
        self.export_entity('Check', 'check.txt')
        self.export_entity('Drug', 'drug.txt')
        self.export_entity('Food', 'food.txt')
        self.export_entity('Producer', 'producer.txt')
        self.export_entity('Symptom', 'symptom.txt')
        self.export_entity('Component', 'component.txt')
        self.export_entity('Location', 'location.txt')
        # Add others if needed

if __name__ == '__main__':
    exporter = DictExporter()
    exporter.export_all()
