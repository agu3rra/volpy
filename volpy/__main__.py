# Python self executing directory
import sys
import os
CURRENT_PATH = sys.path[0]
sys.path.append(os.path.join(CURRENT_PATH, 'lib'))

def demo():
    print("volpy demo run.")

if __name__ == '__main__':
    demo()
