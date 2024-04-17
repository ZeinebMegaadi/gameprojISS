import os

character_path = '../gameproj/graphics/player/'

if os.path.exists(character_path):
    print(f"The path '{character_path}' exists.")
else:
    print(f"The path '{character_path}' does not exist. Please check it.")
