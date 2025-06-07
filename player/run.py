#!/usr/bin/env python3
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from player.main import main

if __name__ == "__main__":
    main() 