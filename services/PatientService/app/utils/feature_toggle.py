from functools import wraps
from fastapi import HTTPException

FEATURES = {
    "patient_read": True,
    "patient_write": True,
    "patient_delete": False
}

def feature_toggle(feature_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not FEATURES.get(feature_name, False):
                raise HTTPException(
                    status_code=403,
                    detail=f"Feature {feature_name} is disabled"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator