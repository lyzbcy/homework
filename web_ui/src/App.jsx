import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Activity, Info, HelpCircle, Database, ChevronRight, ChevronLeft } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import ForceGraph2D from 'react-force-graph-2d';
import { chatWithBot, getGraphData } from './api';

function App() {
  const [messages, setMessages] = useState([
    { role: 'bot', content: '👋 您好！我是医疗知识图谱智能助手。\n\n我可以回答关于疾病、症状、药品、检查等方面的问题。请问有什么可以帮您？' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [showGraph, setShowGraph] = useState(true);
  const chatEndRef = useRef(null);
  const graphRef = useRef(null);

  const suggestedQuestions = [
    "感冒的症状是什么？",
    "发烧可能是什么病？",
    "感冒怎么治疗？",
    "布洛芬有什么副作用？",
    "阿司匹林有什么禁忌？"
  ];

  useEffect(() => {
    // Load initial graph data
    fetchGraphData();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchGraphData = async () => {
    try {
      const data = await getGraphData();
      // Transform data for react-force-graph if necessary
      // The API returns { nodes: [], links: [] } which is compatible
      setGraphData(data);
    } catch (error) {
      console.error("Failed to load graph data", error);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatWithBot(userMessage.content);
      const botMessage = { role: 'bot', content: response.answer };
      setMessages(prev => [...prev, botMessage]);

      // Refresh graph data after a query (in a real app, we might fetch a subgraph related to the query)
      fetchGraphData();

    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: '抱歉，系统遇到了一些问题，请稍后再试。' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionClick = (question) => {
    setInput(question);
    // Optional: auto send
    // handleSend(); 
  };

  return (
    <div className="flex h-screen bg-gray-100 font-sans overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 flex-shrink-0 hidden md:flex flex-col">
        <div className="p-4 border-b border-gray-200 flex items-center space-x-2">
          <Activity className="text-blue-600" size={24} />
          <h1 className="text-xl font-bold text-gray-800">医疗问答系统</h1>
        </div>

        <div className="p-4 flex-1 overflow-y-auto">
          <div className="mb-6">
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">推荐问题</h2>
            <div className="space-y-2">
              {suggestedQuestions.map((q, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(q)}
                  className="w-full text-left p-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md transition-colors duration-200 truncate"
                  title={q}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">关于系统</h2>
            <div className="text-sm text-gray-600 space-y-2">
              <p className="flex items-center"><Database size={14} className="mr-2" /> 基于 Neo4j 知识图谱</p>
              <p className="flex items-center"><Info size={14} className="mr-2" /> 支持疾病、药品、症状查询</p>
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 text-xs text-gray-400 text-center">
          Medical QA System v2.0
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-white shadow-xl z-10">
        {/* Header for Mobile */}
        <div className="md:hidden p-4 border-b border-gray-200 flex items-center justify-between bg-white">
          <div className="flex items-center space-x-2">
            <Activity className="text-blue-600" size={24} />
            <h1 className="text-lg font-bold text-gray-800">医疗问答</h1>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gray-50">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex max-w-[85%] md:max-w-[70%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-blue-600 ml-3' : 'bg-green-600 mr-3'}`}>
                  {msg.role === 'user' ? <User size={20} className="text-white" /> : <Bot size={20} className="text-white" />}
                </div>

                <div className={`p-4 rounded-2xl shadow-sm ${msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-tl-none'
                  }`}>
                  <ReactMarkdown
                    className="prose prose-sm max-w-none break-words"
                    components={{
                      p: ({ node, ...props }) => <p className={`mb-1 last:mb-0 ${msg.role === 'user' ? 'text-white' : 'text-gray-800'}`} {...props} />
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex flex-row">
                <div className="flex-shrink-0 h-10 w-10 rounded-full bg-green-600 mr-3 flex items-center justify-center">
                  <Bot size={20} className="text-white" />
                </div>
                <div className="bg-white p-4 rounded-2xl rounded-tl-none border border-gray-200 shadow-sm flex items-center">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-gray-200">
          <div className="max-w-4xl mx-auto relative flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="请输入您的问题，例如：感冒吃什么药？"
              className="w-full pl-4 pr-12 py-3 bg-gray-100 border-transparent focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-xl transition-all duration-200 outline-none"
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className={`absolute right-2 p-2 rounded-lg transition-colors duration-200 ${input.trim() && !isLoading
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
            >
              <Send size={20} />
            </button>
          </div>
          <div className="text-center mt-2 text-xs text-gray-400">
            AI 生成内容仅供参考，请遵医嘱
          </div>
        </div>
      </div>

      {/* Graph Toggle Button (Mobile/Desktop) */}
      <button
        onClick={() => setShowGraph(!showGraph)}
        className="absolute top-4 right-4 z-50 bg-white p-2 rounded-full shadow-lg border border-gray-200 hover:bg-gray-50 transition-colors"
        title={showGraph ? "隐藏图谱" : "显示图谱"}
      >
        {showGraph ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>

      {/* Knowledge Graph Panel */}
      {showGraph && (
        <div className="w-96 bg-gray-50 border-l border-gray-200 flex flex-col flex-shrink-0 transition-all duration-300 absolute md:relative right-0 h-full z-20 shadow-xl md:shadow-none">
          <div className="p-4 border-b border-gray-200 bg-white flex justify-between items-center">
            <h3 className="font-bold text-gray-700 flex items-center">
              <Database size={18} className="mr-2 text-purple-600" />
              知识图谱可视化
            </h3>
          </div>
          <div className="flex-1 overflow-hidden relative bg-gray-50">
            {graphData.nodes.length > 0 ? (
              <ForceGraph2D
                ref={graphRef}
                width={384} // w-96 is 24rem = 384px
                height={window.innerHeight - 60}
                graphData={graphData}
                nodeLabel="label"
                nodeColor={node => {
                  const colors = {
                    'Disease': '#ef4444', // red-500
                    'Symptom': '#f59e0b', // amber-500
                    'Drug': '#10b981', // emerald-500
                    'Check': '#8b5cf6', // violet-500
                    'Department': '#ec4899', // pink-500
                    'Food': '#f97316', // orange-500
                    'Producer': '#6366f1' // indigo-500
                  };
                  return colors[node.group] || '#9ca3af';
                }}
                nodeRelSize={6}
                linkColor={() => '#cbd5e1'}
                linkWidth={1.5}
                enableNodeDrag={true}
                cooldownTicks={100}
                onEngineStop={() => graphRef.current?.zoomToFit(400)}
              />
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-gray-400 p-8 text-center">
                <Database size={48} className="mb-4 opacity-20" />
                <p>暂无图谱数据</p>
                <p className="text-xs mt-2">请尝试刷新或提问以加载数据</p>
              </div>
            )}
          </div>
          <div className="p-3 bg-white border-t border-gray-200 text-xs">
            <div className="flex flex-wrap gap-2 justify-center">
              <span className="flex items-center"><span className="w-2 h-2 rounded-full bg-red-500 mr-1"></span>疾病</span>
              <span className="flex items-center"><span className="w-2 h-2 rounded-full bg-amber-500 mr-1"></span>症状</span>
              <span className="flex items-center"><span className="w-2 h-2 rounded-full bg-emerald-500 mr-1"></span>药品</span>
              <span className="flex items-center"><span className="w-2 h-2 rounded-full bg-violet-500 mr-1"></span>检查</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
