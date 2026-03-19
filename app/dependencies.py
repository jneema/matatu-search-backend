from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from app.db.session import get_db
from app.config import get_settings

settings = get_settings()
bearer_scheme = HTTPBearer()


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        role = payload.get("role")
        if role != "admin":
            raise HTTPException(
                status_code=403, detail="Admin access required")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
