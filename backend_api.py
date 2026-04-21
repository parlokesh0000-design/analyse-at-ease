from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO

app = FastAPI(title='Analyze At Ease API')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/')
def root():
    return {'status':'live','app':'Analyze At Ease API'}

@app.post('/analyze')
async def analyze(file: UploadFile = File(...), question: str = Form(...)):
    data = await file.read()
    df = pd.read_csv(BytesIO(data)) if file.filename.endswith('.csv') else pd.read_excel(BytesIO(data))
    summary = {
        'rows': len(df),
        'columns': list(df.columns),
        'question': question,
        'insight': 'Backend connected. Add OpenAI/Razorpay auth next.'
    }
    return summary

@app.post('/payment/webhook')
def payment_webhook(payload: dict):
    return {'received': True, 'payload': payload}
