module.exports = {
    apps: [{
      name: "ai-merchant-api",
      script: "uvicorn",
      interpreter: "C:\\Users\\gelwahy\\AppData\\Local\\anaconda3\\envs\\AI_Merchant_Transaction_Matching\\python.exe",
      args: "main:app --host 0.0.0.0 --port 8000 --workers 4"
    }]
  }