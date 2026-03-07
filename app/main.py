from fastapi import FastAPI

app = FastAPI(
    title="AI Financial Operations Platform",
    description="AI-powered document intelligence and financial risk system",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "AI FinOps Platform Running"}