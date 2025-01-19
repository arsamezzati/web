from pymongo import MongoClient, DESCENDING
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId
from typing import List, Optional, Dict, Any

class MongoService:
    def __init__(self):
        """Initialize MongoDB connection and collections."""
        try:
            self.client = MongoClient('mongodb://mongodb:27017/')
            self.db = self.client.gametracker
            self.likes = self.db.likes
            self.comments = self.db.comments
            
            # Create indexes
            self.likes.create_index([("user_id", 1), ("game_id", 1)], unique=True)
            self.comments.create_index([("game_id", 1), ("created_at", -1)])
            
        except Exception as e:
            raise Exception(f"Failed to initialize MongoDB: {str(e)}")

    async def toggle_game_like(self, user_id: int, game_data: dict) -> dict:
        """Toggle like status for a game."""
        try:
            # Check if like already exists
            existing_like = self.likes.find_one({
                'user_id': user_id,
                'game_id': game_data['id']
            })

            if existing_like:
                # Unlike: Remove the like
                self.likes.delete_one({
                    'user_id': user_id,
                    'game_id': game_data['id']
                })
                return {'liked': False}
            else:
                # Like: Add new like with game data
                like_doc = {
                    'user_id': user_id,
                    'game_id': game_data['id'],
                    'game_data': game_data,
                    'created_at': datetime.utcnow()
                }
                self.likes.insert_one(like_doc)
                return {'liked': True}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_user_liked_games(self, user_id: int) -> List[dict]:
        """Get all games liked by a user."""
        try:
            likes = self.likes.find(
                {'user_id': user_id}
            ).sort('created_at', DESCENDING)
            
            return [like['game_data'] for like in likes]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def is_game_liked(self, user_id: int, game_id: int) -> bool:
        """Check if a game is liked by a user."""
        try:
            like = self.likes.find_one({
                'user_id': user_id,
                'game_id': game_id
            })
            return bool(like)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def add_comment(self, 
                         user_id: int, 
                         game_id: int, 
                         content: str, 
                         user_name: str) -> dict:
        """Add a new comment to a game."""
        try:
            comment_doc = {
                'user_id': user_id,
                'game_id': game_id,
                'content': content,
                'user_name': user_name,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'likes': 0,
                'is_edited': False
            }
            
            result = self.comments.insert_one(comment_doc)
            comment_doc['_id'] = str(result.inserted_id)
            return comment_doc
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_game_comments(self, game_id: int, 
                              limit: int = 50, 
                              skip: int = 0) -> List[dict]:
        """Get comments for a specific game with pagination."""
        try:
            cursor = self.comments.find(
                {'game_id': game_id}
            ).sort(
                'created_at', DESCENDING
            ).skip(skip).limit(limit)
            
            return [{
                **comment,
                '_id': str(comment['_id']),
                'created_at': comment['created_at'].isoformat(),
                'updated_at': comment['updated_at'].isoformat()
            } for comment in cursor]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update_comment(self, 
                           comment_id: str, 
                           user_id: int, 
                           content: str) -> Optional[dict]:
        """Update a comment if it belongs to the user."""
        try:
            comment = self.comments.find_one({
                '_id': ObjectId(comment_id),
                'user_id': user_id
            })
            
            if not comment:
                return None
                
            result = self.comments.update_one(
                {'_id': ObjectId(comment_id)},
                {
                    '$set': {
                        'content': content,
                        'updated_at': datetime.utcnow(),
                        'is_edited': True
                    }
                }
            )
            
            if result.modified_count > 0:
                updated_comment = self.comments.find_one(
                    {'_id': ObjectId(comment_id)}
                )
                updated_comment['_id'] = str(updated_comment['_id'])
                return updated_comment
                
            return None
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def delete_comment(self, 
                           comment_id: str, 
                           user_id: int) -> bool:
        """Delete a comment if it belongs to the user."""
        try:
            result = self.comments.delete_one({
                '_id': ObjectId(comment_id),
                'user_id': user_id
            })
            return result.deleted_count > 0
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def toggle_comment_like(self, 
                                comment_id: str, 
                                user_id: int) -> dict:
        """Toggle like status for a comment."""
        try:
            comment = self.comments.find_one({'_id': ObjectId(comment_id)})
            if not comment:
                raise HTTPException(status_code=404, detail="Comment not found")
                
            # Check if user has already liked the comment
            liked_by = comment.get('liked_by', [])
            
            if user_id in liked_by:
                # Unlike
                self.comments.update_one(
                    {'_id': ObjectId(comment_id)},
                    {
                        '$pull': {'liked_by': user_id},
                        '$inc': {'likes': -1}
                    }
                )
                return {'liked': False}
            else:
                # Like
                self.comments.update_one(
                    {'_id': ObjectId(comment_id)},
                    {
                        '$addToSet': {'liked_by': user_id},
                        '$inc': {'likes': 1}
                    }
                )
                return {'liked': True}
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def close(self):
        """Close the MongoDB connection."""
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing MongoDB connection: {str(e)}")

# Create a single instance of the service
mongo_service = MongoService()