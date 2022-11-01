from http.client import HTTPException
from fastapi import FastAPI,Depends,status,response
from pydantic import BaseModel
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog,db:Session=Depends(get_db)):
	new_blog = models.Blog(title=request.title,body=request.body)
	db.add(new_blog)
	db.commit()
	db.refresh(new_blog)
	return new_blog


@app.get('/blog')
def all(db: Session = Depends(get_db)):
	blogs = db.query(models.Blog).all()
	return blogs

# Getting a blog with a particular id
@app.get('/blog/{id}',status_code=200,response_model=schemas.showBlog)
def show(id,db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id).first()

	if not blog:
		response.status_code = status.HTTP_404_NOT_FOUND
		return {'detail':f'Blog with id {id} is not available'}
	return blog


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session = Depends(get_db)):

	
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	if not blog.first():
		raise HTTPException(stats_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")

	blog.delete(synchronize_session=False)
	db.commit()
	return 'done'


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: schemas.Blog,db: Session = Depends(get_db)):
	
	blog = db.query(models.Blog).filter(models.Blog.id == id)
	if not blog.first():
		raise HTTPException(stats_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")

	blog.update(request)
	db.commit()
	return 'updated successfully'