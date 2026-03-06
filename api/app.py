from fastapi import FastAPI
from core.ufac_engine import run_ufac

app = FastAPI()

@app.post("/check")
def check(user_data: dict):
    return run_ufac(user_data)
