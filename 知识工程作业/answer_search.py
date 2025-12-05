from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "tangyudiadid0"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            
            # 处理需要两步查询的问题类型
            if question_type == 'symptom_disease_prevent':
                # 第一步：通过症状找到相关疾病
                diseases = []
                for query in queries:
                    ress = self.g.run(query).data()
                    diseases.extend([r.get('m.name') for r in ress if r.get('m.name')])
                
                # 第二步：查询这些疾病的预防方法
                if diseases:
                    prevent_queries = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(d) for d in set(diseases)]
                    for query in prevent_queries:
                        ress = self.g.run(query).data()
                        answers += ress
                    # 修改问题类型以便使用正确的格式化函数
                    question_type = 'disease_prevent'
            
            elif question_type == 'symptom_disease_drug':
                # 第一步：通过症状找到相关疾病
                diseases = []
                for query in queries:
                    ress = self.g.run(query).data()
                    diseases.extend([r.get('m.name') for r in ress if r.get('m.name')])
                
                # 第二步：查询这些疾病的用药
                if diseases:
                    drug_queries1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(d) for d in set(diseases)]
                    drug_queries2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(d) for d in set(diseases)]
                    for query in drug_queries1 + drug_queries2:
                        ress = self.g.run(query).data()
                        answers += ress
                    # 修改问题类型以便使用正确的格式化函数
                    question_type = 'disease_drug'
            
            else:
                # 普通查询
                for query in queries:
                    ress = self.g.run(query).data()
                    answers += ress
            
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        
        elif question_type == 'symptom_disease_prevent':
            # 这种情况已经在search_main中转换为disease_prevent处理
            pass

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']

            final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        
        # 新增：药物禁忌查询
        elif question_type == 'drug_taboo':
            taboo_items = []
            for i in answers:
                node_type = i.get('node_type', [])
                if node_type:
                    node_type = node_type[0] if isinstance(node_type, list) else str(node_type)
                else:
                    node_type = '未知'
                taboo_name = i.get('n.name', '')
                if taboo_name:
                    taboo_items.append(f"{taboo_name}({node_type})")
            subject = answers[0]['d.name'] if answers else ''
            if taboo_items:
                final_answer = '{0}的禁忌包括：{1}'.format(subject, '；'.join(list(set(taboo_items))[:self.num_limit]))
            else:
                final_answer = '{0}暂无禁忌信息'.format(subject)
        
        # 新增：药物不良反应查询
        elif question_type == 'drug_adverse_reaction':
            adverse_items = []
            for i in answers:
                adverse_name = i.get('n.name', '')
                content = i.get('r.content', '')
                if adverse_name:
                    if content and content != adverse_name:
                        adverse_items.append(f"{adverse_name}：{content}")
                    else:
                        adverse_items.append(adverse_name)
            subject = answers[0]['d.name'] if answers else ''
            if adverse_items:
                final_answer = '{0}的不良反应包括：{1}'.format(subject, '；'.join(list(set(adverse_items))[:self.num_limit]))
            else:
                final_answer = '{0}暂无不良反应信息'.format(subject)
        
        # 新增：药物注意事项查询
        elif question_type == 'drug_precaution':
            precaution_items = []
            for i in answers:
                precaution_name = i.get('n.name', '')
                content = i.get('r.content', '')
                if precaution_name:
                    if content and content != precaution_name:
                        precaution_items.append(f"{precaution_name}：{content}")
                    else:
                        precaution_items.append(precaution_name)
            subject = answers[0]['d.name'] if answers else ''
            if precaution_items:
                final_answer = '{0}的注意事项包括：{1}'.format(subject, '；'.join(list(set(precaution_items))[:self.num_limit]))
            else:
                final_answer = '{0}暂无注意事项信息'.format(subject)
        
        # 新增：特殊人群用药查询
        elif question_type == 'drug_special_population':
            population_items = {}
            for i in answers:
                population = i.get('n.name', '')
                rel_name = i.get('r.name', '')
                content = i.get('r.content', '')
                if population:
                    if population not in population_items:
                        population_items[population] = []
                    if content:
                        population_items[population].append(content)
            subject = answers[0]['d.name'] if answers else ''
            if population_items:
                result_parts = []
                for pop, contents in population_items.items():
                    if contents:
                        result_parts.append(f"{pop}：{'；'.join(list(set(contents))[:3])}")
                    else:
                        result_parts.append(f"{pop}：请咨询医生")
                final_answer = '{0}的特殊人群用药信息：\n{1}'.format(subject, '\n'.join(result_parts))
            else:
                final_answer = '{0}暂无特殊人群用药信息'.format(subject)
        
        # 新增：药物成份查询
        elif question_type == 'drug_component':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['d.name'] if answers else ''
            if desc:
                final_answer = '{0}的成份包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer = '{0}暂无成份信息'.format(subject)
        
        # 新增：已知成份查药物
        elif question_type == 'component_drug':
            desc = [i['d.name'] for i in answers]
            subject = answers[0]['n.name'] if answers else ''
            if desc:
                final_answer = '含有{0}成份的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer = '暂无含有{0}成份的药品信息'.format(subject)
        
        # 新增：症状导致疾病查询
        elif question_type == 'symptom_lead_disease':
            desc = [i['d.name'] for i in answers]
            subject = answers[0]['s.name'] if answers else ''
            if desc:
                final_answer = '症状{0}可能导致以下疾病：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer = '症状{0}暂无相关疾病信息'.format(subject)
        
        # 新增：科室查询疾病/症状
        elif question_type == 'department_entity':
            diseases = []
            symptoms = []
            for i in answers:
                entity_type = i.get('entity_type', '')
                entity_name = i.get('d.name') or i.get('s.name', '')
                if entity_type == 'Disease' and entity_name:
                    diseases.append(entity_name)
                elif entity_type == 'Symptom' and entity_name:
                    symptoms.append(entity_name)
            subject = answers[0].get('dept.name', '') if answers else ''
            result_parts = []
            if diseases:
                result_parts.append(f"疾病：{'；'.join(list(set(diseases))[:self.num_limit])}")
            if symptoms:
                result_parts.append(f"症状：{'；'.join(list(set(symptoms))[:self.num_limit])}")
            if result_parts:
                final_answer = '{0}相关的：\n{1}'.format(subject, '\n'.join(result_parts))
            else:
                final_answer = '{0}暂无相关信息'.format(subject)
        
        # 新增：部位查询疾病/症状
        elif question_type == 'location_entity':
            diseases = []
            symptoms = []
            for i in answers:
                entity_type = i.get('entity_type', '')
                entity_name = i.get('d.name') or i.get('s.name', '')
                if entity_type == 'Disease' and entity_name:
                    diseases.append(entity_name)
                elif entity_type == 'Symptom' and entity_name:
                    symptoms.append(entity_name)
            subject = answers[0].get('loc.name', '') if answers else ''
            result_parts = []
            if diseases:
                result_parts.append(f"疾病：{'；'.join(list(set(diseases))[:self.num_limit])}")
            if symptoms:
                result_parts.append(f"症状：{'；'.join(list(set(symptoms))[:self.num_limit])}")
            if result_parts:
                final_answer = '{0}部位相关的：\n{1}'.format(subject, '\n'.join(result_parts))
            else:
                final_answer = '{0}部位暂无相关信息'.format(subject)

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()