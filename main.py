from fastapi import FastAPI
import uvicorn
from mysite.api import ai

app = FastAPI(title='AutoSchool')

app.include_router(ai.ai_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)