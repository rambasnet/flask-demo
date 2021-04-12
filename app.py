from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def hello_world():
  data = {
    'heading': 'Hello world',
    'title': 'Hello world app...',
    'content': 'some content...<em>text</em>'
  }
  return template(data)
  

@app.route('/dashboard', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dashboard():
  data = {
    'title': 'Dashboard...',
    'heading': 'see your stuff...'
  }
  if request.method == 'GET':
    return template(data)
  elif request.method == 'POST':
    return 'Post method was sucessfully received...'
  elif request.method == 'PUT':
    return 'Put request received...'


def template(data={}):
  return f'''
  <!doctype html>
  <html>
    <head>
      <title>{data.get('title', 'default title')}</title>
    </head>
    <body>
      <header>
        <a href="/"Home>Home</a> | <a href="/dashboard">Dashboard</a>
      </header>
      <h1>{data.get('heading', 'default heading')}</h1>
      <h2>Hello World!</h2>
      <p> {data.get('content', 'default content')}</p>
    </body> 
    <footer>
      <a href="/"Home>Home</a> | <a href="/dashboard">Dashboard</a>
    </footer>
  </html>
  '''
