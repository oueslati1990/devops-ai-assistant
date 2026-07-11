from fastapi import FastAPI

app = FastAPI(title="AI Devops Assistant")


@app.get("/health")
async def health():
    return {"status": "ok"}
