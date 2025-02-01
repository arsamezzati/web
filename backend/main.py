from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, EmailStr, Field
from datetime import date
import bcrypt
from mysql import get_db
from typing import Optional
import logging
from igdb_service import igdb_service
from mongo import mongo_service
from pydantic import BaseModel



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3535"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str 
    surname: str 
    email: str
    password: str 
    birthdate: str  
@app.post("/api/login")
async def login(user: UserLogin):
    logger.info(f"Login attempt for email: {user.email}")
    
    try:
        with get_db() as db:
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT uid, name, surname, email, birthdate, password FROM users WHERE email = %s",
                    (user.email,)
                )
                user_data = cursor.fetchone()
                
                if not user_data:
                    raise HTTPException(status_code=401, detail="Invalid email or password")
                
                # Verify password
                stored_password = user_data['password'].encode('utf-8')
                provided_password = user.password.encode('utf-8')
                
                if not bcrypt.checkpw(provided_password, stored_password):
                    raise HTTPException(status_code=401, detail="Invalid email or password")
                    
                # removing the password from response for security purposes
                user_data.pop('password')
                
                # date to string
                if 'birthdate' in user_data:
                    user_data['birthdate'] = user_data['birthdate'].isoformat()
                
                return user_data
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/register")
async def register(user: UserRegister):
    # Logging received data
    logger.info(f"Received registration data: {jsonable_encoder(user)}")
    
    try:
        
        birth_date = date.fromisoformat(user.birthdate)
        
        with get_db() as db:
            with db.cursor() as cursor:
                # Check if user exists
                cursor.execute("SELECT uid FROM users WHERE email = %s", (user.email,))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="Email already registered")
                
                # Hash password
                hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
                
                
                cursor.execute(
                    """INSERT INTO users (name, surname, email, birthdate, password) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (user.name, user.surname, user.email, birth_date, 
                     hashed_password.decode('utf-8'))
                )
                
                new_user_id = cursor.lastrowid
                
                
                cursor.execute(
                    """SELECT uid, name, surname, email, birthdate 
                       FROM users WHERE uid = %s""",
                    (new_user_id,)
                )
                new_user = cursor.fetchone()
                return new_user
                
    except ValueError as e:
        logger.error(f"Date conversion error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/api/games/popular")
async def get_popular_games():
    return await igdb_service.get_popular_games()
@app.get("/api/games/search")
async def search_games(query: str):
    return await igdb_service.search_games(query)

class GameData(BaseModel):
    id: int
    name: str
    cover: dict = None
    first_release_date: int = None
    summary: str = None
    rating: float = None

@app.post("/api/games/{game_id}/like")
async def toggle_game_like(game_id: int, game_data: GameData, user_id: int):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    return await mongo_service.toggle_game_like(user_id, game_data.dict())

@app.get("/api/games/liked")
async def get_liked_games(user_id: int):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    return await mongo_service.get_user_liked_games(user_id)

@app.get("/api/games/{game_id}/liked")
async def is_game_liked(game_id: int, user_id: int):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
class CommentCreate(BaseModel):
    content: str
    game_id: int
    user_id: int
    user_name: str

@app.post("/api/games/{game_id}/comments")
async def add_comment(game_id: int, comment: CommentCreate):
    if not comment.user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    return await mongo_service.add_comment(
        comment.user_id,
        game_id,
        comment.content,
        comment.user_name
    )

@app.get("/api/games/{game_id}/comments")
async def get_comments(game_id: int):
    return await mongo_service.get_game_comments(game_id)
    
    return {"liked": await mongo_service.is_game_liked(user_id, game_id)}