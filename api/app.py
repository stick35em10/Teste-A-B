# api/app.py
from fastapi import FastAPI
from api.endpoints import experiments, assignments, results

app = FastAPI(title="Sistema de Teste A/B", version="1.0.0")

app.include_router(experiments.router, prefix="/api/v1/experiments")
app.include_router(assignments.router, prefix="/api/v1/assignments")
app.include_router(results.router, prefix="/api/v1/results")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}