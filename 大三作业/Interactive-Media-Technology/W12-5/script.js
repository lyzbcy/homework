// 游戏状态
const gameState = {
    apiType: 'deepseek',
    apiKey: '',
    apiUrl: 'https://api.deepseek.com/v1/chat/completions',
    words: [],
    currentStory: '',
    storyType: 'general',
    storyLength: 500,
    storyStyle: 'creative',
    history: [],
    currentRating: 0,
    demoMode: false
};

// 预设关键词
const presets = {
    fantasy: ['魔法', '巨龙', '勇士', '城堡', '冒险'],
    'sci-fi': ['太空', 'AI', '未来', '星际', '科技'],
    romance: ['相遇', '心动', '永恒', '温柔', '承诺'],
    mystery: ['谜题', '线索', '真相', '侦探', '秘密']
};

// 推荐词语库
const suggestions = {
    general: ['梦想', '希望', '勇气', '友谊', '成长', '探索', '发现', '创造'],
    fantasy: ['魔法', '咒语', '精灵', '巫师', '宝藏', '冒险', '传说', '神秘'],
    'sci-fi': ['机器人', '飞船', '星球', '时间', '维度', '能量', '数据', '虚拟'],
    romance: ['爱情', '温柔', '拥抱', '微笑', '承诺', '永恒', '心动', '浪漫'],
    mystery: ['秘密', '线索', '真相', '推理', '悬疑', '调查', '证据', '谜团'],
    comedy: ['搞笑', '幽默', '滑稽', '欢乐', '笑声', '趣事', '玩笑', '轻松'],
    drama: ['情感', '冲突', '选择', '成长', '人生', '命运', '挑战', '坚持']
};

// DOM元素
const elements = {
    startScreen: document.getElementById('startScreen'),
    gameScreen: document.getElementById('gameScreen'),
    startBtn: document.getElementById('startBtn'),
    backBtn: document.getElementById('backBtn'),
    apiKeyInput: document.getElementById('apiKey'),
    apiKeySection: document.getElementById('apiKeySection'),
    apiUrlInput: document.getElementById('apiUrl'),
    toggleKey: document.getElementById('toggleKey'),
    wordInput: document.getElementById('wordInput'),
    wordTags: document.getElementById('wordTags'),
    wordCount: document.getElementById('wordCount'),
    generateBtn: document.getElementById('generateBtn'),
    clearBtn: document.getElementById('clearBtn'),
    addWordBtn: document.getElementById('addWordBtn'),
    storyContainer: document.getElementById('storyContainer'),
    storyMeta: document.getElementById('storyMeta'),
    storyActions: document.getElementById('storyActions'),
    saveBtn: document.getElementById('saveBtn'),
    regenerateBtn: document.getElementById('regenerateBtn'),
    shareBtn: document.getElementById('shareBtn'),
    rateBtn: document.getElementById('rateBtn'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    apiOptions: document.querySelectorAll('.api-option'),
    modeOptions: document.querySelectorAll('.mode-option'),
    demoNotice: document.getElementById('demoNotice'),
    quickStartBtns: document.querySelectorAll('.quick-start-btn'),
    storyType: document.getElementById('storyType'),
    storyLength: document.getElementById('storyLength'),
    lengthValue: document.getElementById('lengthValue'),
    storyStyle: document.getElementById('storyStyle'),
    suggestions: document.getElementById('suggestions'),
    historyList: document.getElementById('historyList'),
    rateModal: document.getElementById('rateModal'),
    submitRating: document.getElementById('submitRating'),
    cancelRating: document.getElementById('cancelRating')
};

// 初始化
function init() {
    loadHistory();
    setupEventListeners();
    updateSuggestions();
    updateWordCount();
}

// 设置事件监听
function setupEventListeners() {
    // 运行模式切换
    elements.modeOptions.forEach(option => {
        option.addEventListener('click', () => {
            elements.modeOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            const mode = option.dataset.mode;
            gameState.demoMode = mode === 'demo';
            
            if (gameState.demoMode) {
                elements.apiKeySection.style.display = 'none';
                elements.demoNotice.style.display = 'block';
            } else {
                elements.apiKeySection.style.display = 'block';
                elements.demoNotice.style.display = 'none';
            }
        });
    });
    
    // API类型切换
    elements.apiOptions.forEach(option => {
        option.addEventListener('click', () => {
            elements.apiOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            gameState.apiType = option.dataset.api;
            updateApiUrl();
        });
    });

    // API Key显示/隐藏
    elements.toggleKey.addEventListener('click', () => {
        const type = elements.apiKeyInput.type === 'password' ? 'text' : 'password';
        elements.apiKeyInput.type = type;
        elements.toggleKey.textContent = type === 'password' ? '👁️' : '🙈';
    });

    // API URL输入
    elements.apiUrlInput.addEventListener('change', (e) => {
        gameState.apiUrl = e.target.value || gameState.apiUrl;
    });

    // 快速开始按钮
    elements.quickStartBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const preset = btn.dataset.preset;
            if (presets[preset]) {
                gameState.words = [...presets[preset]];
                renderWords();
                updateWordCount();
                showNotification('已加载预设关键词！');
            }
        });
    });

    // 开始游戏
    elements.startBtn.addEventListener('click', startGame);

    // 返回设置
    elements.backBtn.addEventListener('click', () => {
        elements.startScreen.classList.add('active');
        elements.gameScreen.classList.remove('active');
    });

    // 添加词语
    elements.wordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addWord();
        }
    });

    elements.addWordBtn.addEventListener('click', addWord);

    // 生成故事
    elements.generateBtn.addEventListener('click', generateStory);

    // 清空词语
    elements.clearBtn.addEventListener('click', clearWords);

    // 保存故事
    elements.saveBtn.addEventListener('click', saveStory);

    // 重新生成
    elements.regenerateBtn.addEventListener('click', generateStory);

    // 分享故事
    elements.shareBtn.addEventListener('click', shareStory);

    // 评分
    elements.rateBtn.addEventListener('click', () => {
        elements.rateModal.classList.remove('hidden');
    });

    elements.cancelRating.addEventListener('click', () => {
        elements.rateModal.classList.add('hidden');
        gameState.currentRating = 0;
        updateStars();
    });

    // 星级评分
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('click', () => {
            gameState.currentRating = parseInt(star.dataset.rating);
            updateStars();
        });
    });

    elements.submitRating.addEventListener('click', submitRating);

    // 故事类型变化
    elements.storyType.addEventListener('change', (e) => {
        gameState.storyType = e.target.value;
        updateSuggestions();
    });

    // 故事长度滑块
    elements.storyLength.addEventListener('input', (e) => {
        gameState.storyLength = parseInt(e.target.value);
        elements.lengthValue.textContent = `${gameState.storyLength}字`;
    });

    // 故事风格变化
    elements.storyStyle.addEventListener('change', (e) => {
        gameState.storyStyle = e.target.value;
    });
}

// 更新API URL
function updateApiUrl() {
    if (gameState.apiType === 'deepseek') {
        elements.apiUrlInput.value = 'https://api.deepseek.com/v1/chat/completions';
        gameState.apiUrl = 'https://api.deepseek.com/v1/chat/completions';
    } else if (gameState.apiType === 'dashscope') {
        elements.apiUrlInput.value = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation';
        gameState.apiUrl = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation';
    }
}

// 开始游戏
function startGame() {
    if (!gameState.demoMode) {
        const apiKey = elements.apiKeyInput.value.trim();
        if (!apiKey) {
            showNotification('请输入API Key或选择演示模式', 'error');
            return;
        }
        gameState.apiKey = apiKey;
        gameState.apiUrl = elements.apiUrlInput.value.trim() || gameState.apiUrl;
    } else {
        gameState.apiKey = '';
        showNotification('已进入演示模式，使用本地故事生成器', 'success');
    }

    elements.startScreen.classList.remove('active');
    elements.gameScreen.classList.add('active');
    
    // 显示演示模式标识
    const demoBadge = document.getElementById('demoModeBadge');
    if (gameState.demoMode) {
        demoBadge.style.display = 'flex';
    } else {
        demoBadge.style.display = 'none';
    }
    
    showNotification('欢迎来到文字构建师！', 'success');
}

// 添加词语
function addWord() {
    const word = elements.wordInput.value.trim();
    
    if (!word) return;

    // 处理逗号或空格分隔的多个词语
    const words = word.split(/[,\s]+/).filter(w => w.trim());
    
    let added = false;
    words.forEach(w => {
        if (w && !gameState.words.includes(w)) {
            gameState.words.push(w);
            renderWordTag(w);
            added = true;
        }
    });

    if (added) {
        elements.wordInput.value = '';
        updateWordCount();
        updateSuggestions();
    }
}

// 渲染词语标签
function renderWordTag(word) {
    const tag = document.createElement('div');
    tag.className = 'word-tag';
    tag.innerHTML = `
        <span>${word}</span>
        <button class="remove-btn" data-word="${word}">×</button>
    `;
    
    tag.querySelector('.remove-btn').addEventListener('click', () => {
        removeWord(word);
    });
    
    elements.wordTags.appendChild(tag);
}

// 移除词语
function removeWord(word) {
    gameState.words = gameState.words.filter(w => w !== word);
    renderWords();
    updateWordCount();
    updateSuggestions();
}

// 渲染所有词语
function renderWords() {
    elements.wordTags.innerHTML = '';
    gameState.words.forEach(word => renderWordTag(word));
}

// 清空词语
function clearWords() {
    if (gameState.words.length === 0) return;
    
    if (confirm('确定要清空所有词语吗？')) {
        gameState.words = [];
        renderWords();
        updateWordCount();
        updateSuggestions();
        showNotification('已清空所有词语');
    }
}

// 更新词语计数
function updateWordCount() {
    elements.wordCount.textContent = gameState.words.length;
}

// 更新推荐词语
function updateSuggestions() {
    const type = gameState.storyType;
    const words = suggestions[type] || suggestions.general;
    const availableWords = words.filter(w => !gameState.words.includes(w));
    
    elements.suggestions.innerHTML = '';
    
    if (availableWords.length === 0) {
        return;
    }
    
    availableWords.slice(0, 8).forEach(word => {
        const tag = document.createElement('div');
        tag.className = 'suggestion-tag';
        tag.textContent = word;
        tag.addEventListener('click', () => {
            if (!gameState.words.includes(word)) {
                gameState.words.push(word);
                renderWordTag(word);
                updateWordCount();
                updateSuggestions();
            }
        });
        elements.suggestions.appendChild(tag);
    });
}

// 显示加载
function showLoading() {
    elements.loadingOverlay.classList.remove('hidden');
}

// 隐藏加载
function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

// 生成故事
async function generateStory() {
    if (gameState.words.length === 0) {
        showNotification('请至少输入一个词语', 'error');
        return;
    }

    if (!gameState.demoMode && !gameState.apiKey) {
        showNotification('请先配置API Key或选择演示模式', 'error');
        elements.startScreen.classList.add('active');
        elements.gameScreen.classList.remove('active');
        return;
    }

    showLoading();

    try {
        let story;
        if (gameState.demoMode) {
            // 演示模式：使用本地生成器
            story = await generateLocalStory(gameState.words);
        } else {
            // API模式：调用真实API
            story = await callAIAPI(gameState.words);
        }
        
        gameState.currentStory = story;
        displayStory(story);
        saveToHistory();
        showNotification('故事生成成功！', 'success');
    } catch (error) {
        console.error('生成故事失败:', error);
        let errorMsg = '生成故事失败: ';
        if (error.message) {
            errorMsg += error.message;
        } else {
            errorMsg += '网络错误或API配置有误，请检查API Key和网络连接';
        }
        showNotification(errorMsg, 'error');
        elements.storyContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">❌</div>
                <p>${escapeHtml(errorMsg)}</p>
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// 本地故事生成器（演示模式）
async function generateLocalStory(words) {
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));
    
    const type = gameState.storyType;
    const length = gameState.storyLength;
    const style = gameState.storyStyle;
    
    // 故事开头模板
    const storyBeginnings = {
        fantasy: [
            `在遥远的${words[0] || '魔法'}世界中，`,
            `古老的${words[0] || '城堡'}中，`,
            `在${words[0] || '森林'}深处，`,
            `传说中，${words[0] || '神秘'}的${words[1] || '力量'}`
        ],
        'sci-fi': [
            `公元${words[0] || '2088'}年，`,
            `未来的${words[0] || '地球'}上，`,
            `在${words[0] || '星际'}旅行的时代，`,
            `${words[0] || '太空'}站中，`
        ],
        romance: [
            `那是一个${words[0] || '春天'}的午后，`,
            `${words[0] || '多年'}后，`,
            `在${words[0] || '雨夜'}中，`,
            `${words[0] || '阳光'}明媚的${words[1] || '早晨'}，`
        ],
        mystery: [
            `${words[0] || '深夜'}，`,
            `在${words[0] || '废弃'}的${words[1] || '建筑'}中，`,
            `${words[0] || '调查'}进行到关键时刻，`,
            `当${words[0] || '线索'}出现时，`
        ],
        comedy: [
            `这是一个关于${words[0] || '搞笑'}的故事。`,
            `${words[0] || '意外'}的一天，`,
            `因为${words[0] || '误会'}，`,
            `突然，${words[0] || '有趣'}的事情发生了。`
        ],
        drama: [
            `在${words[0] || '人生'}的十字路口，`,
            `${words[0] || '命运'}的转折改变了`,
            `面对${words[0] || '挑战'}，`,
            `在${words[0] || '困难'}面前，`
        ],
        general: [
            `这是一个关于${words[0] || '梦想'}和${words[1] || '希望'}的故事。`,
            `在${words[0] || '探索'}的过程中，`,
            `通过${words[0] || '友谊'}和${words[1] || '合作'}，`,
            `${words[0] || '生活'}中，`
        ]
    };
    
    // 构建故事
    let story = '';
    const beginnings = storyBeginnings[type] || storyBeginnings.general;
    const beginning = beginnings[Math.floor(Math.random() * beginnings.length)];
    story += beginning;
    
    // 构建主体部分
    const mainParts = buildMainStory(words, type);
    story += mainParts;
    
    // 构建结尾
    const endings = buildEnding(words, type);
    story += endings;
    
    // 调整长度
    story = adjustStoryLength(story, length);
    
    // 根据风格调整
    if (style === 'poetic') {
        story = addPoeticTouch(story);
    } else if (style === 'detailed') {
        story = addDetails(story, words);
    } else if (style === 'concise') {
        story = simplifyStory(story);
    }
    
    return story;
}

// 构建故事主体
function buildMainStory(words, type) {
    let main = '';
    const usedWords = new Set();
    
    words.forEach((word, index) => {
        if (usedWords.has(word)) return;
        usedWords.add(word);
        
        const connectors = ['，', '。', '；'];
        const connector = connectors[index % connectors.length];
        
        if (index === 0) {
            main += `${word}出现了。`;
        } else if (index === 1) {
            main += `这时，${word}成为了关键。`;
        } else if (index === 2) {
            main += `随着${word}的到来，`;
        } else if (index === 3) {
            main += `故事围绕着${word}展开。`;
        } else {
            main += `${word}让情节更加${['精彩', '复杂', '有趣', '深刻'][index % 4]}`;
        }
        
        if (index < words.length - 1) {
            main += ' ';
        }
    });
    
    return main;
}

// 构建结尾
function buildEnding(words, type) {
    const endings = {
        fantasy: `最终，${words[0] || '一切'}都得到了${words[1] || '解决'}，${words[2] || '世界'}恢复了${words[3] || '和平'}。`,
        'sci-fi': `真相大白，${words[0] || '人类'}和${words[1] || '科技'}共同${words[2] || '前进'}。`,
        romance: `${words[0] || '他们'}终于走到了一起，${words[1] || '爱情'}如${words[2] || '阳光'}般温暖。`,
        mystery: `谜团解开，${words[0] || '真相'}浮出水面，${words[1] || '正义'}得到${words[2] || '伸张'}。`,
        comedy: `最后，${words[0] || '笑声'}充满了${words[1] || '整个'}空间，${words[2] || '欢乐'}无限。`,
        drama: `经历了${words[0] || '风雨'}，${words[1] || '主角'}终于${words[2] || '成长'}了。`,
        general: `这个故事告诉我们，${words[0] || '坚持'}和${words[1] || '努力'}能够${words[2] || '改变'}一切。`
    };
    
    return endings[type] || endings.general;
}

// 调整故事长度
function adjustStoryLength(story, targetLength) {
    const currentLength = story.length;
    
    if (currentLength < targetLength * 0.7) {
        // 需要扩展
        const expansion = generateStoryExpansion([], '', Math.max(targetLength - currentLength, 150));
        story += ' ' + expansion;
    } else if (currentLength > targetLength * 1.3) {
        // 太长，截取
        story = story.substring(0, targetLength) + '...';
    }
    
    return story;
}

// 生成故事扩展内容
function generateStoryExpansion(words, type, targetLength) {
    const connectors = ['。', '，', '；'];
    const details = [
        `在这个过程中，${words[0] || '他们'}经历了${words[1] || '许多'}${words[2] || '挑战'}。`,
        `每一步都充满了${words[0] || '未知'}和${words[1] || '惊喜'}。`,
        `最终，${words[0] || '真相'}大白，${words[1] || '一切'}都有了${words[2] || '答案'}。`,
        `这个故事告诉我们，${words[0] || '坚持'}和${words[1] || '努力'}能够${words[2] || '改变'}${words[3] || '命运'}。`
    ];
    
    let expansion = '';
    let currentLength = 0;
    let detailIndex = 0;
    
    while (currentLength < targetLength && detailIndex < details.length * 2) {
        const detail = details[detailIndex % details.length];
        expansion += detail;
        currentLength += detail.length;
        detailIndex++;
        
        if (currentLength < targetLength) {
            expansion += connectors[Math.floor(Math.random() * connectors.length)];
        }
    }
    
    return expansion;
}

// 添加诗意
function addPoeticTouch(story) {
    return story.replace(/。/g, '，如诗如画。').replace(/，/g, '，如流水般，');
}

// 添加细节
function addDetails(story, words) {
    const detailPhrases = [
        `细节之处，${words[0] || '可见'}${words[1] || '用心'}。`,
        `每一个${words[0] || '瞬间'}都${words[1] || '值得'}${words[2] || '铭记'}。`
    ];
    return story + ' ' + detailPhrases.join(' ');
}

// 简化故事
function simplifyStory(story) {
    return story.replace(/，[^，。]{10,}，/g, '，').replace(/。[^。]{20,}。/g, '。');
}

// 调用AI API
async function callAIAPI(words) {
    const typeNames = {
        'general': '通用',
        'fantasy': '奇幻',
        'sci-fi': '科幻',
        'romance': '爱情',
        'mystery': '悬疑',
        'comedy': '喜剧',
        'drama': '剧情'
    };
    
    const styleNames = {
        'creative': '富有创意和想象力',
        'detailed': '详细生动，注重细节',
        'concise': '简洁明了，重点突出',
        'poetic': '富有诗意和文学性'
    };
    
    const prompt = `请根据以下关键词，创作一个${typeNames[gameState.storyType]}类型的${styleNames[gameState.storyStyle]}故事。故事应该自然地融合这些词语，让它们成为故事的重要组成部分。关键词：${words.join('、')}。请用中文回答，故事长度约${gameState.storyLength}字。`;

    if (gameState.apiType === 'deepseek') {
        return await callDeepSeekAPI(prompt);
    } else if (gameState.apiType === 'dashscope') {
        return await callDashScopeAPI(prompt);
    }
}

// 调用DeepSeek API
async function callDeepSeekAPI(prompt) {
    const response = await fetch(gameState.apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${gameState.apiKey}`
        },
        body: JSON.stringify({
            model: 'deepseek-chat',
            messages: [
                {
                    role: 'system',
                    content: '你是一位富有创造力的故事创作大师，擅长根据关键词创作引人入胜的故事。'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            temperature: 0.8,
            max_tokens: Math.min(gameState.storyLength * 2, 2000)
        })
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ error: { message: '请求失败' } }));
        throw new Error(error.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].message.content.trim();
}

// 调用阿里百炼API
async function callDashScopeAPI(prompt) {
    const response = await fetch(gameState.apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${gameState.apiKey}`
        },
        body: JSON.stringify({
            model: 'qwen-turbo',
            input: {
                messages: [
                    {
                        role: 'system',
                        content: '你是一位富有创造力的故事创作大师，擅长根据关键词创作引人入胜的故事。'
                    },
                    {
                        role: 'user',
                        content: prompt
                    }
                ]
            },
            parameters: {
                temperature: 0.8,
                max_tokens: Math.min(gameState.storyLength * 2, 2000),
                result_format: 'message'
            }
        })
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ error: { message: '请求失败' } }));
        throw new Error(error.error?.message || error.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    // 兼容不同的响应格式
    if (data.output && data.output.choices && data.output.choices[0]) {
        return data.output.choices[0].message.content.trim();
    } else if (data.output && data.output.text) {
        return data.output.text.trim();
    } else if (data.choices && data.choices[0]) {
        return data.choices[0].message.content.trim();
    } else {
        throw new Error('无法解析API响应');
    }
}

// 显示故事
function displayStory(story) {
    if (!story || story.trim() === '') {
        elements.storyContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <p>生成的故事为空，请重试</p>
            </div>
        `;
        return;
    }
    
    const date = new Date().toLocaleString('zh-CN');
    elements.storyMeta.innerHTML = `
        <span>类型: ${getTypeName(gameState.storyType)}</span>
        <span>•</span>
        <span>${date}</span>
    `;
    
    elements.storyContainer.innerHTML = `
        <div class="story-content">${escapeHtml(story)}</div>
    `;
    
    elements.storyActions.style.display = 'flex';
}

// 获取类型名称
function getTypeName(type) {
    const names = {
        'general': '通用',
        'fantasy': '奇幻',
        'sci-fi': '科幻',
        'romance': '爱情',
        'mystery': '悬疑',
        'comedy': '喜剧',
        'drama': '剧情'
    };
    return names[type] || '通用';
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 保存故事
function saveStory() {
    if (!gameState.currentStory) {
        showNotification('没有可保存的故事', 'error');
        return;
    }

    const content = `关键词：${gameState.words.join('、')}\n类型：${getTypeName(gameState.storyType)}\n长度：${gameState.storyLength}字\n风格：${gameState.storyStyle}\n\n${gameState.currentStory}`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `故事_${new Date().getTime()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    showNotification('故事已保存！', 'success');
}

// 分享故事
function shareStory() {
    if (!gameState.currentStory) {
        showNotification('没有可分享的故事', 'error');
        return;
    }

    const text = `我创作了一个故事：\n\n关键词：${gameState.words.join('、')}\n\n${gameState.currentStory.substring(0, 200)}...`;
    
    if (navigator.share) {
        navigator.share({
            title: '我的故事创作',
            text: text
        }).catch(() => {
            copyToClipboard(text);
        });
    } else {
        copyToClipboard(text);
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('已复制到剪贴板！', 'success');
    }).catch(() => {
        showNotification('复制失败', 'error');
    });
}

// 更新星级显示
function updateStars() {
    document.querySelectorAll('.star').forEach((star, index) => {
        if (index < gameState.currentRating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// 提交评分
function submitRating() {
    if (gameState.currentRating === 0) {
        showNotification('请选择评分', 'error');
        return;
    }

    const historyItem = {
        words: [...gameState.words],
        story: gameState.currentStory,
        type: gameState.storyType,
        length: gameState.storyLength,
        style: gameState.storyStyle,
        rating: gameState.currentRating,
        date: new Date().toISOString()
    };

    // 更新历史记录中的评分
    const lastHistory = gameState.history[gameState.history.length - 1];
    if (lastHistory && lastHistory.story === gameState.currentStory) {
        lastHistory.rating = gameState.currentRating;
    }

    saveHistory();
    elements.rateModal.classList.add('hidden');
    showNotification(`已评分 ${gameState.currentRating} 星！`, 'success');
    gameState.currentRating = 0;
    updateStars();
    renderHistory();
}

// 保存到历史记录
function saveToHistory() {
    const historyItem = {
        words: [...gameState.words],
        story: gameState.currentStory,
        type: gameState.storyType,
        length: gameState.storyLength,
        style: gameState.storyStyle,
        rating: 0,
        date: new Date().toISOString()
    };

    gameState.history.unshift(historyItem);
    if (gameState.history.length > 20) {
        gameState.history = gameState.history.slice(0, 20);
    }

    saveHistory();
    renderHistory();
}

// 保存历史记录到本地存储
function saveHistory() {
    try {
        localStorage.setItem('storyHistory', JSON.stringify(gameState.history));
    } catch (e) {
        console.error('保存历史记录失败:', e);
    }
}

// 加载历史记录
function loadHistory() {
    try {
        const saved = localStorage.getItem('storyHistory');
        if (saved) {
            gameState.history = JSON.parse(saved);
            renderHistory();
        }
    } catch (e) {
        console.error('加载历史记录失败:', e);
    }
}

// 渲染历史记录
function renderHistory() {
    if (gameState.history.length === 0) {
        elements.historyList.innerHTML = '<div class="empty-history">暂无历史记录</div>';
        return;
    }

    elements.historyList.innerHTML = '';
    gameState.history.slice(0, 10).forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.style.cssText = 'padding: 12px; margin-bottom: 8px; background: rgba(255,255,255,0.5); border-radius: 8px; cursor: pointer; transition: all 0.2s;';
        historyItem.innerHTML = `
            <div style="font-size: 12px; color: #666; margin-bottom: 4px;">${new Date(item.date).toLocaleDateString()}</div>
            <div style="font-size: 13px; font-weight: 500; margin-bottom: 4px;">${item.words.slice(0, 3).join('、')}${item.words.length > 3 ? '...' : ''}</div>
            <div style="font-size: 11px; color: #999;">${item.story.substring(0, 30)}...</div>
            ${item.rating > 0 ? `<div style="margin-top: 4px;">${'⭐'.repeat(item.rating)}</div>` : ''}
        `;
        
        historyItem.addEventListener('click', () => {
            gameState.words = [...item.words];
            gameState.currentStory = item.story;
            gameState.storyType = item.type;
            gameState.storyLength = item.length;
            gameState.storyStyle = item.style;
            renderWords();
            displayStory(item.story);
            updateWordCount();
            elements.storyLength.value = item.length;
            elements.lengthValue.textContent = `${item.length}字`;
            elements.storyType.value = item.type;
            elements.storyStyle.value = item.style;
        });
        
        historyItem.addEventListener('mouseenter', () => {
            historyItem.style.transform = 'translateX(4px)';
            historyItem.style.background = 'rgba(255,255,255,0.7)';
        });
        
        historyItem.addEventListener('mouseleave', () => {
            historyItem.style.transform = 'translateX(0)';
            historyItem.style.background = 'rgba(255,255,255,0.5)';
        });
        
        elements.historyList.appendChild(historyItem);
    });
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'error' ? '#FF3B30' : type === 'success' ? '#34C759' : 'rgba(0, 122, 255, 0.9)'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        z-index: 3000;
        animation: slideInRight 0.3s ease;
        font-size: 14px;
        font-weight: 500;
        max-width: 300px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 添加通知动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
