from fastapi import status,Header, HTTPException

def verify_authentication(token : str = Header(default="")):
    if token != "abcd":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")