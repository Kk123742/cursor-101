# JSONBin 对话可视化 - 行星文字效果

基于 p5.js 的网页应用，实时读取 JSONBin 中的对话内容，并以行星绕轴旋转的3D效果展示。

## 功能特点

- 🌌 **3D 文字旋转效果**：文字像行星一样绕轴旋转
- 🔄 **实时数据更新**：每2秒自动从 JSONBin 获取最新对话
- 🎨 **美观的视觉效果**：深色背景、发光效果、轨道线
- 📱 **响应式设计**：自适应不同屏幕尺寸

## 文件结构

```
5.2/
├── index.html      # 主页面
├── sketch.js       # p5.js 主逻辑
├── config.js       # JSONBin API 配置
├── vercel.json     # Vercel 部署配置
└── README.md       # 说明文档
```

## 部署到 Vercel

### 方法一：通过 Vercel CLI

1. **安装 Vercel CLI**（如果还没有）：
```bash
npm i -g vercel
```

2. **登录 Vercel**：
```bash
vercel login
```

3. **在项目目录中部署**：
```bash
cd 5.2
vercel
```

4. **按照提示完成部署**：
   - 选择项目名称
   - 确认部署设置
   - 等待部署完成

### 方法二：通过 GitHub

1. **将代码推送到 GitHub 仓库**

2. **在 Vercel 网站操作**：
   - 访问 [vercel.com](https://vercel.com)
   - 点击 "New Project"
   - 导入你的 GitHub 仓库
   - 选择 `5.2` 文件夹作为根目录
   - 点击 "Deploy"

3. **自动部署**：
   - Vercel 会自动检测并部署
   - 部署完成后会提供访问链接

### 方法三：直接拖拽部署

1. **访问 Vercel Dashboard**
2. **选择 "Add New Project"**
3. **选择 "Upload" 选项**
4. **将整个 `5.2` 文件夹拖拽上传**
5. **等待部署完成**

## 配置说明

### JSONBin API 配置

在 `config.js` 中配置你的 JSONBin 信息：

```javascript
const JSONBIN_CONFIG = {
    BIN_ID: "你的Bin_ID",
    ACCESS_KEY: "你的Access_Key",
    API_URL: "https://api.jsonbin.io/v3/b",
    UPDATE_INTERVAL: 2000 // 更新间隔（毫秒）
};
```

### ⚠️ 安全提示

**重要**：Access Key 暴露在前端代码中是不安全的做法。在生产环境中，建议：

1. **使用后端代理**：
   - 创建一个后端 API 端点
   - 前端调用后端 API
   - 后端使用 Access Key 访问 JSONBin

2. **使用环境变量**：
   - 在 Vercel 中设置环境变量
   - 使用 Vercel 的 Serverless Functions 作为代理

3. **使用 CORS 代理**：
   - 使用第三方 CORS 代理服务
   - 或自己搭建代理服务器

## 自定义效果

### 调整旋转速度

在 `sketch.js` 中修改：
```javascript
let rotationSpeed = 0.015; // 增大数值 = 转得更快
```

### 调整轨道半径

```javascript
let orbitRadius = 250; // 增大数值 = 轨道更大
```

### 调整文字大小

```javascript
let textSize = 24; // 增大数值 = 文字更大
```

### 调整更新间隔

在 `config.js` 中修改：
```javascript
UPDATE_INTERVAL: 2000 // 毫秒，2000 = 2秒
```

## 故障排除

### 问题：无法加载 JSONBin 数据

1. **检查 Bin ID 和 Access Key**：
   - 确认 `config.js` 中的配置正确
   - 检查 JSONBin 网站上的配置

2. **检查 Bin 权限**：
   - 如果 Bin 是私有的，确保 Access Key 有读取权限
   - 或者将 Bin 设置为 Public

3. **检查网络连接**：
   - 打开浏览器开发者工具（F12）
   - 查看 Network 标签页
   - 检查 API 请求是否成功

### 问题：文字不显示

1. **检查文字内容**：
   - 确认 JSONBin 中有数据
   - 检查 `data.record.text` 是否有值

2. **检查浏览器控制台**：
   - 按 F12 打开开发者工具
   - 查看 Console 标签页的错误信息

### 问题：部署后无法访问

1. **检查 Vercel 部署状态**：
   - 在 Vercel Dashboard 查看部署日志
   - 确认没有构建错误

2. **检查文件路径**：
   - 确认所有文件都在 `5.2` 文件夹中
   - 确认 `index.html` 在根目录

## 技术栈

- **p5.js**：用于3D图形渲染
- **JSONBin API**：用于数据存储和获取
- **Vercel**：用于静态网站托管

## 许可证

MIT License

