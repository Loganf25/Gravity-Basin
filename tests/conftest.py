import sys
import os

# Ensure project's src/ is on sys.path so tests can import the package
TEST = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TEST)
SRC = os.path.join(ROOT, 'src')
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if SRC not in sys.path:
    sys.path.insert(0, SRC)
