import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Activity, Info, Database, ChevronRight, ChevronLeft, Sparkles, Stethoscope, Pill, Microscope, FileText, Layers } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import ForceGraph2D from 'react-force-graph-2d';
import { chatWithBot, getGraphData } from './api';
import ProjectShowcase from './ProjectShowcase';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: '👋 您好！我是您的智能医疗助手。\n\n我可以为您解答关于**疾病**、**症状**、**药品**及**检查**等方面的疑问。\n\n💡 *试着问我："感冒有哪些症状？" 或 "阿司匹林有什么禁忌？"*'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [showGraph, setShowGraph] = useState(true);
  const [currentView, setCurrentView] = useState('chat'); // 'chat' | 'showcase'

  const chatEndRef = useRef(null);
  const graphRef = useRef(null);
  const graphWrapperRef = useRef(null);
  const [graphDimensions, setGraphDimensions] = useState({ width: 400, height: 600 });

  const suggestedQuestions = [
    { text: "感冒的症状是什么？", icon: <Stethoscope size={14} /> },
    { text: "发烧可能是什么病？", icon: <Activity size={14} /> },
    { text: "感冒怎么治疗？", icon: <Pill size={14} /> },
    { text: "布洛芬有什么副作用？", icon: <Info size={14} /> },
    { text: "CT检查注意事项", icon: <Microscope size={14} /> }
  ];

  useEffect(() => {
    if (currentView === 'chat') {
      fetchGraphData();
      updateGraphDimensions();
      window.addEventListener('resize', updateGraphDimensions);
      return () => window.removeEventListener('resize', updateGraphDimensions);
    }
  }, [showGraph, currentView]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentView]);

  const updateGraphDimensions = () => {
    if (graphWrapperRef.current) {
      setGraphDimensions({
        width: graphWrapperRef.current.offsetWidth,
        height: graphWrapperRef.current.offsetHeight
      });
    }
  };

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchGraphData = async (query = null) => {
    try {
      const data = await getGraphData(query);
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

      // Try to extract a potential entity from input (naive approach: take the first 2-4 chars or the whole input)
      // Better: search for the whole input. The server uses CONTAINS, so if input is "感冒", it matches "感冒".
      // If input is "感冒吃什么药", it matches nothing.
      // Let's pass the input anyway. If it returns empty, maybe fallback to random?
      // For now, let's pass the input. 
      fetchGraphData(userMessage.content);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: '😓 抱歉，系统遇到了一些技术问题，请稍后再试。' }]);
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

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-800 overflow-hidden relative">
      {/* Decorative Background Elements */}
      <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-teal-50 to-transparent pointer-events-none opacity-60 z-0"></div>

      {/* Sidebar - Glassmorphism */}
      <div className="w-72 bg-white/80 backdrop-blur-md border-r border-slate-200 flex-shrink-0 hidden md:flex flex-col z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
        <div className="p-6 border-b border-slate-100 flex items-center space-x-3">
          <div className="bg-gradient-to-tr from-teal-500 to-emerald-400 p-2 rounded-xl shadow-lg shadow-teal-500/20">
            <Activity className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800 tracking-tight">智医问答</h1>
            <p className="text-xs text-teal-600 font-medium">Medical KG Assistant</p>
          </div>
        </div>

        <div className="p-5 flex-1 overflow-y-auto custom-scrollbar">
          <div className="mb-8">
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 flex items-center">
              <Sparkles size={12} className="mr-2" /> 猜你想问
            </h2>
            <div className="space-y-2.5">
              {suggestedQuestions.map((q, index) => (
                <button
                  key={index}
                  onClick={() => {
                    setCurrentView('chat');
                    setInput(q.text);
                  }}
                  className="w-full text-left p-3 text-sm text-slate-600 hover:bg-teal-50 hover:text-teal-700 rounded-xl transition-all duration-200 border border-transparent hover:border-teal-100 shadow-sm hover:shadow-md group flex items-center"
                >
                  <span className="mr-3 text-slate-400 group-hover:text-teal-500 transition-colors">{q.icon}</span>
                  <span className="truncate">{q.text}</span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">功能切换</h2>
            <div className="space-y-3">
              <button
                onClick={() => setCurrentView('showcase')}
                className={`w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center group ${currentView === 'showcase'
                  ? 'bg-teal-50 border-teal-200 shadow-sm'
                  : 'bg-white border-slate-100 hover:border-teal-200 hover:shadow-md'
                  }`}
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 transition-colors ${currentView === 'showcase' ? 'bg-teal-100 text-teal-600' : 'bg-indigo-50 text-indigo-500 group-hover:bg-indigo-100'
                  }`}>
                  <Layers size={16} />
                </div>
                <div>
                  <div className={`font-medium transition-colors ${currentView === 'showcase' ? 'text-teal-800' : 'text-slate-700'
                    }`}>项目全景台</div>
                  <div className="text-xs text-slate-400">原理展示 & 搭建教学</div>
                </div>
                <ChevronRight size={14} className={`ml-auto transition-transform ${currentView === 'showcase' ? 'text-teal-400 rotate-90' : 'text-slate-300 group-hover:text-teal-400'
                  }`} />
              </button>

              <button
                onClick={() => setCurrentView('chat')}
                className={`w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center group ${currentView === 'chat'
                  ? 'bg-teal-50 border-teal-200 shadow-sm'
                  : 'bg-white border-slate-100 hover:border-teal-200 hover:shadow-md'
                  }`}
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 transition-colors ${currentView === 'chat' ? 'bg-teal-100 text-teal-600' : 'bg-pink-50 text-pink-500 group-hover:bg-pink-100'
                  }`}>
                  <Activity size={16} />
                </div>
                <div>
                  <div className={`font-medium transition-colors ${currentView === 'chat' ? 'text-teal-800' : 'text-slate-700'
                    }`}>智能问答</div>
                  <div className="text-xs text-slate-400">Knowledge Chat</div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-slate-100">
          <div className="bg-slate-100/50 rounded-lg p-3 text-center">
            <p className="text-xs text-slate-400">版本 v2.2.0 (Showcase)</p>
          </div>
        </div>
      </div>

      {/* Main Content Area (Chat or Showcase) */}
      <div className="flex-1 flex flex-col min-w-0 z-10 relative">
        {currentView === 'showcase' ? (
          <ProjectShowcase />
        ) : (
          <>
            {/* Mobile Header */}
            <div className="md:hidden p-4 bg-white/90 backdrop-blur-sm border-b border-slate-200 flex items-center justify-between sticky top-0 z-20">
              <div className="flex items-center space-x-2">
                <div className="bg-teal-500 p-1.5 rounded-lg">
                  <Activity className="text-white" size={18} />
                </div>
                <h1 className="text-lg font-bold text-slate-800">智医问答</h1>
              </div>
              <button
                onClick={() => setShowGraph(!showGraph)}
                className={`p-2 rounded-lg ${showGraph ? 'bg-teal-100 text-teal-600' : 'bg-slate-100 text-slate-500'}`}
              >
                <Database size={20} />
              </button>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scroll-smooth">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fadeInUp`}
                  style={{ animationDuration: '0.3s', animationFillMode: 'both' }}
                >
                  <div className={`flex max-w-[90%] md:max-w-[75%] lg:max-w-[65%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} items-end gap-3`}>

                    {/* Avatar */}
                    <div className={`flex-shrink-0 h-9 w-9 rounded-full flex items-center justify-center shadow-sm ${msg.role === 'user'
                      ? 'bg-gradient-to-br from-blue-500 to-blue-600 ring-2 ring-white'
                      : 'bg-gradient-to-br from-teal-400 to-emerald-500 ring-2 ring-white'
                      }`}>
                      {msg.role === 'user' ? <User size={18} className="text-white" /> : <Bot size={18} className="text-white" />}
                    </div>

                    {/* Bubble */}
                    <div className={`px-5 py-3.5 shadow-sm text-sm md:text-base leading-relaxed ${msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-2xl rounded-tr-sm shadow-blue-500/20'
                      : 'bg-white text-slate-700 border border-slate-200/60 rounded-2xl rounded-tl-sm shadow-slate-200/40'
                      }`}>
                      <ReactMarkdown
                        className={`prose ${msg.role === 'user' ? 'prose-invert' : 'prose-slate'} prose-sm max-w-none break-words`}
                        components={{
                          p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
                          ul: ({ node, ...props }) => <ul className="pl-4 list-disc mb-2" {...props} />,
                          li: ({ node, ...props }) => <li className="mb-1" {...props} />,
                          strong: ({ node, ...props }) => <strong className={`font-semibold ${msg.role === 'user' ? 'text-blue-100' : 'text-teal-600'}`} {...props} />
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  </div>
                </div>
              ))}

              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="flex flex-row items-end gap-3">
                    <div className="flex-shrink-0 h-9 w-9 rounded-full bg-gradient-to-br from-teal-400 to-emerald-500 flex items-center justify-center shadow-sm ring-2 ring-white">
                      <Bot size={18} className="text-white" />
                    </div>
                    <div className="bg-white px-4 py-3 rounded-2xl rounded-tl-sm border border-slate-200/60 shadow-sm">
                      <div className="flex space-x-1.5 items-center h-4">
                        <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} className="h-4" />
            </div>

            {/* Input Area */}
            <div className="p-4 md:p-6 bg-white/80 backdrop-blur-md border-t border-slate-200 z-20">
              <div className="max-w-4xl mx-auto relative group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-teal-300 to-blue-300 rounded-2xl opacity-20 group-focus-within:opacity-50 transition duration-300 blur"></div>
                <div className="relative flex items-center bg-white rounded-xl shadow-sm border border-slate-200">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="描述您的症状或相关疾病，例如：感冒吃什么药？"
                    className="w-full pl-5 pr-14 py-4 bg-transparent focus:outline-none text-slate-700 placeholder:text-slate-400"
                    disabled={isLoading}
                  />
                  <button
                    onClick={handleSend}
                    disabled={!input.trim() || isLoading}
                    className={`absolute right-2 p-2.5 rounded-lg transition-all duration-200 ${input.trim() && !isLoading
                      ? 'bg-gradient-to-r from-teal-500 to-blue-500 text-white shadow-lg shadow-teal-500/30 hover:shadow-teal-500/40 transform hover:-translate-y-0.5'
                      : 'bg-slate-100 text-slate-300 cursor-not-allowed'
                      }`}
                  >
                    <Send size={18} />
                  </button>
                </div>
                <div className="text-center mt-3 flex items-center justify-center space-x-1 text-xs text-slate-400">
                  <Info size={12} />
                  <span>AI 诊断结果仅供参考，不作为最终医疗建议</span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Graph Toggle - Desktop (Only show in chat mode) */}
      {currentView === 'chat' && (
        <>
          <button
            onClick={() => setShowGraph(!showGraph)}
            className={`absolute top-6 right-6 z-50 p-2.5 rounded-full shadow-lg border transition-all duration-300 hidden md:flex ${showGraph
              ? 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              : 'bg-teal-500 text-white border-transparent hover:bg-teal-600 rotate-180'
              }`}
            title={showGraph ? "收起图谱" : "展开图谱"}
          >
            <ChevronRight size={20} />
          </button>

          {/* Knowledge Graph Panel */}
          <div className={`fixed inset-y-0 right-0 w-full md:w-[450px] bg-white/95 backdrop-blur-xl border-l border-slate-200 shadow-2xl transform transition-transform duration-300 ease-in-out z-40 flex flex-col ${showGraph ? 'translate-x-0' : 'translate-x-full'
            }`}>

            {/* Graph Header */}
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-white/50">
              <div className="flex items-center space-x-2">
                <div className="bg-indigo-100 p-1.5 rounded-lg text-indigo-600">
                  <Database size={18} />
                </div>
                <h3 className="font-bold text-slate-700">知识图谱可视化</h3>
              </div>
              <button onClick={() => setShowGraph(false)} className="md:hidden p-2 text-slate-400 hover:text-slate-600">
                <ChevronRight size={20} />
              </button>
            </div>

            {/* Legend */}
            <div className="px-4 py-3 bg-slate-50 border-b border-slate-100 grid grid-cols-4 gap-2 text-[10px] text-slate-500 font-medium">
              {[
                { label: '疾病', color: '#ef4444' },
                { label: '症状', color: '#f59e0b' },
                { label: '药品', color: '#10b981' },
                { label: '检查', color: '#8b5cf6' },
                { label: '科室', color: '#ec4899' },
                { label: '食物', color: '#f97316' },
                { label: '厂商', color: '#6366f1' },
                { label: '其他', color: '#9ca3af' },
              ].map(item => (
                <div key={item.label} className="flex items-center space-x-1.5">
                  <span className="w-2.5 h-2.5 rounded-full shadow-sm" style={{ backgroundColor: item.color }}></span>
                  <span>{item.label}</span>
                </div>
              ))}
            </div>

            {/* Graph Area */}
            <div className="flex-1 relative bg-slate-50/30 overflow-hidden" ref={graphWrapperRef}>
              {graphData.nodes.length > 0 ? (
                <ForceGraph2D
                  ref={graphRef}
                  width={graphDimensions.width}
                  height={graphDimensions.height}
                  graphData={graphData}
                  nodeLabel="label"
                  nodeColor={node => {
                    const colors = {
                      'Disease': '#ef4444',
                      'Symptom': '#f59e0b',
                      'Drug': '#10b981',
                      'Check': '#8b5cf6',
                      'Department': '#ec4899',
                      'Food': '#f97316',
                      'Producer': '#6366f1'
                    };
                    return colors[node.group] || '#9ca3af';
                  }}
                  nodeRelSize={5}
                  linkColor={() => '#cbd5e1'}
                  linkWidth={1.5}
                  linkDirectionalParticles={2}
                  linkDirectionalParticleSpeed={0.005}
                  backgroundColor="rgba(0,0,0,0)"
                />
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-slate-400 p-8 text-center space-y-4">
                  <div className="bg-slate-100 p-4 rounded-full">
                    <Database size={32} className="opacity-40" />
                  </div>
                  <div>
                    <p className="font-medium text-slate-500">暂无图谱数据</p>
                    <p className="text-xs mt-1">图谱将随着您的提问动态生成</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
