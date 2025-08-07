import asyncio
import logging
from typing import Dict, List, Optional, Any
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from appwrite.exception import AppwriteException
from database.models import User, Game, GamePlayer
from config import APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, APPWRITE_API_KEY

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint(APPWRITE_ENDPOINT)
        self.client.set_project(APPWRITE_PROJECT_ID)
        self.client.set_key(APPWRITE_API_KEY)
        
        self.databases = Databases(self.client)
        self.database_id = APPWRITE_PROJECT_ID
        
        self.users_collection = 'users'
        self.games_collection = 'games'
        self.game_players_collection = 'game_players'

    async def initialize_collections(self):
        try:
            await self._create_collections_if_not_exist()
            logger.info("Database collections initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")
            raise

    async def _create_collections_if_not_exist(self):
        try:
            logger.info("Checking collections existence...")
            loop = asyncio.get_event_loop()
            
            try:
                await loop.run_in_executor(None, self.databases.get, self.database_id, self.users_collection)
                logger.info("Collections already exist")
            except AppwriteException as e:
                if e.code == 404:
                    logger.info("Collections not found - assuming they exist in cloud")
                else:
                    logger.warning(f"Collection check failed: {e}")
            
            return
        except Exception as e:
            logger.warning(f"Collection initialization check failed: {e}")
            return

    async def create_user(self, user: User) -> bool:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.create_document,
                self.database_id, self.users_collection, str(user.telegram_id), user.to_dict())
            return True
        except AppwriteException as e:
            logger.error(f"Failed to create user {user.telegram_id}: {e}")
            return False

    async def get_user(self, telegram_id: int) -> Optional[User]:
        try:
            loop = asyncio.get_event_loop()
            doc = await loop.run_in_executor(None, self.databases.get_document,
                self.database_id, self.users_collection, str(telegram_id))
            return User.from_dict(doc)
        except AppwriteException as e:
            if e.code == 404:
                return None
            logger.error(f"Failed to get user {telegram_id}: {e}")
            return None

    async def update_user(self, user: User) -> bool:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.update_document,
                self.database_id, self.users_collection, str(user.telegram_id), user.to_dict())
            return True
        except AppwriteException as e:
            logger.error(f"Failed to update user {user.telegram_id}: {e}")
            return False

    async def create_game(self, game: Game) -> bool:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.create_document,
                self.database_id, self.games_collection, game.game_id, game.to_dict())
            return True
        except AppwriteException as e:
            logger.error(f"Failed to create game {game.game_id}: {e}")
            return False

    async def get_game(self, game_id: str) -> Optional[Game]:
        try:
            loop = asyncio.get_event_loop()
            doc = await loop.run_in_executor(None, self.databases.get_document,
                self.database_id, self.games_collection, game_id)
            return Game.from_dict(doc)
        except AppwriteException as e:
            if e.code == 404:
                return None
            logger.error(f"Failed to get game {game_id}: {e}")
            return None

    async def update_game(self, game: Game) -> bool:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.update_document,
                self.database_id, self.games_collection, game.game_id, game.to_dict())
            return True
        except AppwriteException as e:
            logger.error(f"Failed to update game {game.game_id}: {e}")
            return False

    async def delete_game(self, game_id: str) -> bool:
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.delete_document,
                self.database_id, self.games_collection, game_id)
            return True
        except AppwriteException as e:
            logger.error(f"Failed to delete game {game_id}: {e}")
            return False

    async def get_active_game_by_chat(self, chat_id: int) -> Optional[Game]:
        try:
            loop = asyncio.get_event_loop()
            docs = await loop.run_in_executor(None, self.databases.list_documents,
                self.database_id, self.games_collection, [
                    Query.equal('chat_id', chat_id),
                    Query.not_equal('current_phase', 'finished')
                ])
            if docs['documents']:
                return Game.from_dict(docs['documents'][0])
            return None
        except AppwriteException as e:
            logger.error(f"Failed to get active game for chat {chat_id}: {e}")
            return None

    async def create_game_player(self, game_player: GamePlayer) -> bool:
        try:
            document_id = f"{game_player.game_id}_{game_player.user_id}"
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.create_document,
                self.database_id, self.game_players_collection, document_id, game_player.to_dict())
            return True
        except AppwriteException as e:
            logger.error(f"Failed to create game player {document_id}: {e}")
            return False

    async def get_game_player(self, game_id: str, user_id: int) -> Optional[GamePlayer]:
        try:
            document_id = f"{game_id}_{user_id}"
            loop = asyncio.get_event_loop()
            doc = await loop.run_in_executor(None, self.databases.get_document,
                self.database_id, self.game_players_collection, document_id)
            return GamePlayer.from_dict(doc)
        except AppwriteException as e:
            if e.code == 404:
                return None
            logger.error(f"Failed to get game player {document_id}: {e}")
            return None

    async def update_game_player(self, game_player: GamePlayer) -> bool:
        try:
            document_id = f"{game_player.game_id}_{game_player.user_id}"
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.databases.update_document,
                self.database_id, self.game_players_collection, document_id, game_player.to_dict())
            return True
        except AppwriteException as e:
            logger.error(f"Failed to update game player {document_id}: {e}")
            return False

    async def get_game_players(self, game_id: str) -> List[GamePlayer]:
        try:
            loop = asyncio.get_event_loop()
            docs = await loop.run_in_executor(None, self.databases.list_documents,
                self.database_id, self.game_players_collection, [Query.equal('game_id', game_id)])
            return [GamePlayer.from_dict(doc) for doc in docs['documents']]
        except AppwriteException as e:
            logger.error(f"Failed to get game players for {game_id}: {e}")
            return []

    async def delete_game_players(self, game_id: str) -> bool:
        try:
            players = await self.get_game_players(game_id)
            loop = asyncio.get_event_loop()
            for player in players:
                document_id = f"{player.game_id}_{player.user_id}"
                await loop.run_in_executor(None, self.databases.delete_document,
                    self.database_id, self.game_players_collection, document_id)
            return True
        except AppwriteException as e:
            logger.error(f"Failed to delete game players for {game_id}: {e}")
            return False
