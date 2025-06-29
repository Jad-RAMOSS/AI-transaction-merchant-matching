module.exports = {
    apps: [{
      name: "ai-merchant-api",
      script: "uvicorn",
      interpreter: "python",
      args: "main:app --host 0.0.0.0 --port 8000 --workers 4"
    }]
  }