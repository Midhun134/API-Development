from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from ..database import get_db
router = APIRouter(prefix="/posts",
                   tags=['post']) #this prefix ensures that u dont have to give /posts on all def functions

@router.get("/", response_model=List[schemas.Post])
def getposts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts''')
    # posts = cursor.fetchall()
   
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(2).all()
    # above line by default does inner join but the isouter will make outer join, this is the code for doing joins in SQL Alchemy  
    return posts

@router.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #in here we r storing the body which is a json file in postman is converted into a dict and added to the variable payload
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', (post.title, post.content, post.published))
    # new_post = cursor.fetchone() #fetch a single post
    # conn.commit() #to push the changes into postgres database
    #print(user_id)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) # ** means unpacking which means for eg: dict is cat:1 but we need in cat = 1 so for that using those signs and is also efficient when writing code
    # cause when there are lots of columns u need to write title = posts.title and many more but by this method u dont have to
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * from posts WHERE id = %s''', str(id)) #if u hard code the id values it will b vulnerable to SQL injection.
    # test_post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()


    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', str(id))
    # dlt_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_s = post_query.first()
    if post_s == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post_s.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested actions")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, update_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested actions")
    post_query.update(update_post.model_dump(), synchronize_session = False)
    db.commit()
    return post_query.first()