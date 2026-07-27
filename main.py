from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="InsightCore - Sovereign JWT Issuer")

JWT_SECRET = os.getenv("JWT_SECRET", "sovereign_fallback_secret")
ALGORITHM = "HS256"

class AuthRequest(BaseModel):
    client_id: str
    client_secret: str

@app.post("/auth/issue")
async def issue_token(request: AuthRequest):
    VALID_CLIENT_SECRET = os.getenv("CORE_CLIENT_SECRET", "bridge_secret_123")

    if request.client_secret != VALID_CLIENT_SECRET:
        raise HTTPException(status_code=401, detail="Invalid client secret")

    import time
    now = int(time.time())
    payload = {
        "iss": "sovereign-core",
        "aud": "insight-bridge",
        "sub": request.client_id,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + 3600,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
