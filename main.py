from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
	return {'data':{'name':'Mridul'}}

@app.get('/about')
def about():
	return {'data':{'message':'I am fine Buddy'}}