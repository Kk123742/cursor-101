// JSONBin API 配置
// ⚠️ 注意：Access Key 暴露在前端是不安全的，仅用于演示
// 生产环境应该使用后端代理或环境变量
const JSONBIN_CONFIG = {
    BIN_ID: "6938f6c9d0ea881f401ea392",
    ACCESS_KEY: "$2a$10$hq5VYpcYwvz65p/UF5//9.zYr/t.xU.WRlNIT5IHi6TiAQfRQms/W",
    API_URL: "https://api.jsonbin.io/v3/b",
    UPDATE_INTERVAL: 2000 // 每2秒更新一次（毫秒）
};

// 获取 JSONBin 数据的函数
async function fetchJSONBinData() {
    try {
        const url = `${JSONBIN_CONFIG.API_URL}/${JSONBIN_CONFIG.BIN_ID}/latest`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-Access-Key': JSONBIN_CONFIG.ACCESS_KEY
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            return {
                success: true,
                text: data.record?.text || '',
                timestamp: data.record?.timestamp || '',
                read: data.record?.read || false
            };
        } else {
            return {
                success: false,
                error: `HTTP ${response.status}: ${response.statusText}`
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

