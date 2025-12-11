// p5.js 主程序
let currentText = "等待数据...";
let textChars = [];
let angle = 0;
let radius = 200;
let orbitSpeed = 0.02;
let lastUpdateTime = 0;
let updateInterval = 2000; // 2秒更新一次
let isError = false;
let errorMessage = "";

// 文字绕轴旋转的参数
let orbitRadius = 250; // 轨道半径
let rotationSpeed = 0.015; // 旋转速度
let textSize = 24; // 文字大小
let centerX, centerY; // 画布中心

function setup() {
    // 创建全屏画布
    let canvas = createCanvas(windowWidth, windowHeight, WEBGL);
    canvas.parent('canvas-container');
    
    // 设置画布中心
    centerX = 0;
    centerY = 0;
    
    // 初始化文字数组
    updateTextChars(currentText);
    
    // 立即获取一次数据
    loadJSONBinData();
    
    // 设置定时更新
    setInterval(loadJSONBinData, updateInterval);
}

function draw() {
    // 深色背景
    background(20, 20, 40);
    
    // 添加环境光
    ambientLight(60);
    directionalLight(255, 255, 255, 0, 0, -1);
    
    // 旋转角度
    angle += rotationSpeed;
    
    // 绘制轨道线（可选，用于视觉效果）
    push();
    noFill();
    stroke(100, 100, 150, 50);
    strokeWeight(1);
    rotateY(angle);
    rotateX(PI / 6);
    ellipse(0, 0, orbitRadius * 2, orbitRadius * 2);
    pop();
    
    // 绘制文字字符，像行星一样绕轴旋转
    push();
    rotateY(angle);
    rotateX(PI / 6); // 稍微倾斜，更有立体感
    
    // 将文字分散到轨道上
    for (let i = 0; i < textChars.length; i++) {
        let charAngle = (TWO_PI / textChars.length) * i + angle * 2;
        let x = cos(charAngle) * orbitRadius;
        let y = sin(charAngle) * orbitRadius;
        let z = sin(charAngle * 0.5) * 50; // 添加Z轴变化，形成3D效果
        
        push();
        translate(x, y, z);
        
        // 让每个字符面向相机
        let lookAtAngle = atan2(y, x);
        rotateY(lookAtAngle + PI / 2);
        
        // 绘制文字
        fill(255, 255, 255);
        noStroke();
        textAlign(CENTER, CENTER);
        textSize(textSize);
        text(textChars[i], 0, 0);
        
        // 添加发光效果（可选）
        fill(100, 150, 255, 50);
        ellipse(0, 0, textSize * 1.5, textSize * 1.5);
        
        pop();
    }
    
    pop();
    
    // 绘制中心点（可选）
    push();
    fill(255, 200, 0);
    noStroke();
    sphere(5);
    pop();
    
    // 更新信息显示
    updateInfoDisplay();
}

// 更新文字字符数组
function updateTextChars(text) {
    if (!text) {
        textChars = ["无", "数", "据"];
        return;
    }
    
    // 将文字拆分成字符数组
    textChars = text.split('');
    
    // 如果文字太长，可以限制字符数量
    if (textChars.length > 50) {
        textChars = textChars.slice(0, 50);
    }
    
    // 如果文字太短，重复填充
    while (textChars.length < 10) {
        textChars = textChars.concat(textChars);
    }
}

// 从 JSONBin 加载数据
async function loadJSONBinData() {
    const data = await fetchJSONBinData();
    
    if (data.success) {
        if (data.text && data.text !== currentText) {
            currentText = data.text;
            updateTextChars(currentText);
            isError = false;
            lastUpdateTime = Date.now();
            
            // 更新信息显示
            updateTimestamp(data.timestamp);
            updateTextPreview(data.text);
        }
    } else {
        isError = true;
        errorMessage = data.error || "未知错误";
        console.error("JSONBin 加载失败:", errorMessage);
    }
}

// 更新信息显示
function updateInfoDisplay() {
    const statusEl = document.getElementById('status');
    if (statusEl) {
        if (isError) {
            statusEl.textContent = `❌ 错误: ${errorMessage}`;
            statusEl.className = 'error';
        } else {
            statusEl.textContent = '✅ 已连接';
            statusEl.className = '';
        }
    }
}

// 更新时间戳显示
function updateTimestamp(timestamp) {
    const timestampEl = document.getElementById('timestamp');
    if (timestampEl && timestamp) {
        const date = new Date(timestamp);
        const timeStr = date.toLocaleString('zh-CN');
        timestampEl.textContent = `更新时间: ${timeStr}`;
    }
}

// 更新文字预览
function updateTextPreview(text) {
    const previewEl = document.getElementById('text-preview');
    if (previewEl && text) {
        const preview = text.length > 30 ? text.substring(0, 30) + '...' : text;
        previewEl.textContent = `内容: ${preview}`;
    }
}

// 窗口大小改变时调整画布
function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

