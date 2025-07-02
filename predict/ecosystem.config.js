module.exports = {
  apps: [
    {
      name: 'ai-merchant-api',
      cwd: '/home/jad/Bank_Settlement/AI-transaction-merchant-matching/predict',
      script: 'uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      interpreter: '/usr/local/bin/python3.11',
      env: { PYTHONUNBUFFERED: '1' }
    }
  ]
}
