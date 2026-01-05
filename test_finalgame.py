#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试finalgame.py的基本功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """测试导入"""
    try:
        from finalgame import ChatGame, call_zhipu_api
        print("[成功] 导入成功")
        return True
    except Exception as e:
        print(f"[失败] 导入失败: {e}")
        return False

def test_api_call():
    """测试API调用（不实际调用，只测试导入）"""
    try:
        from finalgame import call_zhipu_api
        print("[成功] API函数导入成功")
        return True
    except Exception as e:
        print(f"[失败] API函数导入失败: {e}")
        return False

def test_game_init():
    """测试游戏初始化"""
    try:
        from finalgame import ChatGame
        game = ChatGame()
        game.initialize()
        print("[成功] 游戏初始化成功")
        print(f"  - 对话历史长度: {len(game.conversation_history)}")
        print(f"  - 风险分数: {game.risk_score}")
        print(f"  - 角色: {game.selected_role}")
        return True
    except Exception as e:
        print(f"[失败] 游戏初始化失败: {e}")
        return False

def main():
    print("[测试] 测试 finalgame.py")
    print("=" * 40)

    tests = [
        test_imports,
        test_api_call,
        test_game_init
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print(f"测试结果: {passed}/{len(tests)} 通过")

    if passed == len(tests):
        print("[完成] 所有测试通过！")
    else:
        print("[警告] 有测试失败")

if __name__ == "__main__":
    main()
