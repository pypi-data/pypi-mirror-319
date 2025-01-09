# PyAuthTools

## Surpported Algorisms
HS256

RS256


## Install
```python
pip install pyauthtools
```

## Usages
```python
token = request.headers.get('Authorization').split(' ')[1]
result = jwtauthtool.decode_jwt(token, JWT_SECRET)
```
