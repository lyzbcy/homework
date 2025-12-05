"""
基于知识图谱的医药问答系统 - PyQt5图形界面
现代化的聊天界面，支持问题提示和知识图谱可视化
"""

import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QLabel, QScrollArea, QFrame, QMessageBox, QDialog,
                             QListWidget, QListWidgetItem, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QTextCursor
from chatbot_graph import ChatBotGraph
from py2neo import Graph
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# 设置matplotlib支持中文
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class AnswerThread(QThread):
    """后台线程处理问答，避免界面卡顿"""
    answer_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, chatbot, question):
        super().__init__()
        self.chatbot = chatbot
        self.question = question
    
    def run(self):
        try:
            answer = self.chatbot.chat_main(self.question)
            self.answer_ready.emit(answer)
        except Exception as e:
            self.error_occurred.emit(f"错误: {str(e)}")


class ChatBubble(QFrame):
    """聊天消息气泡"""
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setup_ui(text)
    
    def setup_ui(self, text):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # 消息标签
        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        # 设置样式
        if self.is_user:
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #007AFF;
                    color: white;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 14px;
                    max-width: 500px;
                }
            """)
            message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #E5E5EA;
                    color: #000000;
                    padding: 12px 16px;
                    border-radius: 18px;
                    font-size: 14px;
                    max-width: 500px;
                }
            """)
            message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        layout.addWidget(message_label)
        self.setLayout(layout)


class QuestionHintWidget(QWidget):
    """问题提示组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("💡 您可以询问以下问题：")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; margin-bottom: 10px;")
        layout.addWidget(title)
        
        questions = [
            "疾病症状：感冒的症状是什么？",
            "症状疾病：发烧可能是什么病？",
            "疾病原因：感冒的原因是什么？",
            "疾病预防：如何预防感冒？",
            "疾病治疗：感冒怎么治疗？",
            "疾病药品：感冒用什么药？",
            "疾病食物：感冒吃什么食物？",
            "疾病检查：感冒需要做什么检查？",
            "疾病科室：感冒应该挂什么科？",
            "症状预防：如何预防发烧？",
            "症状用药：发烧用什么药？",
            "药物禁忌：阿司匹林有什么禁忌？",
            "不良反应：布洛芬有什么不良反应？",
            "注意事项：阿司匹林有什么注意事项？",
            "特殊人群：阿司匹林儿童能用吗？",
            "药物成份：布洛芬含有什么成份？",
            "症状导致疾病：发烧会导致什么疾病？",
            "科室查询：心内科看什么病？",
            "部位查询：头部容易得什么病？"
        ]
        
        for q in questions:
            btn = QPushButton(q)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    margin: 5px 0;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: white;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                    border-color: #007AFF;
                }
            """)
            btn.clicked.connect(lambda checked, text=q: self.on_question_clicked(text))
            layout.addWidget(btn)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def on_question_clicked(self, question):
        """点击问题提示时，将问题填入输入框"""
        if self.parent_window:
            self.parent_window.input_line.setText(question)
            self.parent_window.input_line.setFocus()


class KnowledgeGraphDialog(QDialog):
    """知识图谱可视化对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("知识图谱可视化")
        self.setMinimumSize(1000, 700)
        self.setup_ui()
        self.load_graph()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel("📊 医疗知识图谱可视化")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 说明文字
        info = QLabel("展示知识图谱中的疾病、症状、药品等实体及其关系")
        info.setStyleSheet("font-size: 12px; color: #666; padding: 5px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # 图表区域
        self.figure = Figure(figsize=(10, 7))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # 控制按钮
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 刷新图谱")
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #007AFF;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        refresh_btn.clicked.connect(self.load_graph)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #ccc;
                color: black;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
        """)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def load_graph(self):
        """从Neo4j加载知识图谱并可视化"""
        try:
            # 连接Neo4j
            g = Graph("bolt://localhost:7687", auth=("neo4j", "tangyudiadid0"))
            
            # 查询部分节点和关系
            query = """
            MATCH (n)-[r]->(m)
            WHERE n.name IS NOT NULL AND m.name IS NOT NULL
            RETURN n, r, m
            LIMIT 200
            """
            
            result = g.run(query).data()
            
            if not result:
                self.show_empty_graph()
                return
            
            # 创建NetworkX图
            G = nx.Graph()
            node_types = {}
            edge_types = {}
            
            for record in result:
                n = record['n']
                m = record['m']
                r = record['r']
                
                n_name = n.get('name', 'Unknown')
                m_name = m.get('name', 'Unknown')
                n_type = list(n.labels)[0] if n.labels else 'Unknown'
                m_type = list(m.labels)[0] if m.labels else 'Unknown'
                r_type = type(r).__name__
                
                # 添加节点
                if n_name not in G:
                    G.add_node(n_name, node_type=n_type)
                    node_types[n_name] = n_type
                
                if m_name not in G:
                    G.add_node(m_name, node_type=m_type)
                    node_types[m_name] = m_type
                
                # 添加边
                if not G.has_edge(n_name, m_name):
                    G.add_edge(n_name, m_name, relation=r_type)
                    edge_types[(n_name, m_name)] = r_type
            
            # 绘制图谱
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # 使用spring布局，根据节点数量调整参数
            if G.number_of_nodes() > 100:
                pos = nx.spring_layout(G, k=0.5, iterations=30, seed=42)
            else:
                pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
            
            # 按节点类型设置颜色
            color_map = {
                'Disease': '#FF6B6B',
                'Symptom': '#4ECDC4',
                'Drug': '#95E1D3',
                'Food': '#F38181',
                'Check': '#AA96DA',
                'Department': '#FCBAD3',
                'Producer': '#FFD93D'
            }
            
            node_colors = [color_map.get(node_types.get(node, 'Unknown'), '#CCCCCC') 
                          for node in G.nodes()]
            
            # 根据节点数量调整节点大小
            if G.number_of_nodes() > 100:
                node_size = 200
                font_size = 6
            else:
                node_size = 300
                font_size = 8
            
            # 绘制边
            nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.2, width=0.3, 
                                  edge_color='gray')
            
            # 绘制节点
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, 
                                  node_size=node_size, alpha=0.9)
            
            # 绘制标签（只显示部分重要节点，避免过于拥挤）
            max_labels = min(30, G.number_of_nodes())
            important_nodes = list(G.nodes())[:max_labels]
            labels = {node: node[:10] + '...' if len(node) > 10 else node 
                     for node in important_nodes}
            nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=font_size, 
                                   font_weight='bold')
            
            # 添加图例
            legend_elements = []
            for node_type, color in color_map.items():
                if any(node_types.get(n) == node_type for n in G.nodes()):
                    legend_elements.append(plt.Line2D([0], [0], marker='o', 
                                                      color='w', markerfacecolor=color, 
                                                      markersize=10, label=node_type))
            
            if legend_elements:
                ax.legend(handles=legend_elements, loc='upper left', 
                         bbox_to_anchor=(1.02, 1), fontsize=9)
            
            ax.set_title(f'医疗知识图谱可视化\n(节点数: {G.number_of_nodes()}, 边数: {G.number_of_edges()})', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.axis('off')
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            self.show_error(str(e))
    
    def show_empty_graph(self):
        """显示空图谱提示"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, '暂无数据\n请确保Neo4j数据库已启动\n并已构建知识图谱', 
                ha='center', va='center', fontsize=14, 
                transform=ax.transAxes)
        ax.axis('off')
        self.canvas.draw()
    
    def show_error(self, error_msg):
        """显示错误信息"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, f'加载失败\n{error_msg}', 
                ha='center', va='center', fontsize=12, 
                transform=ax.transAxes, color='red')
        ax.axis('off')
        self.canvas.draw()


class MedicalChatBotGUI(QMainWindow):
    """医疗问答系统主窗口"""
    def __init__(self):
        super().__init__()
        self.chatbot = None
        self.init_chatbot()
        self.setup_ui()
        self.add_welcome_message()
    
    def init_chatbot(self):
        """初始化问答系统"""
        try:
            self.chatbot = ChatBotGraph()
        except Exception as e:
            QMessageBox.warning(self, "警告", 
                              f"初始化问答系统失败：{str(e)}\n请确保Neo4j数据库已启动！")
    
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("医疗知识图谱问答系统")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧：问题提示面板（可滚动）
        hint_scroll_area = QScrollArea()
        hint_scroll_area.setWidgetResizable(True)
        hint_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        hint_scroll_area.setMinimumWidth(280)
        hint_scroll_area.setMaximumWidth(320)
        hint_scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border-right: 1px solid #ddd;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 8px;
                margin: 20px 0 20px 0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
            }
        """)
        hint_widget = QuestionHintWidget(self)
        hint_scroll_area.setWidget(hint_widget)
        splitter.addWidget(hint_scroll_area)
        
        # 右侧：聊天区域
        chat_container = QWidget()
        chat_layout = QVBoxLayout()
        chat_container.setLayout(chat_layout)
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        chat_layout.addWidget(toolbar)
        
        # 聊天消息区域
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F5F5F5;
            }
        """)
        
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_widget.setLayout(self.chat_layout)
        self.chat_area.setWidget(self.chat_widget)
        
        chat_layout.addWidget(self.chat_area)
        
        # 底部输入区域
        input_container = self.create_input_area()
        chat_layout.addWidget(input_container)
        
        splitter.addWidget(chat_container)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        # 设置分割器比例
        splitter.setSizes([300, 900])
    
    def create_toolbar(self):
        """创建顶部工具栏"""
        toolbar = QFrame()
        toolbar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #ddd;
                padding: 10px;
            }
        """)
        layout = QHBoxLayout()
        
        title = QLabel("🏥 医疗知识图谱智能问答系统")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # 关于按钮
        about_btn = QPushButton("📊 关于")
        about_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #007AFF;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
        """)
        about_btn.clicked.connect(self.show_about)
        layout.addWidget(about_btn)
        
        toolbar.setLayout(layout)
        return toolbar
    
    def create_input_area(self):
        """创建输入区域"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #ddd;
                padding: 15px;
            }
        """)
        layout = QHBoxLayout()
        
        # 输入框
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("请输入您的问题...")
        self.input_line.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 25px;
                font-size: 14px;
                background-color: #F9F9F9;
            }
            QLineEdit:focus {
                border-color: #007AFF;
                background-color: white;
            }
        """)
        self.input_line.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_line)
        
        # 发送按钮
        send_btn = QPushButton("发送")
        send_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background-color: #007AFF;
                color: white;
                border-radius: 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056CC;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(send_btn)
        
        container.setLayout(layout)
        return container
    
    def add_welcome_message(self):
        """添加欢迎消息"""
        welcome_text = """👋 欢迎使用医疗知识图谱智能问答系统！

我可以回答以下类型的问题：
• 疾病症状查询
• 症状疾病诊断
• 疾病原因分析
• 疾病预防建议
• 疾病治疗方案
• 疾病用药推荐
• 疾病饮食建议
• 疾病检查项目
• 疾病科室推荐

请在左侧选择问题示例，或直接输入您的问题。"""
        
        self.add_message(welcome_text, is_user=False)
    
    def add_message(self, text, is_user=True):
        """添加消息到聊天区域"""
        # 创建消息容器
        message_container = QWidget()
        message_layout = QHBoxLayout()
        message_layout.setContentsMargins(10, 5, 10, 5)
        
        if is_user:
            message_layout.addStretch()
            bubble = ChatBubble(text, is_user=True)
            message_layout.addWidget(bubble)
        else:
            bubble = ChatBubble(text, is_user=False)
            message_layout.addWidget(bubble)
            message_layout.addStretch()
        
        message_container.setLayout(message_layout)
        
        # 添加到聊天区域
        self.chat_layout.addWidget(message_container)
        
        # 滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """发送消息"""
        question = self.input_line.text().strip()
        if not question:
            return
        
        # 添加用户消息
        self.add_message(question, is_user=True)
        
        # 清空输入框
        self.input_line.clear()
        
        # 显示思考中
        self.thinking_container = QWidget()
        thinking_layout = QHBoxLayout()
        thinking_layout.setContentsMargins(10, 5, 10, 5)
        thinking_bubble = ChatBubble("正在思考中...", is_user=False)
        thinking_layout.addWidget(thinking_bubble)
        thinking_layout.addStretch()
        self.thinking_container.setLayout(thinking_layout)
        self.chat_layout.addWidget(self.thinking_container)
        self.scroll_to_bottom()
        
        # 在后台线程处理问答
        if self.chatbot:
            self.answer_thread = AnswerThread(self.chatbot, question)
            self.answer_thread.answer_ready.connect(self.on_answer_ready)
            self.answer_thread.error_occurred.connect(self.on_answer_error)
            self.answer_thread.start()
        else:
            self.on_answer_error("系统未初始化，请检查Neo4j连接！")
    
    def on_answer_ready(self, answer):
        """答案准备就绪"""
        # 移除思考中消息
        self.chat_layout.removeWidget(self.thinking_container)
        self.thinking_container.deleteLater()
        
        # 添加答案消息
        self.add_message(answer, is_user=False)
    
    def on_answer_error(self, error):
        """答案错误"""
        # 移除思考中消息
        self.chat_layout.removeWidget(self.thinking_container)
        self.thinking_container.deleteLater()
        
        # 添加错误消息
        self.add_message(error, is_user=False)
    
    def show_about(self):
        """显示关于对话框和知识图谱可视化"""
        dialog = KnowledgeGraphDialog(self)
        dialog.exec_()


def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    window = MedicalChatBotGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

