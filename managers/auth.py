from typing import Optional

import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from starlette.requests import Request

from db import database
from models import user


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user["id"],
                "exp": datetime.utcnow() + timedelta(days=2)
            }
            return jwt.encode(payload, config("SECRET_KEY"), algorithm="HS256")
        except Exception as ex:
            #log exceptions
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPBasicCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(res.credentials, config("SECRET_KEY"), algorithm=["HS256"])
            user_data = await database.fetch_one(user.select().where(user.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


def is_complainer(reques)