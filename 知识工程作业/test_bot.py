from question_classifier import QuestionClassifier
from question_parser import QuestionPaser
from answer_search import AnswerSearcher

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是医药智能助理，希望可以帮到您。如果没答上来，可联系https://liuhuanyong.github.io/。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    questions = [
        "感冒吃什么药",
        "阿司匹林有什么禁忌",
        "阿司匹林有什么副作用",
        "儿童能吃阿司匹林吗",
        "感冒有什么症状",
        "头痛是哪些病的症状"
    ]
    import traceback
    try:
        for q in questions:
            print(f"Q: {q}")
            print(f"A: {handler.chat_main(q)}")
            print("-" * 20)
    except Exception:
        traceback.print_exc()
