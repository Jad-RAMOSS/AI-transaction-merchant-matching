module.exports = {
  apps: [
    {
      name: 'ai-merchant-api',
      cwd: '/app/Bank_Statement_Rep_Prediction/AI-transaction-merchant-matching/predict',
      script: 'main.py',
      args: '',
      interpreter: '/usr/bin/python3',
      env: { PYTHONUNBUFFERED: '1' }
    }
  ]
}
