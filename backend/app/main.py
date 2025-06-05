from fastapi import FastAPI

app = FastAPI(
    title="Mind's Eye Dream-Visualizer",
    description="An AI-powered dream visualizer app",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "OK"} 