import json
import os
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class UserAPIKeyStorage:
    """Simple file-based storage for user API keys."""
    
    def __init__(self, storage_file: str = "user_api_keys.json"):
        self.storage_file = storage_file
        self.ensure_storage_file()
    
    def ensure_storage_file(self):
        """Create storage file if it doesn't exist."""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({}, f)
    
    def store_api_key(self, user_id: str, provider: str, api_key: str, model_name: str = None):
        """Store API key for a user and provider."""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            if user_id not in data:
                data[user_id] = {}
            
            data[user_id][provider] = {
                'api_key': api_key,
                'model_name': model_name
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"API key stored for user {user_id}, provider {provider}")
            return True
        except Exception as e:
            logger.error(f"Error storing API key: {e}")
            return False
    
    def get_api_key(self, user_id: str, provider: str) -> Optional[Dict]:
        """Get API key for a user and provider."""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return data.get(user_id, {}).get(provider)
        except Exception as e:
            logger.error(f"Error retrieving API key: {e}")
            return None
    
    def get_user_models(self, user_id: str) -> Dict:
        """Get all models for a user."""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            return data.get(user_id, {})
        except Exception as e:
            logger.error(f"Error retrieving user models: {e}")
            return {}
    
    def delete_api_key(self, user_id: str, provider: str) -> bool:
        """Delete API key for a user and provider."""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            if user_id in data and provider in data[user_id]:
                del data[user_id][provider]
                
                # Clean up empty user entries
                if not data[user_id]:
                    del data[user_id]
                
                with open(self.storage_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                logger.info(f"API key deleted for user {user_id}, provider {provider}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting API key: {e}")
            return False

# Global instance
api_key_storage = UserAPIKeyStorage()
