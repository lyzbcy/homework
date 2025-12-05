import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Brain, Terminal, Search, Database, MessageSquare,
    MapPin, FileText, ChevronRight, Play, Check, Copy,
    Lightbulb, Microscope, Zap, BookOpen, Layers
} from 'lucide-react';

const ProjectShowcase = () => {
    const [activeTab, setActiveTab] = useState('story'); // 'story' | 'guide'

    return (
        <div className="flex flex-col h-full bg-slate-50 relative overflow-hidden font-sans">
            {/* Dynamic Background */}
            <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-teal-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
                <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '2s' }}></div>
            </div>

            {/* Header */}
            <header className="flex-shrink-0 px-8 py-6 bg-white/70 backdrop-blur-xl border-b border-slate-200 z-10 flex justify-between items-center">
                <div>
                    <h2 className="text-2xl font-bold text-slate-800 flex items-center">
                        <Layers className="mr-3 text-teal-600" />
                        系统全景解密
                        <span className="ml-3 px-2 py-0.5 text-xs font-bold text-teal-600 bg-teal-50 rounded-full border border-teal-100 uppercase tracking-wider">Education Mode</span>
                    </h2>
                    <p className="text-slate-500 mt-1 ml-9 text-sm">
                        像侦探一样思考：揭秘 AI 如何听懂你的话并找到答案
                    </p>
                </div>

                {/* Tab Switcher */}
                <div className="flex bg-slate-100/80 p-1 rounded-xl">
                    <TabButton
                        active={activeTab === 'story'}
                        onClick={() => setActiveTab('story')}
                        icon={<Brain size={16} />}
                        label="原理·侦探故事"
                    />
                    <TabButton
                        active={activeTab === 'guide'}
                        onClick={() => setActiveTab('guide')}
                        icon={<Terminal size={16} />}
                        label="实战·特工手册"
                    />
                </div>
            </header>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 md:p-8 relative z-0 custom-scrollbar">
                <AnimatePresence mode="wait">
                    {activeTab === 'story' ? <StoryView key="story" /> : <GuideView key="guide" />}
                </AnimatePresence>
            </div>
        </div>
    );
};

const TabButton = ({ active, onClick, icon, label }) => (
    <button
        onClick={onClick}
        className={`flex items-center px-4 py-2 rounded-lg text-sm font-bold transition-all duration-300 ${active
                ? 'bg-white text-teal-700 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
    >
        <span className="mr-2">{icon}</span>
        {label}
    </button>
);

// --- Story View: The Detective Analogy ---
const StoryView = () => {
    const [step, setStep] = useState(0);

    const steps = [
        {
            id: 0,
            title: "1.虽然我听得懂人话，但并不完全懂",
            subtitle: "用户输入 (Input)",
            desc: "就像侦探接到了一个模糊的委托电话。用户说了一句我们能听懂的话，但对于计算机来说，这只是一串没有意义的字符串。",
            icon: <MessageSquare className="text-blue-500" size={32} />,
            content: <StepContentInput />
        },
        {
            id: 1,
            title: "2. 寻找关键线索 (NER)",
            subtitle: "实体识别 (Entity Recognition)",
            desc: "侦探拿出放大镜，在句子中寻找关键词。'感冒' 是一种病，'吃什么药' 代表意图。我们将这些关键词提取出来，贴上标签。",
            icon: <Search className="text-purple-500" size={32} />,
            content: <StepContentNER />
        },
        {
            id: 2,
            title: "3. 连接证据墙 (KG)",
            subtitle: "图谱查询 (Graph Query)",
            desc: "侦探来到证据墙（知识图谱）前。墙上挂满了卡片（节点），红线（关系）将它们连在一起。我们找到 '感冒' 这张卡片，顺着 '推荐用药' 这根红线，找到了 '感冒灵'。",
            icon: <Database className="text-emerald-500" size={32} />,
            content: <StepContentGraph />
        },
        {
            id: 3,
            title: "4. 生成结案报告",
            subtitle: "答案生成 (Generation)",
            desc: "侦探将找到的线索整理成一份通俗易懂的报告，反馈给委托人。",
            icon: <FileText className="text-teal-500" size={32} />,
            content: <StepContentReport />
        }
    ];

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="max-w-6xl mx-auto h-full flex flex-col md:flex-row gap-6"
        >
            {/* Left: Navigation Steps */}
            <div className="w-full md:w-1/3 flex flex-col gap-4">
                {steps.map((s, index) => (
                    <button
                        key={index}
                        onClick={() => setStep(index)}
                        className={`text-left p-5 rounded-2xl border-2 transition-all duration-300 relative overflow-hidden group ${step === index
                                ? 'bg-white border-teal-500 shadow-xl shadow-teal-500/10 scale-105 z-10'
                                : 'bg-white/50 border-transparent hover:bg-white hover:border-teal-200 opacity-70 hover:opacity-100'
                            }`}
                    >
                        <div className="flex items-start justify-between mb-2">
                            <div className={`p-2 rounded-lg ${step === index ? 'bg-teal-50' : 'bg-slate-100'}`}>
                                {s.icon}
                            </div>
                            <span className={`text-4xl font-black opacity-10 ${step === index ? 'text-teal-500' : 'text-slate-300'}`}>0{index + 1}</span>
                        </div>
                        <h3 className={`font-bold text-lg mb-1 ${step === index ? 'text-slate-800' : 'text-slate-600'}`}>{s.subtitle}</h3>
                        <p className="text-xs text-slate-500 line-clamp-2">{s.title}</p>

                        {/* Progress Bar for active step */}
                        {step === index && (
                            <motion.div
                                layoutId="active-bar"
                                className="absolute left-0 top-0 bottom-0 w-1.5 bg-teal-500"
                            />
                        )}
                    </button>
                ))}
            </div>

            {/* Right: Interactive Viz Stage */}
            <div className="flex-1 bg-white rounded-3xl border border-slate-200 shadow-2xl p-8 relative overflow-hidden flex flex-col">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                    <Brain size={200} />
                </div>

                <div className="relative z-10 flex-1 flex flex-col justify-center">
                    <h2 className="text-2xl font-bold text-slate-800 mb-2">{steps[step].title}</h2>
                    <p className="text-slate-500 mb-8 text-lg leading-relaxed max-w-2xl">{steps[step].desc}</p>

                    <div className="bg-slate-50 rounded-2xl border border-slate-100 p-8 min-h-[300px] flex items-center justify-center relative overflow-hidden">
                        {/* Grid Background */}
                        <div className="absolute inset-0 z-0" style={{ backgroundImage: 'radial-gradient(#cbd5e1 1px, transparent 1px)', backgroundSize: '20px 20px', opacity: 0.3 }}></div>

                        <div className="z-10 w-full max-w-xl">
                            {steps[step].content}
                        </div>
                    </div>
                </div>

                <div className="mt-6 flex justify-between items-center text-sm text-slate-400">
                    <span>Step {step + 1} / 4</span>
                    <div className="flex gap-2">
                        <button
                            onClick={() => setStep(Math.max(0, step - 1))}
                            disabled={step === 0}
                            className="px-4 py-2 rounded-lg hover:bg-slate-100 disabled:opacity-30 disabled:cursor-not-allowed font-medium transition-colors"
                        >
                            上一步
                        </button>
                        <button
                            onClick={() => setStep(Math.min(3, step + 1))}
                            disabled={step === 3}
                            className="px-6 py-2 rounded-lg bg-teal-600 text-white shadow-lg shadow-teal-500/30 hover:bg-teal-700 disabled:opacity-50 disabled:cursor-not-allowed font-bold transition-all transform active:scale-95 flex items-center"
                        >
                            下一步 <ChevronRight size={16} className="ml-1" />
                        </button>
                    </div>
                </div>
            </div>
        </motion.div>
    );
};

// --- Story Components ---
const StepContentInput = () => (
    <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="flex flex-col items-center space-y-6"
    >
        <div className="text-6xl animate-bounce">📱</div>
        <div className="bg-white px-8 py-4 rounded-full shadow-xl border border-blue-100 text-xl font-medium text-slate-700 relative">
            <div>"感冒吃什么药？"</div>
            <div className="absolute -top-3 -right-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full animate-pulse">New Message</div>
        </div>
        <div className="flex flex-col items-center">
            <div className="h-8 w-0.5 bg-slate-300"></div>
            <div className="bg-slate-800 text-white px-4 py-1 rounded text-xs font-mono">Raw String Data</div>
        </div>
    </motion.div>
);

const StepContentNER = () => (
    <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="flex items-center justify-center space-x-2 text-2xl font-bold"
    >
        <motion.span
            className="px-4 py-2 rounded-lg bg-red-100 text-red-600 border-2 border-red-200 relative group cursor-help"
            whileHover={{ scale: 1.1 }}
        >
            感冒
            <span className="absolute -bottom-6 left-0 w-full text-center text-[10px] font-mono text-red-500 uppercase">Disease</span>
        </motion.span>
        <span className="text-slate-300">+</span>
        <motion.span
            className="px-4 py-2 rounded-lg bg-green-100 text-green-600 border-2 border-green-200 relative group cursor-help"
            whileHover={{ scale: 1.1 }}
        >
            吃什么药
            <span className="absolute -bottom-6 left-0 w-full text-center text-[10px] font-mono text-green-500 uppercase">Intent</span>
        </motion.span>
        <div className="absolute top-0 right-0">
            <div className="flex items-center text-xs text-slate-400 space-x-2">
                <Search size={14} className="animate-spin-slow" />
                <span>Scanning...</span>
            </div>
        </div>
    </motion.div>
);

const StepContentGraph = () => (
    <div className="relative w-full h-64 flex items-center justify-center">
        {/* Nodes */}
        <motion.div
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="absolute left-10 md:left-20 flex flex-col items-center z-10"
        >
            <div className="w-16 h-16 rounded-full bg-red-500 border-4 border-white shadow-lg flex items-center justify-center text-white font-bold text-lg">
                感冒
            </div>
            <span className="bg-red-100 text-red-600 text-xs px-2 py-0.5 rounded-full mt-2 font-bold">Disease</span>
        </motion.div>

        <motion.div
            initial={{ width: 0 }}
            animate={{ width: 140 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="h-1 bg-slate-300 relative overflow-hidden"
        >
            <div className="absolute top-0 left-0 h-full w-full bg-teal-400 animate-loading-bar"></div>
            <div className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-bold text-slate-400 bg-white px-2 py-1 rounded shadow-sm">
                recommend_drug
            </div>
        </motion.div>

        <motion.div
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 1 }}
            className="absolute right-10 md:right-20 flex flex-col items-center z-10"
        >
            <div className="w-16 h-16 rounded-full bg-green-500 border-4 border-white shadow-lg flex items-center justify-center text-white font-bold text-lg text-center leading-tight">
                感冒灵<br /><span className="text-[10px]">颗粒</span>
            </div>
            <span className="bg-green-100 text-green-600 text-xs px-2 py-0.5 rounded-full mt-2 font-bold">Drug</span>
        </motion.div>
    </div>
);

const StepContentReport = () => (
    <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white rounded-xl shadow-lg border border-teal-100 p-6 max-w-md w-full relative overflow-hidden"
    >
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-teal-400 to-blue-500"></div>
        <div className="flex items-start space-x-4">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-400 to-emerald-500 flex items-center justify-center text-white flex-shrink-0">
                <BotIcon />
            </div>
            <div className="flex-1 space-y-2">
                <div className="h-2 w-1/4 bg-slate-100 rounded animate-pulse"></div>
                <p className="text-slate-600 text-sm leading-relaxed">
                    <span className="font-bold text-slate-800">感冒</span> 常用药物包括：
                    <span className="text-green-600 font-bold bg-green-50 px-1 rounded mx-1">感冒灵颗粒</span>、
                    <span className="text-green-600 font-bold bg-green-50 px-1 rounded mx-1">阿莫西林</span> 等。
                    请遵医嘱使用。
                </p>
            </div>
        </div>
        <div className="mt-4 flex justify-end">
            <div className="text-xs text-slate-300 flex items-center">
                <Check size={12} className="mr-1" /> Generated in 0.05s
            </div>
        </div>
    </motion.div>
);

const BotIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"></path></svg>
);


// --- Guide View: The Agent Handbook ---
const GuideView = () => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-4xl mx-auto"
        >
            <div className="mb-8 text-center">
                <h3 className="text-3xl font-black text-slate-800 mb-2">特工行动手册</h3>
                <p className="text-slate-500">按照以下步骤部署你的专属医疗 AI</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <GuideCard
                    level="Level 1"
                    title="准备武器库 (Environment)"
                    icon={<Zap className="text-yellow-500" />}
                    tasks={[
                        "安装 Python 3.8+",
                        "安装 JDK 11 (用于图数据库)",
                        "下载 & 安装 Neo4j Desktop"
                    ]}
                />
                <GuideCard
                    level="Level 2"
                    title="填装弹药 (Dependencies)"
                    icon={<Layers className="text-blue-500" />}
                    code="pip install -r requirements.txt"
                    tasks={[
                        "安装 py2neo (连接数据库)",
                        "安装 fastapi (后端服务)",
                        "安装 jieba (中文分词)"
                    ]}
                />
                <GuideCard
                    level="Level 3"
                    title="构建情报网 (Graph ETL)"
                    icon={<Database className="text-red-500" />}
                    code="python build_medicalgraph.py"
                    tasks={[
                        "读取 JSON 医疗数据",
                        "创建 44,000+ 个节点",
                        "建立 27,000+ 条关系"
                    ]}
                />
                <GuideCard
                    level="Level 4"
                    title="启动作战中心 (Deploy)"
                    icon={<Play className="text-green-500" />}
                    code="python server.py"
                    tasks={[
                        "加载分类器模型",
                        "开启 8000 端口监听",
                        "启动 React 前端界面 (npm run dev)"
                    ]}
                />
            </div>

            <div className="mt-12 p-6 bg-gradient-to-r from-teal-500 to-emerald-500 rounded-2xl text-white text-center shadow-xl">
                <h4 className="text-xl font-bold mb-2">🎉 任务完成！</h4>
                <p className="opacity-90 text-sm mb-4">你现在拥有了一个基于知识图谱的智能医疗专家系统。</p>
                <button className="bg-white text-teal-600 px-6 py-2 rounded-full font-bold shadow-lg hover:shadow-xl hover:scale-105 transition-all">
                    开始体验
                </button>
            </div>
        </motion.div>
    );
};

const GuideCard = ({ level, title, icon, tasks, code }) => (
    <div className="bg-white rounded-xl border border-slate-100 shadow-lg shadow-slate-200/50 p-6 hover:shadow-xl transition-shadow relative overflow-hidden group">
        <div className="absolute top-0 right-0 bg-slate-100 px-3 py-1 rounded-bl-xl text-xs font-bold text-slate-400 group-hover:bg-teal-500 group-hover:text-white transition-colors">
            {level}
        </div>
        <div className="flex items-center mb-4">
            <div className="p-3 bg-slate-50 rounded-lg mr-4 group-hover:scale-110 transition-transform">
                {icon}
            </div>
            <h4 className="font-bold text-slate-800 text-lg">{title}</h4>
        </div>

        <ul className="space-y-2 mb-4">
            {tasks.map((task, i) => (
                <li key={i} className="flex items-start text-sm text-slate-500">
                    <Check size={14} className="mr-2 mt-0.5 text-teal-500 flex-shrink-0" />
                    {task}
                </li>
            ))}
        </ul>

        {code && (
            <div className="bg-slate-800 rounded-lg p-3 flex items-center justify-between group/code cursor-pointer" onClick={() => navigator.clipboard.writeText(code)}>
                <code className="text-xs font-mono text-teal-300 truncate mr-2">{code}</code>
                <Copy size={12} className="text-slate-500 group-hover/code:text-white transition-colors" />
            </div>
        )}
    </div>
);

export default ProjectShowcase;
