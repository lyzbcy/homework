import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict', 'disease.txt')
        self.department_path = os.path.join(cur_dir, 'dict', 'department.txt')
        self.check_path = os.path.join(cur_dir, 'dict', 'check.txt')
        self.drug_path = os.path.join(cur_dir, 'dict', 'drug.txt')
        self.food_path = os.path.join(cur_dir, 'dict', 'food.txt')
        self.producer_path = os.path.join(cur_dir, 'dict', 'producer.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict', 'symptom.txt')
        self.deny_path = os.path.join(cur_dir, 'dict', 'deny.txt')
        # 新增字典路径
        self.component_path = os.path.join(cur_dir, 'dict', 'component.txt')
        self.location_path = os.path.join(cur_dir, 'dict', 'location.txt')
        # 加载特征词（使用安全的编码处理）
        def safe_load_dict(file_path):
            """安全加载字典文件，尝试多种编码"""
            encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'utf-8-sig']
            for encoding in encodings:
                try:
                    with open(file_path, encoding=encoding) as f:
                        return [i.strip() for i in f if i.strip()]
                except (UnicodeDecodeError, UnicodeError):
                    continue
            # 如果所有编码都失败，使用 utf-8 并忽略错误
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                return [i.strip() for i in f if i.strip()]
        
        self.disease_wds = safe_load_dict(self.disease_path)
        self.department_wds = safe_load_dict(self.department_path)
        self.check_wds = safe_load_dict(self.check_path)
        self.drug_wds = safe_load_dict(self.drug_path)
        self.food_wds = safe_load_dict(self.food_path)
        self.producer_wds = safe_load_dict(self.producer_path)
        self.symptom_wds = safe_load_dict(self.symptom_path)
        # 新增字典加载
        try:
            self.component_wds = safe_load_dict(self.component_path)
        except:
            self.component_wds = []
        try:
            self.location_wds = safe_load_dict(self.location_path)
        except:
            self.location_wds = []
        self.region_words = set(self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + 
                               self.food_wds + self.producer_wds + self.symptom_wds + self.component_wds + self.location_wds)
        self.deny_words = safe_load_dict(self.deny_path)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        # 新增：禁忌相关疑问词
        self.taboo_qwds = ['禁忌', '不能', '禁止', '避免', '禁用', '不可以', '不能和', '不能与', '不能同时', '不能一起吃', '不能一起用']
        # 新增：不良反应相关疑问词
        self.adverse_qwds = ['不良反应', '副作用', '不良作用', '有什么副作用', '有什么不良反应', '副作用是什么', '不良反应是什么']
        # 新增：注意事项相关疑问词
        self.precaution_qwds = ['注意事项', '注意', '需要注意', '要注意', '注意什么', '需要注意什么']
        # 新增：特殊人群用药相关疑问词
        self.special_population_qwds = ['儿童', '老人', '老年', '孕妇', '妇女', '小孩', '婴幼儿', '儿童能用', '老人能用', '孕妇能用', 
                                         '儿童可以用', '老人可以用', '孕妇可以用', '儿童用药', '老年用药', '妇女用药', '孕妇用药']
        # 新增：成份相关疑问词
        self.component_qwds = ['成份', '成分', '含有', '包含', '有什么成份', '有什么成分', '含有什么', '包含什么']
        # 新增：部位相关疑问词
        self.location_qwds = ['部位', '位置', '哪里', '哪个部位', '什么部位']
        # 新增：症状导致疾病相关疑问词
        self.lead_qwds = ['导致', '引起', '会造成', '会引发', '会得', '会患', '会患上']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # 推荐食品
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        #已知食物找疾病
        if self.check_words(self.food_qwds+self.cure_qwds, question) and 'food' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'food_not_disease'
            else:
                question_type = 'food_do_disease'
            question_types.append(question_type)

        # 推荐药品（支持"吃什么药"这种没有明确疾病的问题）
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)
        elif self.check_words(self.drug_qwds, question) and 'symptom' in types:
            # 对于症状的用药问题，先查找相关疾病，然后返回疾病的用药
            question_type = 'symptom_disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.check_qwds, question) and 'disease' in types:
            question_type = 'disease_check'
            question_types.append(question_type)

        # 已知检查项目查相应疾病
        if self.check_words(self.check_qwds+self.cure_qwds, question) and 'check' in types:
            question_type = 'check_disease'
            question_types.append(question_type)

        #　症状防御（优先匹配疾病，如果没有疾病但有症状，则查找相关疾病的预防方法）
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)
        elif self.check_words(self.prevent_qwds, question) and 'symptom' in types:
            # 对于症状的预防问题，先查找相关疾病，然后返回疾病的预防方法
            question_type = 'symptom_disease_prevent'
            question_types.append(question_type)

        # 疾病医疗周期
        if self.check_words(self.lasttime_qwds, question) and 'disease' in types:
            question_type = 'disease_lasttime'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)

        # 疾病治愈可能性
        if self.check_words(self.cureprob_qwds, question) and 'disease' in types:
            question_type = 'disease_cureprob'
            question_types.append(question_type)

        # 疾病易感染人群
        if self.check_words(self.easyget_qwds, question) and 'disease' in types :
            question_type = 'disease_easyget'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 新增：药物禁忌查询
        if self.check_words(self.taboo_qwds, question) and 'drug' in types:
            question_type = 'drug_taboo'
            question_types.append(question_type)
        
        # 新增：药物不良反应查询
        if self.check_words(self.adverse_qwds, question) and 'drug' in types:
            question_type = 'drug_adverse_reaction'
            question_types.append(question_type)
        
        # 新增：药物注意事项查询
        if self.check_words(self.precaution_qwds, question) and 'drug' in types:
            question_type = 'drug_precaution'
            question_types.append(question_type)
        
        # 新增：特殊人群用药查询
        if self.check_words(self.special_population_qwds, question) and 'drug' in types:
            question_type = 'drug_special_population'
            question_types.append(question_type)
        
        # 新增：药物成份查询
        if self.check_words(self.component_qwds, question) and 'drug' in types:
            question_type = 'drug_component'
            question_types.append(question_type)
        
        # 新增：已知成份查药物
        if self.check_words(self.component_qwds + self.cure_qwds, question) and 'component' in types:
            question_type = 'component_drug'
            question_types.append(question_type)
        
        # 新增：症状导致疾病查询（使用leads_to关系）
        if self.check_words(self.lead_qwds, question) and 'symptom' in types:
            question_type = 'symptom_lead_disease'
            question_types.append(question_type)
        
        # 新增：科室查询疾病/症状
        if self.check_words(self.belong_qwds + self.cure_qwds, question) and 'department' in types:
            question_type = 'department_entity'
            question_types.append(question_type)
        
        # 新增：部位查询疾病/症状
        if self.check_words(self.location_qwds + self.cure_qwds, question) and 'location' in types:
            question_type = 'location_entity'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
            if wd in self.component_wds:
                wd_dict[wd].append('component')
            if wd in self.location_wds:
                wd_dict[wd].append('location')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            if not isinstance(word, str):
                continue
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)