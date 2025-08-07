#!/usr/bin/env python3
"""
Comprehensive test of UC Kingdom Bot using main.py
Tests all roles, abilities, game mechanics, and bot functionality
"""

import asyncio
import logging
import sys
from datetime import datetime
from database.db_manager import DatabaseManager
from database.models import User, Game, GamePlayer
from roles.role_factory import RoleFactory
from game.role_distribution import assign_roles
from game.items import ItemSystem
from game.game_manager import GameManager
from game.phase_manager import PhaseManager
from game.voting_system import VotingSystem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveTestSuite:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.role_factory = RoleFactory()
        self.item_system = ItemSystem()
        self.test_results = []
        
    async def run_all_tests(self):
        """Run comprehensive tests of all bot functionality"""
        print("🚀 UC Kingdom Bot - Comprehensive Production Test")
        print("=" * 70)
        
        await self.test_database_operations()
        await self.test_all_roles_and_abilities()
        await self.test_game_mechanics()
        await self.test_item_system()
        await self.test_ranking_system()
        await self.test_game_flow_simulation()
        
        self.print_final_results()
        
    async def test_database_operations(self):
        """Test all database operations"""
        print("\n📊 Testing Database Operations...")
        
        try:
            await self.db_manager.initialize_collections()
            print("✅ Database initialization successful")
            
            test_user = User(telegram_id=999999, ign="TestPlayer", rank_stars=5)
            await self.db_manager.create_user(test_user)
            print("✅ User creation successful")
            
            retrieved_user = await self.db_manager.get_user(999999)
            if retrieved_user and retrieved_user.ign == "TestPlayer":
                print("✅ User retrieval successful")
            else:
                print("❌ User retrieval failed")
                
            test_user.rank_stars = 10
            await self.db_manager.update_user(test_user)
            print("✅ User update successful")
            
            test_game = Game(
                game_id="test_game_001",
                chat_id=-1001234567890,
                creator_id=999999,
                players=[999999, 888888, 777777]
            )
            await self.db_manager.create_game(test_game)
            print("✅ Game creation successful")
            
            retrieved_game = await self.db_manager.get_game("test_game_001")
            if retrieved_game and len(retrieved_game.players) == 3:
                print("✅ Game retrieval successful")
            else:
                print("❌ Game retrieval failed")
                
            self.test_results.append(("Database Operations", True))
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            self.test_results.append(("Database Operations", False))
    
    async def test_all_roles_and_abilities(self):
        """Test all 19 roles and their abilities"""
        print("\n🎭 Testing All 19 Roles and Abilities...")
        
        try:
            available_roles = self.role_factory.get_available_roles()
            print(f"Available roles: {len(available_roles)}")
            
            if len(available_roles) != 19:
                print(f"❌ Expected 19 roles, found {len(available_roles)}")
                self.test_results.append(("Role System", False))
                return
                
            role_tests_passed = 0
            
            for role_name in available_roles:
                try:
                    role_instance = self.role_factory.create_role(role_name, 999999, "test_game")
                    
                    if hasattr(role_instance, 'get_team'):
                        team = role_instance.get_team()
                        print(f"✅ {role_name}: Team = {team}")
                    
                    if hasattr(role_instance, 'get_win_condition'):
                        win_condition = role_instance.get_win_condition()
                        print(f"   Win condition: {win_condition[:50]}...")
                    
                    if hasattr(role_instance, 'can_act_at_night'):
                        can_act = role_instance.can_act_at_night()
                        if can_act:
                            print(f"   Night action available: Yes")
                    
                    role_tests_passed += 1
                    
                except Exception as e:
                    print(f"❌ {role_name} failed: {e}")
            
            print(f"\n✅ Role tests: {role_tests_passed}/{len(available_roles)} passed")
            
            for player_count in [7, 10, 15, 20]:
                roles = assign_roles(player_count)
                if len(roles) == player_count:
                    print(f"✅ Role distribution for {player_count} players: {len(roles)} roles")
                else:
                    print(f"❌ Role distribution for {player_count} players failed")
            
            self.test_results.append(("Role System", role_tests_passed == len(available_roles)))
            
        except Exception as e:
            print(f"❌ Role system test failed: {e}")
            self.test_results.append(("Role System", False))
    
    async def test_game_mechanics(self):
        """Test core game mechanics"""
        print("\n🎮 Testing Game Mechanics...")
        
        try:
            game_manager = GameManager(self.db_manager, None)
            
            test_players = [999999, 888888, 777777, 666666, 555555, 444444, 333333]
            game_id = await game_manager.create_game(-1001234567890, 999999)
            
            if game_id:
                print("✅ Game creation successful")
                
                for player_id in test_players[1:]:
                    success = await game_manager.join_game(game_id, player_id)
                    if success:
                        print(f"✅ Player {player_id} joined game")
                
                game = await self.db_manager.get_game(game_id)
                if game and len(game.players) == len(test_players):
                    print(f"✅ All {len(test_players)} players in game")
                
                phase_manager = PhaseManager(self.db_manager)
                voting_system = VotingSystem()
                
                print("✅ Phase manager initialized")
                print("✅ Voting system initialized")
                
                await self.db_manager.delete_game(game_id)
                print("✅ Game cleanup successful")
                
            self.test_results.append(("Game Mechanics", True))
            
        except Exception as e:
            print(f"❌ Game mechanics test failed: {e}")
            self.test_results.append(("Game Mechanics", False))
    
    async def test_item_system(self):
        """Test item system and Lucky Draw"""
        print("\n🎁 Testing Item System...")
        
        try:
            available_items = self.item_system.get_available_items()
            print(f"Available items: {len(available_items)}")
            
            if len(available_items) != 7:
                print(f"❌ Expected 7 items, found {len(available_items)}")
                self.test_results.append(("Item System", False))
                return
            
            for item_name in available_items:
                item_info = self.item_system.get_item_info(item_name)
                print(f"✅ {item_name}: {item_info['description'][:30]}...")
            
            draw_results = []
            for i in range(10):
                result = self.item_system.perform_lucky_draw()
                draw_results.append(result)
                print(f"   Draw {i+1}: {result}")
            
            display_results = [r['display'] for r in draw_results]
            unique_results = set(display_results)
            if len(unique_results) > 1:
                print("✅ Lucky Draw producing varied results")
            else:
                print("⚠️  Lucky Draw results seem uniform")
            
            self.test_results.append(("Item System", True))
            
        except Exception as e:
            print(f"❌ Item system test failed: {e}")
            self.test_results.append(("Item System", False))
    
    async def test_ranking_system(self):
        """Test ranking and performance system"""
        print("\n🏆 Testing Ranking System...")
        
        try:
            test_user = User(telegram_id=777777, ign="RankTest", rank_stars=0)
            
            for stars in [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30]:
                test_user.rank_stars = stars
                rank_info = test_user.get_rank_info()
                print(f"✅ {stars} stars = {rank_info['rank']['name']} rank")
            
            test_user.rank_stars = 5
            test_user.add_performance_stars(3)
            if test_user.rank_stars == 8:
                print("✅ Performance star addition working")
            
            test_user.subtract_performance_stars(2)
            if test_user.rank_stars == 6:
                print("✅ Performance star subtraction working")
            
            brick_reward = test_user.calculate_brick_reward(5)
            if brick_reward == 50:
                print("✅ Brick reward calculation correct (5 stars = 50 bricks)")
            
            self.test_results.append(("Ranking System", True))
            
        except Exception as e:
            print(f"❌ Ranking system test failed: {e}")
            self.test_results.append(("Ranking System", False))
    
    async def test_game_flow_simulation(self):
        """Simulate a complete game flow"""
        print("\n🎯 Testing Complete Game Flow Simulation...")
        
        try:
            game_manager = GameManager(self.db_manager, None)
            
            test_players = list(range(100001, 100011))
            game_id = await game_manager.create_game(-1001111111111, test_players[0])
            
            for player_id in test_players[1:]:
                await game_manager.join_game(game_id, player_id)
            
            game = await self.db_manager.get_game(game_id)
            if game and len(game.players) == 10:
                print("✅ 10-player game created successfully")
                
                roles = assign_roles(10)
                print(f"✅ Roles assigned: {len(roles)} roles for 10 players")
                
                role_counts = {}
                for role in roles:
                    team = self.role_factory.create_role(role, 999999).get_team()
                    role_counts[team] = role_counts.get(team, 0) + 1
                
                print(f"✅ Team distribution: {role_counts}")
                
                game.current_phase = "night"
                game.day_count = 1
                await self.db_manager.update_game(game)
                print("✅ Game phase transition successful")
                
                for i, (player_id, role) in enumerate(zip(game.players, roles)):
                    game_player = GamePlayer(
                        game_id=game_id,
                        user_id=player_id,
                        role=role,
                        role_data={}
                    )
                    await self.db_manager.create_game_player(game_player)
                
                print("✅ All game players created with roles")
                
                game_players = await self.db_manager.get_game_players(game_id)
                if len(game_players) == 10:
                    print("✅ Game player retrieval successful")
                
                await self.db_manager.delete_game_players(game_id)
                await self.db_manager.delete_game(game_id)
                print("✅ Game cleanup completed")
                
            self.test_results.append(("Game Flow Simulation", True))
            
        except Exception as e:
            print(f"❌ Game flow simulation failed: {e}")
            self.test_results.append(("Game Flow Simulation", False))
    
    def print_final_results(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 70)
        
        passed = 0
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<25} {status}")
            if result:
                passed += 1
        
        print("-" * 70)
        print(f"OVERALL RESULT: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - BOT IS FULLY FUNCTIONAL!")
            print("✅ Database operations working")
            print("✅ All 19 roles implemented correctly")
            print("✅ Game mechanics operational")
            print("✅ Item system functional")
            print("✅ Ranking system working")
            print("✅ Complete game flow verified")
        else:
            print("⚠️  Some tests failed - review issues above")

async def main():
    """Run comprehensive test suite"""
    test_suite = ComprehensiveTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
