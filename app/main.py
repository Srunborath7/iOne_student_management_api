from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Auths Service")

@app.get("/")
def root():
    return ("Welcome to student management with fastapi!")
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)