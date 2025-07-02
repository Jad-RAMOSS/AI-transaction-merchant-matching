module.exports = {
  apps: [
    {
      name: 'ai-merchant-api',
      cwd: '/app/Bank_Statement_Rep_Prediction/AI-transaction-merchant-matching/predict',
      script: 'uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      interpreter: '/usr/bin/python3',
      env: { PYTHONUNBUFFERED: '1' }
    }
  ]
}
