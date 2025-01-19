import requests
import json
from datetime import datetime, timedelta
from fastapi import HTTPException

class IGDBService:
    def __init__(self):
        # Load credentials from JSON file
        try:
            with open('details.json', 'r') as f:
                credentials = json.load(f)
                self.client_id = credentials['client']
                self.client_secret = credentials['secret']
        except Exception as e:
            raise Exception(f"Failed to load IGDB credentials: {str(e)}")
            
        self.access_token = None
        self.token_expires_at = None
        self.base_url = 'https://api.igdb.com/v4'

    async def ensure_token(self):
        if not self.access_token or datetime.now() >= self.token_expires_at:
            await self.get_access_token()

    async def get_access_token(self):
        url = f'https://id.twitch.tv/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data['access_token']
            self.token_expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'] - 100)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get IGDB access token: {str(e)}")

    async def search_games(self, query: str, limit: int = 10):
        await self.ensure_token()
        
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }
        
        body = f"""
        search "{query}";
        fields name, cover.url, first_release_date, summary, rating;
        limit {limit};
        where version_parent = null;
        """

        try:
            response = requests.post(f'{self.base_url}/games', headers=headers, data=body)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to search games: {str(e)}")

    async def get_popular_games(self, limit: int = 20):
        await self.ensure_token()
        
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }
        
        current_timestamp = int(datetime.now().timestamp())
        
        body = f"""
        fields name, cover.url, first_release_date, summary, rating, total_rating;
        where total_rating != null & cover != null;
        sort total_rating desc;
        limit {limit};
        """

        try:
            response = requests.post(f'{self.base_url}/games', headers=headers, data=body)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get popular games: {str(e)}")

# Create single instance
igdb_service = IGDBService()