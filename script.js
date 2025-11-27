// 游戏状态
const gameState = {
    apiType: 'deepseek',
    apiKey: '',
    apiUrl: 'https://api.deepseek.com/v1/chat/completions',
    words: [],
    currentStory: ''
};

// DOM元素
const elements = {
    startScreen: document.getElementById('startScreen'),
    gameScreen: document.getElementById('gameScreen'),
    startBtn: document.getElementById('startBtn'),
    backBtn: document.getElementById('backBtn'),
    apiKeyInput: document.getElementById('apiKey'),
    apiUrlInput: document.getElementById('apiUrl'),
    wordInput: document.getElementById('wordInput'),
    wordTags: document.getElementById('wordTags'),
    generateBtn: document.getElementById('generateBtn'),
    clearBtn: document.getElementById('clearBtn'),
    storyContainer: document.getElementById('storyContainer'),
    saveBtn: document.getElementById('saveBtn'),
    regenerateBtn: document.getElementById('regenerateBtn'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    apiTypeRadios: document.querySelectorAll('input[name="apiType"]')
};

// 初始化
function init() {
    // API类型切换
    elements.apiTypeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            gameState.apiType = e.target.value;
            if (gameState.apiType === 'deepseek') {
                elements.apiUrlInput.value = 'https://api.deepseek.com/v1/chat/completions';
                gameState.apiUrl = 'https://api.deepseek.com/v1/chat/completions';
            } else if (gameState.apiType === 'dashscope') {
                elements.apiUrlInput.value = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation';
                gameState.apiUrl = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation';
            }
        });
    });

    // API URL输入
    elements.apiUrlInput.addEventListener('change', (e) => {
        gameState.apiUrl = e.target.value || gameState.apiUrl;
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
            addWord();
        }
    });

    elements.wordInput.addEventListener('blur', () => {
        if (elements.wordInput.value.trim()) {
            addWord();
        }
    });

    // 生成故事
    elements.generateBtn.addEventListener('click', generateStory);

    // 清空词语
    elements.clearBtn.addEventListener('click', clearWords);

    // 保存故事
    elements.saveBtn.addEventListener('click', saveStory);

    // 重新生成
    elements.regenerateBtn.addEventListener('click', generateStory);
}

// 开始游戏
function startGame() {
    const apiKey = elements.apiKeyInput.value.trim();
    
    if (!apiKey) {
        alert('请输入API Key');
        return;
    }

    gameState.apiKey = apiKey;
    gameState.apiUrl = elements.apiUrlInput.value.trim() || gameState.apiUrl;
    gameState.apiType = document.querySelector('input[name="apiType"]:checked').value;

    elements.startScreen.classList.remove('active');
    elements.gameScreen.classList.add('active');
}

// 添加词语
function addWord() {
    const word = elements.wordInput.value.trim();
    
    if (!word) return;

    // 处理逗号或空格分隔的多个词语
    const words = word.split(/[,\s]+/).filter(w => w.trim());
    
    words.forEach(w => {
        if (w && !gameState.words.includes(w)) {
            gameState.words.push(w);
            renderWordTag(w);
        }
    });

    elements.wordInput.value = '';
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
}

// 渲染所有词语
function renderWords() {
    elements.wordTags.innerHTML = '';
    gameState.words.forEach(word => renderWordTag(word));
}

// 清空词语
function clearWords() {
    gameState.words = [];
    renderWords();
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
        alert('请至少输入一个词语');
        return;
    }

    if (!gameState.apiKey) {
        alert('请先配置API Key');
        elements.startScreen.classList.add('active');
        elements.gameScreen.classList.remove('active');
        return;
    }

    showLoading();

    try {
        const story = await callAIAPI(gameState.words);
        gameState.currentStory = story;
        displayStory(story);
    } catch (error) {
        console.error('生成故事失败:', error);
        let errorMsg = '生成故事失败: ';
        if (error.message) {
            errorMsg += error.message;
        } else {
            errorMsg += '网络错误或API配置有误，请检查API Key和网络连接';
        }
        alert(errorMsg);
        elements.storyContainer.innerHTML = `
            <div class="placeholder">
                <p style="color: #e74c3c;">${escapeHtml(errorMsg)}</p>
            </div>
        `;
    } finally {
        hideLoading();
    }
}

// 调用AI API
async function callAIAPI(words) {
    const prompt = `请根据以下关键词，创作一个完整、有趣、有深度的故事。故事应该自然地融合这些词语，让它们成为故事的重要组成部分。关键词：${words.join('、')}。请用中文回答，故事长度在300-500字左右。`;

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
            max_tokens: 1000
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
                max_tokens: 1000,
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
            <div class="placeholder">
                <p>生成的故事为空，请重试</p>
            </div>
        `;
        return;
    }
    
    elements.storyContainer.innerHTML = `
        <div class="story-content">${escapeHtml(story)}</div>
    `;
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
        alert('没有可保存的故事');
        return;
    }

    const content = `关键词：${gameState.words.join('、')}\n\n${gameState.currentStory}`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `故事_${new Date().getTime()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);

