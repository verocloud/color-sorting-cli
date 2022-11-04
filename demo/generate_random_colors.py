import os
import random

file_content: str = ""


for line in range(1000):
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    file_content += f"({red}, {green}, {blue})\n"

this_directory_path = os.path.dirname(__file__)
this_directory_absolute_path = os.path.abspath(this_directory_path)
new_file_path = os.path.join(this_directory_absolute_path, "colors_file.txt")

with open(new_file_path, "w", encoding="utf8") as new_file:
    new_file.write(file_content)
