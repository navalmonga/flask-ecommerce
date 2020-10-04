## flask-ecommerce

Secure, full-stack Bootstrap ecommerce Flask app. 


## Install virtualenv

**Install via pipx**

```
brew install pipx
pipx ensurepath
pipx install virtualenv
virtualenv --help
```

## Local Development

```
virtualenv .
source ./bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0
```

## Find & kill PID running on port 5000
```
lsof -i :{PORT}
kill -9 {PID}
```

## Full browser refresh (cache)
```
Ctrl + C
Command + Shift + R
```