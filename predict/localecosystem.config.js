module.exports = {
    apps: [
      {
        name: 'ai-merchant-api',
        cwd: 'C:/AI Merchant Transaction Matching/BERT_api/predict',
        script: 'main.py',
        args: '-m uvicorn main:app --host 0.0.0.0 --port 8000',
        script: 'C:/Users/gelwahy/AppData/Local/anaconda3/envs/AI_Merchant_Transaction_Matching/python.exe',
        env: { PYTHONUNBUFFERED: '1' }
      }
    ]
  }