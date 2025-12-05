# -*- coding: utf-8 -*-
"""
从补充资料中导入增强数据到知识图谱
包括：禁忌关系、不良反应、注意事项、特殊人群用药、成份、部位、科室层级等
"""
import os
import pandas as pd
import re
from py2neo import Graph, Node, Relationship, NodeMatcher

class EnhancedDataImporter:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "tangyudiadid0"))
        self.matcher = NodeMatcher(self.g)
        
        # 获取补充资料路径
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_path = os.path.join(cur_dir, '..', '医疗知识图谱', 'KG_demo代码')
        
    def safe_read_excel(self, file_path):
        """安全读取Excel文件"""
        try:
            return pd.read_excel(file_path, encoding='utf-8')
        except:
            try:
                return pd.read_excel(file_path, encoding='gbk')
            except:
                return pd.read_excel(file_path, encoding='gb18030')
    
    def safe_read_csv(self, file_path):
        """安全读取CSV文件"""
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'utf-8-sig']
        for encoding in encodings:
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except:
                continue
        return pd.read_csv(file_path, encoding='utf-8', errors='ignore')
    
    def create_node_if_not_exists(self, label, name):
        """如果节点不存在则创建"""
        node = self.matcher.match(label).where(name=name).first()
        if node is None:
            node = Node(label, name=name)
            self.g.create(node)
        return node
    
    def import_taboo_relationships(self):
        """导入禁忌关系（从寻医问药数据）"""
        print("正在导入禁忌关系...")
        taboo_file = os.path.join(self.base_path, 'data', 'xunyiwenyao', '寻医问药中药品名的禁忌关系.csv')
        if not os.path.exists(taboo_file):
            print(f"禁忌关系文件不存在: {taboo_file}")
            return
        
        try:
            df = self.safe_read_csv(taboo_file)
        except Exception as e:
            print(f"读取禁忌关系文件失败: {e}")
            return
        count = 0
        
        for i in range(len(df)):
            drug_name = str(df.iloc[i]['药品名']).strip()
            taboo_entity = str(df.iloc[i]['禁忌节点']).strip()
            node_type = str(df.iloc[i]['节点类型']).strip()
            
            if drug_name == 'nan' or taboo_entity == 'nan':
                continue
            
            # 查找药品节点（可能是Drug节点）
            drug_node = self.matcher.match('Drug').where(name=drug_name).first()
            if drug_node is None:
                continue
            
            # 根据节点类型创建禁忌实体
            if node_type == '疾病或病症':
                # 先尝试匹配疾病
                taboo_node = self.matcher.match('Disease').where(name=taboo_entity).first()
                if taboo_node is None:
                    # 再尝试匹配症状
                    taboo_node = self.matcher.match('Symptom').where(name=taboo_entity).first()
                    if taboo_node is None:
                        # 创建为症状节点
                        taboo_node = self.create_node_if_not_exists('Symptom', taboo_entity)
            elif node_type == '病人属性':
                taboo_node = self.create_node_if_not_exists('PatientAttribute', taboo_entity)
            elif node_type == '成份':
                taboo_node = self.create_node_if_not_exists('Component', taboo_entity)
            elif node_type == '药物':
                taboo_node = self.matcher.match('Drug').where(name=taboo_entity).first()
                if taboo_node is None:
                    continue
            else:
                continue
            
            # 创建禁忌关系
            try:
                # 检查关系是否已存在
                existing = self.g.run(
                    f"MATCH (d:Drug)-[r:taboo]->(t) WHERE d.name='{drug_name}' AND id(t)={taboo_node.identity} RETURN r"
                ).data()
                if not existing:
                    rel = Relationship(drug_node, 'taboo', taboo_node, name='禁忌')
                    self.g.create(rel)
                    count += 1
            except Exception as e:
                print(f"创建禁忌关系失败: {drug_name} -> {taboo_entity}, 错误: {e}")
        
        print(f"成功导入 {count} 条禁忌关系")
    
    def import_haoxinqing_data(self):
        """导入好心情数据（不良反应、注意事项、特殊人群用药等）"""
        print("正在导入好心情数据...")
        haoxinqing_file = os.path.join(self.base_path, 'data', 'haoxinqing', '好心情_全部.xlsx')
        if not os.path.exists(haoxinqing_file):
            print(f"好心情数据文件不存在: {haoxinqing_file}")
            return
        
        try:
            df = self.safe_read_excel(haoxinqing_file)
        except Exception as e:
            print(f"读取好心情数据失败: {e}")
            return
        
        # 统计导入数量
        stats = {
            'adverse_reaction': 0,
            'precaution': 0,
            'child_drug': 0,
            'elderly_drug': 0,
            'women_drug': 0,
            'component': 0,
            'treat': 0
        }
        
        # 检查必要的列是否存在
        required_columns = ['药品ID', '药品名称']
        if not all(col in df.columns for col in required_columns):
            print(f"好心情数据缺少必要列: {required_columns}")
            return
        
        for i in range(len(df)):
            drug_id = str(df.iloc[i]['药品ID']).strip()
            drug_name = str(df.iloc[i]['药品名称']).strip()
            
            if drug_name == 'nan':
                continue
            
            # 查找或创建药品节点
            drug_node = self.matcher.match('Drug').where(name=drug_name).first()
            if drug_node is None:
                drug_node = Node('Drug', name=drug_name)
                self.g.create(drug_node)
            
            # 处理不良反应
            if '不良反应' in df.columns:
                adverse = str(df.iloc[i]['不良反应']).strip()
                if adverse != 'nan' and adverse:
                    # 创建不良反应节点
                    adverse_node = self.create_node_if_not_exists('AdverseReaction', adverse)
                    try:
                        rel = Relationship(drug_node, 'adverse_reaction', adverse_node, name='不良反应', content=adverse)
                        self.g.create(rel)
                        stats['adverse_reaction'] += 1
                    except:
                        pass
            
            # 处理注意事项
            if '注意事项' in df.columns:
                precaution = str(df.iloc[i]['注意事项']).strip()
                if precaution != 'nan' and precaution:
                    precaution_node = self.create_node_if_not_exists('Precaution', precaution)
                    try:
                        rel = Relationship(drug_node, 'precaution', precaution_node, name='注意事项', content=precaution)
                        self.g.create(rel)
                        stats['precaution'] += 1
                    except:
                        pass
            
            # 处理儿童用药
            if '儿童用药' in df.columns:
                child_drug = str(df.iloc[i]['儿童用药']).strip()
                if child_drug != 'nan' and child_drug:
                    child_node = self.create_node_if_not_exists('PatientAttribute', '儿童')
                    try:
                        rel = Relationship(drug_node, 'special_population', child_node, name='儿童用药', content=child_drug)
                        self.g.create(rel)
                        stats['child_drug'] += 1
                    except:
                        pass
            
            # 处理老年用药
            if '老年用药' in df.columns:
                elderly_drug = str(df.iloc[i]['老年用药']).strip()
                if elderly_drug != 'nan' and elderly_drug:
                    elderly_node = self.create_node_if_not_exists('PatientAttribute', '老年')
                    try:
                        rel = Relationship(drug_node, 'special_population', elderly_node, name='老年用药', content=elderly_drug)
                        self.g.create(rel)
                        stats['elderly_drug'] += 1
                    except:
                        pass
            
            # 处理妇女用药
            if '妇女用药' in df.columns or '孕妇用药' in df.columns:
                women_drug_col = '妇女用药' if '妇女用药' in df.columns else '孕妇用药'
                women_drug = str(df.iloc[i][women_drug_col]).strip()
                if women_drug != 'nan' and women_drug:
                    women_node = self.create_node_if_not_exists('PatientAttribute', '孕妇')
                    try:
                        rel = Relationship(drug_node, 'special_population', women_node, name='妇女用药', content=women_drug)
                        self.g.create(rel)
                        stats['women_drug'] += 1
                    except:
                        pass
            
            # 处理成份
            if '成份' in df.columns or '成分' in df.columns:
                component_col = '成份' if '成份' in df.columns else '成分'
                component = str(df.iloc[i][component_col]).strip()
                if component != 'nan' and component:
                    # 成份可能是多个，用逗号分隔
                    components = re.split('[,，]', component)
                    for comp in components:
                        comp = comp.strip()
                        if comp:
                            comp_node = self.create_node_if_not_exists('Component', comp)
                            try:
                                rel = Relationship(drug_node, 'contains', comp_node, name='包含')
                                self.g.create(rel)
                                stats['component'] += 1
                            except:
                                pass
            
            # 处理治疗关系
            if '治疗' in df.columns or '适应症' in df.columns:
                treat_col = '治疗' if '治疗' in df.columns else '适应症'
                treat = str(df.iloc[i][treat_col]).strip()
                if treat != 'nan' and treat:
                    # 治疗可能是疾病或症状，用逗号分隔
                    treats = re.split('[,，]', treat)
                    for t in treats:
                        t = t.strip()
                        if t:
                            # 先尝试匹配疾病
                            treat_node = self.matcher.match('Disease').where(name=t).first()
                            if treat_node is None:
                                # 再尝试匹配症状
                                treat_node = self.matcher.match('Symptom').where(name=t).first()
                                if treat_node is None:
                                    # 创建为疾病节点
                                    treat_node = self.create_node_if_not_exists('Disease', t)
                            try:
                                rel = Relationship(drug_node, 'treats', treat_node, name='治疗')
                                self.g.create(rel)
                                stats['treat'] += 1
                            except:
                                pass
        
        print(f"好心情数据导入完成:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
    
    def import_symptom_lead_disease(self):
        """导入症状导致疾病的关系"""
        print("正在导入症状导致疾病关系...")
        symptom_file = os.path.join(self.base_path, 'data', 'symptom_lead_disease', '求医网中症状导致疾病层级结构.txt')
        if not os.path.exists(symptom_file):
            print(f"症状导致疾病文件不存在: {symptom_file}")
            return
        
        try:
            with open(symptom_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            try:
                with open(symptom_file, 'r', encoding='gbk') as f:
                    lines = f.readlines()
            except:
                return
        
        count = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析格式：症状 -> 疾病
            if '->' in line or '→' in line:
                parts = re.split('[-→>]', line)
                if len(parts) >= 2:
                    symptom = parts[0].strip()
                    disease = parts[-1].strip()
                    
                    symptom_node = self.matcher.match('Symptom').where(name=symptom).first()
                    disease_node = self.matcher.match('Disease').where(name=disease).first()
                    
                    if symptom_node and disease_node:
                        try:
                            query = f"MATCH (s:Symptom), (d:Disease) WHERE s.name='{symptom}' AND d.name='{disease}' MERGE (s)-[r:leads_to]->(d) SET r.name='导致' RETURN r"
                            result = self.g.run(query).data()
                            if not result:
                                rel = Relationship(symptom_node, 'leads_to', disease_node, name='导致')
                                self.g.create(rel)
                                count += 1
                        except:
                            pass
        
        print(f"成功导入 {count} 条症状导致疾病关系")
    
    def import_department_location_hierarchy(self):
        """导入科室-部位层级结构"""
        print("正在导入科室-部位层级结构...")
        
        # 科室-疾病关系
        dept_disease_file = os.path.join(self.base_path, 'data', 'xunyiwenyao', '寻医问药--科室--疾病.txt')
        if os.path.exists(dept_disease_file):
            self._import_dept_entity_relation(dept_disease_file, 'Disease')
        
        # 科室-症状关系
        dept_symptom_file = os.path.join(self.base_path, 'data', 'xunyiwenyao', '寻医问药--科室--症状.txt')
        if os.path.exists(dept_symptom_file):
            self._import_dept_entity_relation(dept_symptom_file, 'Symptom')
        
        # 部位-疾病关系
        location_disease_file = os.path.join(self.base_path, 'data', 'xunyiwenyao', '寻医问药--部位--疾病.txt')
        if os.path.exists(location_disease_file):
            self._import_location_entity_relation(location_disease_file, 'Disease')
        
        # 部位-症状关系
        location_symptom_file = os.path.join(self.base_path, 'data', 'xunyiwenyao', '寻医问药--部位--症状.txt')
        if os.path.exists(location_symptom_file):
            self._import_location_entity_relation(location_symptom_file, 'Symptom')
    
    def _import_dept_entity_relation(self, file_path, entity_type):
        """导入科室-实体关系"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    lines = f.readlines()
            except:
                return
        
        count = 0
        for line in lines:
            line = line.strip()
            if not line or '->' not in line and '→' not in line:
                continue
            
            parts = re.split('[-→>]', line)
            if len(parts) >= 2:
                dept = parts[0].strip()
                entity = parts[-1].strip()
                
                dept_node = self.create_node_if_not_exists('Department', dept)
                entity_node = self.matcher.match(entity_type).where(name=entity).first()
                
                if entity_node:
                    try:
                        rel = Relationship(dept_node, 'includes', entity_node, name='包括')
                        self.g.create(rel)
                        count += 1
                    except:
                        pass
        
        print(f"  导入 {count} 条科室-{entity_type}关系")
    
    def _import_location_entity_relation(self, file_path, entity_type):
        """导入部位-实体关系"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    lines = f.readlines()
            except:
                return
        
        count = 0
        for line in lines:
            line = line.strip()
            if not line or '->' not in line and '→' not in line:
                continue
            
            parts = re.split('[-→>]', line)
            if len(parts) >= 2:
                location = parts[0].strip()
                entity = parts[-1].strip()
                
                location_node = self.create_node_if_not_exists('Location', location)
                entity_node = self.matcher.match(entity_type).where(name=entity).first()
                
                if entity_node:
                    try:
                        rel = Relationship(location_node, 'includes', entity_node, name='包括')
                        self.g.create(rel)
                        count += 1
                    except:
                        pass
        
        print(f"  导入 {count} 条部位-{entity_type}关系")
    
    def import_all(self):
        """导入所有增强数据"""
        print("=" * 50)
        print("开始导入增强数据...")
        print("=" * 50)
        
        self.import_taboo_relationships()
        self.import_haoxinqing_data()
        self.import_symptom_lead_disease()
        self.import_department_location_hierarchy()
        
        print("=" * 50)
        print("增强数据导入完成！")
        print("=" * 50)

if __name__ == '__main__':
    importer = EnhancedDataImporter()
    importer.import_all()

