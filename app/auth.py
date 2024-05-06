from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from .config import settings

# Api key is expected in the header x-api-key
api_key_header = APIKeyHeader(name="x-api-key")


def authenticated(api_key_header: str = Security(api_key_header)):
    # Checks if the x-api-key header is same as the api_key from the config
    if settings.api_key == api_key_header:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or Invalid API Key"
    )
