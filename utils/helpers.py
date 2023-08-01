import base64
from http.client import HTTPException


def decode_photo(path, encoded_string):
    try:
        with open(path, 'wb') as f:
            f.write(base64.b64decode(encoded_string.encode("utf-8")))
    except Exception as ex:
        raise HTTPException(400, "Invalid photo encoding")
