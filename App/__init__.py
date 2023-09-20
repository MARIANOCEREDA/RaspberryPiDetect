import sys
import os

print("Adding to the path for main App ...")
current_folder = os.path.dirname(__file__)

sys.path.append(f"{current_folder}")
