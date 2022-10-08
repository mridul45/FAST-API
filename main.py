from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
# only get 10 blogs and those which are published
def index(limit=10,published:bool=True,sort: Optional[str]=None):
	if published:
		return {'data':f'{limit} published from the database'}
	else:
		return {'data':f'{limit} from the database'}

@app.get('/blog/{id}')
def about(id:int):  # Here we have specified that the id shoul be integer/string/float.
	return {'data':id}

@app.get('/blog/unpublished')
def unpublished():
	return {'data':'Account of all unpublished blogs'}


@app.get('/blog/{id}/comments')
def comments(id,limit=10):
	return limit
	return {'data':{'1','2'}}


class Blog(BaseModel):
	title: str
	body: str
	published_at: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
	# return request
	return {'data':f'A blog is created with title {blog.title}'}