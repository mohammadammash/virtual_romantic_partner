from fastapi import status,Header, HTTPException
import jwt
#internal:
from ..config.main import settings

def verify_authentication(token : str = Header(default="")):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except (jwt.InvalidSignatureError, jwt.DecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")