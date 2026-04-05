from fastapi import FastAPI

app = FastAPI(title="KMS API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

