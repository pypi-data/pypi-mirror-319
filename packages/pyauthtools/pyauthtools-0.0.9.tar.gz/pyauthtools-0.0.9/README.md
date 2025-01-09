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
@app.route('/index', methods=['POST', 'GET'])
@auth    # Just above the func
def index():
  return rend_template('index.html')
```
