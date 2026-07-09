import os
import sys

# Add root directory to sys.path so Vercel can find run.py and the app/ package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app
