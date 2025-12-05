class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease_prevent':
                # 先查找症状相关的疾病，然后返回这些疾病的预防方法
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'symptom_disease_drug':
                # 先查找症状相关的疾病，然后返回这些疾病的用药
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))
            
            # 新增：药物禁忌查询
            elif question_type == 'drug_taboo':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            
            # 新增：药物不良反应查询
            elif question_type == 'drug_adverse_reaction':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            
            # 新增：药物注意事项查询
            elif question_type == 'drug_precaution':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            
            # 新增：特殊人群用药查询
            elif question_type == 'drug_special_population':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            
            # 新增：药物成份查询
            elif question_type == 'drug_component':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            
            # 新增：已知成份查药物
            elif question_type == 'component_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('component'))
            
            # 新增：症状导致疾病查询
            elif question_type == 'symptom_lead_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))
            
            # 新增：科室查询疾病/症状
            elif question_type == 'department_entity':
                sql = self.sql_transfer(question_type, entity_dict.get('department'))
            
            # 新增：部位查询疾病/症状
            elif question_type == 'location_entity':
                sql = self.sql_transfer(question_type, entity_dict.get('location'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2
        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 症状相关疾病的预防方法（两步查询：先找疾病，再找预防）
        elif question_type == 'symptom_disease_prevent':
            # 第一步：通过症状找到相关疾病
            disease_sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return distinct m.name".format(i) for i in entities]
            # 注意：这里返回的SQL需要特殊处理，在answer_search中执行两步查询
            sql = disease_sql

        # 症状相关疾病的用药（两步查询：先找疾病，再找用药）
        elif question_type == 'symptom_disease_drug':
            # 第一步：通过症状找到相关疾病
            disease_sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return distinct m.name".format(i) for i in entities]
            sql = disease_sql
        
        # 新增：药物禁忌查询
        elif question_type == 'drug_taboo':
            sql = ["MATCH (d:Drug)-[r:taboo]->(n) where d.name = '{0}' return d.name, r.name, labels(n) as node_type, n.name".format(i) for i in entities]
        
        # 新增：药物不良反应查询
        elif question_type == 'drug_adverse_reaction':
            sql = ["MATCH (d:Drug)-[r:adverse_reaction]->(n:AdverseReaction) where d.name = '{0}' return d.name, r.name, n.name, r.content".format(i) for i in entities]
        
        # 新增：药物注意事项查询
        elif question_type == 'drug_precaution':
            sql = ["MATCH (d:Drug)-[r:precaution]->(n:Precaution) where d.name = '{0}' return d.name, r.name, n.name, r.content".format(i) for i in entities]
        
        # 新增：特殊人群用药查询
        elif question_type == 'drug_special_population':
            sql = ["MATCH (d:Drug)-[r:special_population]->(n:PatientAttribute) where d.name = '{0}' return d.name, r.name, n.name, r.content".format(i) for i in entities]
        
        # 新增：药物成份查询
        elif question_type == 'drug_component':
            sql = ["MATCH (d:Drug)-[r:contains]->(n:Component) where d.name = '{0}' return d.name, r.name, n.name".format(i) for i in entities]
        
        # 新增：已知成份查药物
        elif question_type == 'component_drug':
            sql = ["MATCH (d:Drug)-[r:contains]->(n:Component) where n.name = '{0}' return d.name, r.name, n.name".format(i) for i in entities]
        
        # 新增：症状导致疾病查询
        elif question_type == 'symptom_lead_disease':
            sql = ["MATCH (s:Symptom)-[r:leads_to]->(d:Disease) where s.name = '{0}' return s.name, r.name, d.name".format(i) for i in entities]
        
        # 新增：科室查询疾病/症状
        elif question_type == 'department_entity':
            sql1 = ["MATCH (dept:Department)-[r:includes]->(d:Disease) where dept.name = '{0}' return dept.name, r.name, d.name, 'Disease' as entity_type".format(i) for i in entities]
            sql2 = ["MATCH (dept:Department)-[r:includes]->(s:Symptom) where dept.name = '{0}' return dept.name, r.name, s.name, 'Symptom' as entity_type".format(i) for i in entities]
            sql = sql1 + sql2
        
        # 新增：部位查询疾病/症状
        elif question_type == 'location_entity':
            sql1 = ["MATCH (loc:Location)-[r:includes]->(d:Disease) where loc.name = '{0}' return loc.name, r.name, d.name, 'Disease' as entity_type".format(i) for i in entities]
            sql2 = ["MATCH (loc:Location)-[r:includes]->(s:Symptom) where loc.name = '{0}' return loc.name, r.name, s.name, 'Symptom' as entity_type".format(i) for i in entities]
            sql = sql1 + sql2

        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
