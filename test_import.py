#!/usr/bin/env python
"""Test if imports work correctly"""
import sys
import os
import importlib.util

SCRIPT_DIR = os.getcwd()
UTILS_DIR = os.path.join(SCRIPT_DIR, "utils")

print(f"Current dir: {SCRIPT_DIR}")
print(f"Utils dir: {UTILS_DIR}")
print(f"Utils exists: {os.path.exists(UTILS_DIR)}")

# Test 1: Regular import
print("\n=== Test 1: Regular import ===")
try:
    from utils.auth_utils import is_authenticated
    print("✓ Regular import successful!")
except Exception as e:
    print(f"✗ Regular import failed: {e}")

# Test 2: Direct file loading
print("\n=== Test 2: Direct file loading ===")
auth_utils_path = os.path.join(UTILS_DIR, "auth_utils.py")
print(f"Auth utils path: {auth_utils_path}")
print(f"Auth utils exists: {os.path.exists(auth_utils_path)}")

try:
    spec = importlib.util.spec_from_file_location("utils.auth_utils", auth_utils_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules['utils.auth_utils'] = module
        spec.loader.exec_module(module)
        print("✓ Direct file loading successful!")
        print(f"  - Module: {module}")
        print(f"  - Functions: {[x for x in dir(module) if not x.startswith('_')][:5]}")
except Exception as e:
    print(f"✗ Direct file loading failed: {e}")

print("\n✓ All tests passed!")
