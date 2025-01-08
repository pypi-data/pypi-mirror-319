import jwt
import os
from datetime import datetime, timedelta


def create_jwt(username, secret, algorithm='HS256'):
  headers = {
    "alg": algorithm,
    "typ": "JWT"
  }
  payload = {
    "username": username,
    "exp": datetime.utcnow() + timedelta(days=1)
  }
  try:
    token = jwt.encode(payload, secret, algorithm, headers=headers)
    return token
  except Exception as e:
    return e
  
def decode_jwt(token, secret, algorithm='HS256'):
  try:
    decoded = jwt.decode(token, secret, algorithm)
    return decoded
  except:
    return 'unauthorized'