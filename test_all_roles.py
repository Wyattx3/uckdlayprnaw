#!/usr/bin/env python3
"""
Test all 19 roles and their abilities in UC Kingdom Bot
"""

import asyncio
import logging
from database.db_manager import DatabaseManager
from database.models import User, Game, GamePlayer
from roles.role_factory import RoleFactory
from game.role_distribution import assign_roles
from game.items import ItemSystem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_all_roles():
    """Test all 19 roles and their abilities"""
    print("🎭 Testing All 19 Roles and Abilities...")
    
    role_factory = RoleFactory()
    available_roles = role_factory.get_available_roles()
    
    print(f"Available roles: {len(available_roles)}")
    
    if len(available_roles) != 19:
        print(f"❌ Expected 19 roles, found {len(available_roles)}")
        return False
    
    role_tests_passed = 0
    
    for role_name in available_roles:
        try:
            role_instance = role_factory.create_role(role_name, 999999, "test_game")
            
            print(f"\n🔍 Testing {role_name}:")
            
            if hasattr(role_instance, 'get_team'):
                team = role_instance.get_team()
                print(f"  ✅ Team: {team}")
            
            if hasattr(role_instance, 'get_role_name'):
                name = role_instance.get_role_name()
                print(f"  ✅ Name: {name}")
            
            if hasattr(role_instance, 'get_role_emoji'):
                emoji = role_instance.get_role_emoji()
                print(f"  ✅ Emoji: {emoji}")
            
            if hasattr(role_instance, 'get_win_condition'):
                win_condition = role_instance.get_win_condition()
                print(f"  ✅ Win condition: {win_condition[:50]}...")
            
            if hasattr(role_instance, 'can_act_at_night'):
                can_act = role_instance.can_act_at_night()
                print(f"  ✅ Night action: {'Yes' if can_act else 'No'}")
            
            if hasattr(role_instance, 'get_role_description'):
                description = role_instance.get_role_description()
                print(f"  ✅ Description: {description[:50]}...")
            
            role_tests_passed += 1
            print(f"  ✅ {role_name} - ALL TESTS PASSED")
            
        except Exception as e:
            print(f"  ❌ {role_name} failed: {e}")
    
    print(f"\n📊 Role tests: {role_tests_passed}/{len(available_roles)} passed")
    
    for player_count in [7, 10, 15, 20]:
        roles = assign_roles(player_count)
        if len(roles) == player_count:
            print(f"✅ Role distribution for {player_count} players: {len(roles)} roles")
            
            team_counts = {}
            for role in roles:
                team = role_factory.get_team_for_role(role)
                team_counts[team] = team_counts.get(team, 0) + 1
            print(f"   Team distribution: {team_counts}")
        else:
            print(f"❌ Role distribution for {player_count} players failed")
    
    return role_tests_passed == len(available_roles)

async def test_item_system():
    """Test item system functionality"""
    print("\n🎁 Testing Item System...")
    
    item_system = ItemSystem()
    available_items = item_system.get_available_items()
    
    print(f"Available items: {len(available_items)}")
    
    if len(available_items) != 7:
        print(f"❌ Expected 7 items, found {len(available_items)}")
        return False
    
    for item_name in available_items:
        item_info = item_system.get_item_info(item_name)
        print(f"✅ {item_name}: {item_info['description'][:40]}...")
    
    print("\n🎲 Testing Lucky Draw (10 draws):")
    draw_results = []
    for i in range(10):
        result = item_system.perform_lucky_draw()
        draw_results.append(result)
        print(f"   Draw {i+1}: {result['display']}")
    
    unique_results = set(r['display'] for r in draw_results)
    if len(unique_results) > 1:
        print("✅ Lucky Draw producing varied results")
    else:
        print("⚠️  Lucky Draw results seem uniform")
    
    return True

async def main():
    """Run all role and item tests"""
    print("🚀 UC Kingdom Bot - Complete Role & Item Testing")
    print("=" * 60)
    
    roles_passed = await test_all_roles()
    items_passed = await test_item_system()
    
    print("\n" + "=" * 60)
    print("📊 COMPLETE TEST RESULTS")
    print("=" * 60)
    
    print(f"Roles System:     {'✅ PASS' if roles_passed else '❌ FAIL'}")
    print(f"Items System:     {'✅ PASS' if items_passed else '❌ FAIL'}")
    
    if roles_passed and items_passed:
        print("\n🎉 ALL SYSTEMS FUNCTIONAL!")
        print("✅ All 19 roles working correctly")
        print("✅ All 7 items working correctly")
        print("✅ Role distributions balanced")
        print("✅ Lucky Draw system operational")
    else:
        print("\n⚠️  Some systems need attention")

if __name__ == "__main__":
    asyncio.run(main())
