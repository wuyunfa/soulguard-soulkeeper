#!/bin/bash
# 运行所有测试

echo "=== SoulGuard测试套件 ==="
echo ""

echo "1. 运行单元测试..."
python3 -m pytest tests/test_unit.py -v 2>/dev/null || python3 tests/test_unit.py

echo ""
echo "2. 运行集成测试..."
python3 tests/test_integration.py

echo ""
echo "3. 运行压力测试..."
python3 tests/test_stress.py

echo ""
echo "=== 所有测试完成 ==="
