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
@auth
@app.route('/index', methods=['POST', 'GET'])
def index():
  return rend_template('index.html')
```
