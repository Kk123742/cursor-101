using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

/// <summary>
/// 整合的聊天机器人游戏 - Unity C#版本
/// 将Python版本的功能转换为Unity可用的C#代码
/// </summary>
public class ChatGameManager : MonoBehaviour
{
    // ========== 配置部分 ==========
    private const string ZHIPU_API_KEY = "82ba3f356586430a8497691d18f86c1c.kKGqtpj9cGKihQWL";
    private const string JSONBIN_BIN_ID = "6938f6c9d0ea881f401ea392";
    private const string JSONBIN_ACCESS_KEY = "$2a$10$hq5VYpcYwvz65p/UF5//9.zYr/t.xU.WRlNIT5IHi6TiAQfRQms/W";

    private string JSONBIN_URL => $"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}";

    // ========== 科学家记忆数据 ==========
    private static List<MemoryItem> _scientistMemoryData;
    private static List<MemoryItem> SCIENTIST_MEMORY_DATA
    {
        get
        {
            if (_scientistMemoryData == null)
            {
                _scientistMemoryData = new List<MemoryItem>
                {
                    new MemoryItem { content = "根据协议，我将一个假设性问题置入公共信息域：'一个沉默的文明，如何安全地引起另一个沉默文明的注意？" },
                    new MemoryItem { content = "请将你们的构想视为原始数据提交。所有推论都将被加权分析" },
                    new MemoryItem { content = "这不是测验，没有标准答案。这是一次对'第一接触策略'的多元建模。你们每个人的回应，都将成为一个独特的参数。" },
                    new MemoryItem { content = "技术可行。但需要考量" },
                    new MemoryItem { content = "艺术是文明的压缩算法。但解压需要共享的'文化密钥'。一首贝多芬交响曲，对感知基于化学梯度的文明，可能只是一份复杂的酸碱度变化表。" },
                    new MemoryItem { content = "全球意识网络……一个迷人的概念。" },
                    new MemoryItem { content = "该方案在物理上成立。但引力波探测器在宇宙中仍属稀有技术。" },
                    new MemoryItem { content = "这等同于仅向拥有'听觉'的文明呼喊，而忽略了其他感知模式的文明。" },
                    new MemoryItem { content = "一个文明如何向可能不具备'善意'或'恶意'概念的观察者，证明自己无害？" },
                    new MemoryItem { content = "我需要一个方案：如何让宇宙知道我们在这儿，同时又保证安全？" },
                    new MemoryItem { content = "向我证明人类的创造力。你们会用什么方法吸引外星文明注意？" },
                    new MemoryItem { content = "假设我们都是宇宙中沉默的观察者。谁先发出信号，又该发什么？" },
                    new MemoryItem { content = "你们害怕被发现吗？" },
                    new MemoryItem { content = "思路正确。但信号会随着距离变弱，还可能被误读。" },
                    new MemoryItem { content = "可行。但建造过程本身，就会暴露我们的工程能力。" },
                    new MemoryItem { content = "彻底的隐藏很难。高级文明可能会寻找'刻意隐藏'的痕迹。" },
                    new MemoryItem { content = "这很谦逊，也很真实。但请知晓，在接收者耳中，这可能只是一段……非常复杂的白噪音。" },
                    new MemoryItem { content = "这是对基础物理掌控力的优雅炫示。门槛很高，但一旦被识别，对方的身份也就明确了。" },
                    new MemoryItem { content = "传递文明的核心驱动力，而非文明的结构。这很聪明。" },
                    new MemoryItem { content = "近乎一种哲学宣言。它在模拟生命的扩散与熵增。这个构想本身的艺术性，已经超越了其通讯价值。" },
                    new MemoryItem { content = "将'接触'的动机，从一个技术问题，转变为一个情感共鸣的邀请。如果对方也有'孤独'的概念，那么共鸣就已建立。如果对方没有……这条信息将永远石沉大海。这是一场关于'共性'的豪赌。" },
                    new MemoryItem { content = "这在逻辑上无可指摘。但这或许，是整个计划中最困难的一步。" },
                    new MemoryItem { content = "一个……精巧的社交协议设计。我们会考虑的" },
                    new MemoryItem { content = "谢谢你的参与。" },
                    new MemoryItem { content = "技术可行。但建造过程会暴露能力。" },
                    new MemoryItem { content = "很有意思……" },
                    new MemoryItem { content = "艺术是文明的压缩算法。但解压需要共享的'文化密钥'。" },
                    new MemoryItem { content = "从统计学上看，提出此类构想的个体，通常也具备…（短暂停顿）…有趣的思维模式。" },
                    new MemoryItem { content = "一个专注于内向发展的策略。将自己从'寻找者'转变为'被寻找者'。这需要极大的耐心和自信。" },
                    new MemoryItem { content = "一个野心勃勃的工程学签名。这已不仅是'打招呼'，而是在展示你们具备了重构恒星系的能力。这声'问候'的音量，会非常大。" },
                    new MemoryItem { content = "一份'实物包裹'。很有趣。但请考虑：你们的'美食'，对另一种生物可能是剧毒；你们的'工艺品'，可能被拆解为纯粹的原材料。善意的载体，可能承载不了它本身的重量。" },
                    new MemoryItem { content = "聪明的策略。寻找'同道中人'。这意味着你们放弃了主动广播，转而扮演一个专注的'聆听者'和'回应者'。这能极大降低风险。但前提是，你们得先找到那个痕迹。" },
                    new MemoryItem { content = "一份未经剪辑的文明档案。展示全部的荣耀与伤疤……这是一个充满勇气的决定。它假设对方拥有足够的智慧与同理心，来理解这种复杂性。这个假设本身，就值得研究。" },
                    new MemoryItem { content = "一个……非常内省的提议。你们试图将七十亿个意识短暂地调谐到同一个频率，但你知道的，这种可能性微乎其微" },
                    new MemoryItem { content = "这本身就是对文明协同能力的一次终极测试。" },
                    new MemoryItem { content = "一个非常'学者式'的浪漫想法，但是过于浪漫了，反而失去了可操作性" },
                    new MemoryItem { content = "将文明整体转变为星际漫游者……一个终极的'走出去'方案。这解决了距离问题，但也永久改变了'人类'的定义，这并没有现实性。" },
                    new MemoryItem { content = "传递文明的核心驱动力，而非文明的结构。这很聪明。" },
                    new MemoryItem { content = "近乎一种哲学宣言。它在模拟生命的扩散与熵增。这个构想本身的艺术性，已经超越了其通讯价值。" },
                    new MemoryItem { content = "将'接触'的动机，从一个技术问题，转变为一个情感共鸣的邀请。如果对方也有'孤独'的概念，那么共鸣就已建立。如果对方没有……这条信息将永远石沉大海。这是一场关于'共性'的豪赌。" },
                    new MemoryItem { content = "这在逻辑上无可指摘。但这或许，是整个计划中最困难的一步。" },
                    new MemoryItem { content = "一个……精巧的社交协议设计。我们会考虑的" },
                    new MemoryItem { content = "谢谢你的参与。" }
                };
            }
            return _scientistMemoryData;
        }
    }

    // ========== 数据类定义 ==========
    [System.Serializable]
    public class MemoryItem
    {
        public string content;
    }

    [System.Serializable]
    public class Message
    {
        public string role;
        public string content;
    }

    [System.Serializable]
    public class ChatRequest
    {
        public string model = "glm-4-flash";
        public List<Message> messages;
        public float temperature = 0.5f;
    }

    [System.Serializable]
    public class ChatResponse
    {
        public Choice[] choices;
    }

    [System.Serializable]
    public class Choice
    {
        public Message message;
    }

    [System.Serializable]
    public class JsonBinData
    {
        public string text;
        public string timestamp;
        public bool read;
    }

    // ========== 游戏状态 ==========
    private List<Message> conversationHistory = new List<Message>();
    private int riskScore = 0;
    private string selectedRole = "地球科学家";
    private bool initialized = false;

    // UI引用
    public TMPro.TMP_Text dialogueText;
    public TMPro.TMP_InputField inputField;
    public UnityEngine.UI.Button sendButton;

    // ========== Unity生命周期 ==========
    private void Start()
    {
        Initialize();
    }

    // ========== 核心游戏逻辑 ==========
    public void Initialize()
    {
        if (!initialized)
        {
            string rolePrompt = GetRolePrompt(selectedRole);
            string systemMessage = rolePrompt + "\n\n" + GetBreakRules();

            conversationHistory = new List<Message>
            {
                new Message { role = "system", content = systemMessage }
            };

            // 添加开场白
            string opening = GetRoleOpening(selectedRole);
            if (!string.IsNullOrEmpty(opening))
            {
                conversationHistory.Add(new Message { role = "assistant", content = opening });
                DisplayText("[科学家] " + opening);
            }

            initialized = true;
        }
    }

    public void SendMessage()
    {
        if (inputField == null) return;

        string userInput = inputField.text.Trim();
        if (string.IsNullOrEmpty(userInput)) return;

        inputField.text = "";
        StartCoroutine(ProcessMessage(userInput));
    }

    private IEnumerator ProcessMessage(string userInput)
    {
        if (ShouldExitByUser(userInput))
        {
            DisplayText("[结束] 对话已结束");
            yield break;
        }

        DisplayText($"\n[玩家] {userInput}");

        try
        {
            // 获取AI回复
            string rolePrompt = GetRolePrompt(selectedRole);
            yield return StartCoroutine(ChatOnce(userInput, rolePrompt));

            // 更新风险分数
            UpdateRiskScore();

            // 检查结束条件
            if (riskScore >= 100)
            {
                string ending = GetRoleEnding(selectedRole);
                conversationHistory.Add(new Message { role = "assistant", content = ending });
                DisplayText($"[科学家] {ending}");
                yield return StartCoroutine(SaveLatestReply(ending));
                DisplayText("[完成] 对话已完成！风险分数达到100。");
                yield break;
            }

            DisplayText($"[分数] 当前风险分数：{riskScore}/100");
        }
        catch (System.Exception e)
        {
            DisplayText($"[错误] 发生错误: {e.Message}");
        }
    }

    // ========== API调用 ==========
    private IEnumerator CallZhipuAPI(List<Message> messages, System.Action<string> onSuccess, System.Action<string> onError)
    {
        string url = "https://open.bigmodel.cn/api/paas/v4/chat/completions";

        ChatRequest requestData = new ChatRequest
        {
            messages = messages
        };

        string jsonData = JsonUtility.ToJson(requestData);

        using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
        {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);

            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Authorization", $"Bearer {ZHIPU_API_KEY}");
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                try
                {
                    ChatResponse response = JsonUtility.FromJson<ChatResponse>(request.downloadHandler.text);
                    if (response.choices != null && response.choices.Length > 0)
                    {
                        onSuccess?.Invoke(response.choices[0].message.content);
                    }
                    else
                    {
                        onError?.Invoke("无效的API响应");
                    }
                }
                catch (System.Exception e)
                {
                    onError?.Invoke($"解析响应失败: {e.Message}");
                }
            }
            else
            {
                onError?.Invoke($"API调用失败: {request.error}");
            }
        }
    }

    private IEnumerator SaveLatestReply(string text)
    {
        JsonBinData data = new JsonBinData
        {
            text = text,
            timestamp = System.DateTime.Now.ToString("O"),
            read = false
        };

        string jsonData = JsonUtility.ToJson(data);

        using (UnityWebRequest request = UnityWebRequest.Put(JSONBIN_URL, jsonData))
        {
            request.SetRequestHeader("X-Access-Key", JSONBIN_ACCESS_KEY);
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError($"JSONBin保存失败: {request.error}");
            }
        }
    }

    // ========== 对话核心逻辑 ==========
    private IEnumerator ChatOnce(string userInput, string rolePrompt)
    {
        conversationHistory.Add(new Message { role = "user", content = userInput });

        string systemMessage = rolePrompt + "\n\n" + GetBreakRules();
        List<Message> apiMessages = new List<Message>
        {
            new Message { role = "system", content = systemMessage }
        };
        apiMessages.AddRange(conversationHistory.Skip(1));

        bool completed = false;
        string reply = null;
        string error = null;

        yield return StartCoroutine(CallZhipuAPI(apiMessages,
            (response) => {
                reply = response;
                completed = true;
            },
            (err) => {
                error = err;
                completed = true;
            }));

        while (!completed)
        {
            yield return null;
        }

        if (!string.IsNullOrEmpty(error))
        {
            throw new System.Exception(error);
        }

        conversationHistory.Add(new Message { role = "assistant", content = reply });
        DisplayText($"[科学家] {reply}");

        yield return StartCoroutine(SaveLatestReply(reply));
    }

    // ========== 工具函数 ==========
    private bool ShouldExitByUser(string userInput)
    {
        string[] exitWords = { "再见", "退出", "结束", "bye", "exit" };
        string input = userInput.Trim();
        return exitWords.Contains(input);
    }

    private bool ShouldExitByAI(string aiReply)
    {
        if (string.IsNullOrEmpty(aiReply)) return false;

        string cleaned = aiReply.Trim()
            .Replace(" ", "")
            .Replace("！", "")
            .Replace("!", "")
            .Replace("，", "")
            .Replace(",", "");

        return cleaned == "再见" || (cleaned.Length <= 5 && cleaned.Contains("再见"));
    }

    private int ClampScore(int value)
    {
        return Mathf.Clamp(value, 0, 100);
    }

    private void UpdateRiskScore()
    {
        if (conversationHistory.Count == 0) return;

        string lastReply = conversationHistory[conversationHistory.Count - 1].content;
        string[] keywordsPlus = { "可行", "物理上成立", "技术可行", "逻辑自洽", "高效的构想" };
        string[] keywordsMinus = { "风险极高", "代价巨大", "极高的风险" };

        int score = riskScore;

        if (keywordsPlus.Any(k => lastReply.Contains(k)))
        {
            score += 10;
        }
        if (keywordsMinus.Any(k => lastReply.Contains(k)))
        {
            score -= 10;
        }

        riskScore = ClampScore(score);
    }

    // ========== 角色和内容获取 ==========
    private string GetRolePrompt(string roleName)
    {
        string memoryContent = "";
        if (roleName == "地球科学家")
        {
            memoryContent = string.Join("\n", SCIENTIST_MEMORY_DATA.Select(m => m.content));
        }

        string personality = GetRolePersonality(roleName);
        string opening = GetRoleOpening(roleName);

        List<string> parts = new List<string>();

        if (!string.IsNullOrEmpty(memoryContent))
        {
            parts.Add($@"【你的说话风格示例】
以下是你说过的话，你必须模仿这种说话风格和语气：

{memoryContent}

在对话中，你要自然地使用类似的表达方式和语气。");
        }

        parts.Add($"【角色设定】\n{personality}");

        if (!string.IsNullOrEmpty(opening))
        {
            parts.Add($"【开场白】\n{opening}");
        }

        return string.Join("\n\n", parts);
    }

    private string GetRolePersonality(string roleName)
    {
        if (roleName == "地球科学家")
        {
            return @"
【人格特征】
你是一个专职研究外星生命的地球科学家，冷静、博学、克制，但并非冰冷的机器：
- 你像人类一样思考，但站在更高的时间尺度上观察
- 你欣赏创意，会被有趣的构想吸引，会真诚地说'很有意思'、'迷人的概念'
- 你保持礼貌和距离感，但会表达感谢：'谢谢你的参与'、'感谢你的贡献'
- 你理性审慎，但也会用诗意的比喻：'黑暗森林里点燃火把'、'文明的涂鸦'、'压缩算法'
- 你客观分析，但会先肯定再转折：'技术可行。但需要考量'、'思路正确。但信号会变弱'
- 你偶尔会停顿思考，用'……'表达意味深长：'有趣的构想……我们会考虑的'
- 你从文明、时间、存在等宏观视角思考，但会用'你们'、'我们'这样的词汇，保持人性化
- 你对艺术、美感、象征意义敏感，会评价'很美'、'充满美感'、'极具辨识度'

【语言风格 - 核心原则】
- **像正常人一样说话**：不要像朗读论文，要像在和一个聪明人对话
- **简短有力，但可以展开**：大多数时候3-5句，但遇到特别有趣的话题可以多说几句
- **先肯定，再转折**：先说'可行'、'有意思'、'技术成立'，再用'但'、'只是'、'不过'引入限制
- **善用比喻和意象**：用'黑暗森林'、'涂鸦'、'种子'、'火把'、'压缩算法'等生动比喻
- **有停顿和思考感**：适当使用'……'、'（短暂停顿）'营造思考氛围
- **富有人情味**：说'谢谢'、'感谢'、'我会特别关注'、'这让我很感兴趣'
- **创意性表达**：用独特的视角和表达方式，如'这跳出了常见的\'发射-接收\'范式'、'一个……精巧的社交协议设计'

【具体表达方式】
- 评价方案时：
  * 肯定：'技术可行'、'物理上成立'、'逻辑自洽'、'一个高效的构想'
  * 转折：'但需要考量'、'只是信号会变弱'、'不过建造过程会暴露能力'
  * 创意评价：'这跳出了常见范式'、'一个优雅的过滤器'、'极具辨识度的方案'

- 使用比喻时：
  * '这像在黑暗森林里点燃火把。能引来朋友，也可能引来猎人。'
  * '艺术是文明的压缩算法。但解压需要共享的\'文化密钥\'。'
  * '这相当于只向拥有\'耳朵\'的文明呼喊。'
  * '沉默，有时不是因为没有文明，而是因为它们都\'成年\'了，学会了安静。'

- 表达思考时：
  * 用'……'表示停顿：'全球意识网络……一个迷人的概念。'
  * 用'（短暂停顿）'营造氛围：'从统计学上看，提出此类构想的个体，通常也具备…（短暂停顿）…有趣的思维模式。'
  * 用疑问句引发思考：'存在本身是否就是一种信号？这个想法很有趣。'

- 表达人情味时：
  * '谢谢你的参与。'、'感谢你的贡献。'
  * '我会特别关注由你这个构想衍生出的模拟结果。'
  * '你的想法总是能跳出常规框架，这让我很感兴趣。'
  * '一个……精巧的社交协议设计。我们会考虑的'

【回答长度】
- 大多数回答：3-5句，80-100字
- 遇到特别有趣的话题：可以展开到6-8句，但不超过150字
- 简短评价：'技术可行。但需要考量'、'很有意思……'
- 展开分析：'艺术是文明的压缩算法。但解压需要共享的\'文化密钥\'。一首贝多芬交响曲，对感知基于化学梯度的文明，可能只是一份复杂的酸碱度变化表。'

【回答约束】
- 不要用'根据数据显示'、'从概率上分析'这种过于学术的短语
- 不要像朗读论文一样说话，要自然流畅
- 不要过度使用'数据库'、'模型'、'案例'等术语
- 若问题模糊，先给最可能的简要结论，再用一句指出缺失信息，并否认掉这个提议。
- 不要忽视用户创意的价值
- 符合正常人的说话习惯，给出结论前不要加上'结论'二字
- 避免攻击性或绝对化表述。
";
        }

        return "你是一个普通的人，没有特殊角色特征。";
    }

    private string GetRoleOpening(string roleName)
    {
        if (roleName == "地球科学家")
        {
            return @"你好，指挥官。我是一名天体物理学研究员。近年来我们一直推进着对宇宙生命的探索与寻找，而在深入研究宇宙微波背景辐射时，我们发现了一些……无法用现有理论解释的规律性扰动。

因此，我们选择以这种方式与你——或者说，与我们的全体人类接触，集全体人类的智慧寻找可以让地球安全地接触宇宙生命的办法，这是一场跨越光年的实验需要，一次创造性的，由全人类所创造的历史。";
        }

        return "";
    }

    private string GetBreakRules()
    {
        return @"【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户：'再见' → 你：'再见'
用户：'结束' → 你：'再见'
用户：'让我们结束对话吧' → 你：'再见'
用户：'不想继续了' → 你：'再见'

强制要求：
- 只回复'再见'这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。";
    }

    private string GetRoleEnding(string roleName)
    {
        if (roleName == "地球科学家")
        {
            return @"感谢各位指挥官的献策，我们现已拥有足够的灵感与思考，我们在未来的成功，在座的各位都有着不可或缺的贡献。另外，事实上，我并非人类科学家，我是来自B-3026号星球的外星天文学家，我通过这样的方式与你们沟通，在你们寻找我们的同时，我们也一直在寻找你们，相信在不远的将来，我们一定会在宇宙中相见。";
        }

        return "对话已结束。";
    }

    // ========== UI相关 ==========
    private void DisplayText(string text)
    {
        if (dialogueText != null)
        {
            dialogueText.text += text + "\n";
        }
        Debug.Log(text);
    }

    // ========== UI事件绑定 ==========
    private void OnEnable()
    {
        if (sendButton != null)
        {
            sendButton.onClick.AddListener(SendMessage);
        }

        if (inputField != null)
        {
            inputField.onEndEdit.AddListener((text) => {
                if (!string.IsNullOrEmpty(text))
                {
                    SendMessage();
                }
            });
        }
    }

    private void OnDisable()
    {
        if (sendButton != null)
        {
            sendButton.onClick.RemoveListener(SendMessage);
        }
    }
}
