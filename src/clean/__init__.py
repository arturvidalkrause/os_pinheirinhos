import sys, os

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "clean")
TESTS_PATH = os.path.join(PROJECT_PATH, "tests")  

sys.path.append(SOURCE_PATH)
sys.path.append(TESTS_PATH)  
