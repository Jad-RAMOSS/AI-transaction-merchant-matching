

const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '.env') });

module.exports = {
  apps: [
    {
      name: 'ai-merchant-api',
      cwd: process.env.CWD || '/home/jad/Bank_Settlement/AI-transaction-merchant-matching/predict',
      script: 'uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      interpreter: process.env.INTERPRETER || '/usr/local/bin/python3.11',
      env: { PYTHONUNBUFFERED: '1' }
    }
  ]
}
