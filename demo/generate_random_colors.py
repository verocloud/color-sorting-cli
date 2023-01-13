import os
import random

AMOUNT_OF_COLORS = 6
file_content: str = ""

MAXIMUM_RGB_VALUE = 255

for line in range(AMOUNT_OF_COLORS):
    red = random.randint(0, MAXIMUM_RGB_VALUE)
    green = random.randint(0, MAXIMUM_RGB_VALUE)
    blue = random.randint(0, MAXIMUM_RGB_VALUE)

    file_content += f"({red}, {green}, {blue})\n"

this_directory_path = os.path.dirname(__file__)
this_directory_absolute_path = os.path.abspath(this_directory_path)
new_file_path = os.path.join(this_directory_absolute_path, "colors_file.txt")

with open(new_file_path, "w", encoding="utf8") as new_file:
    new_file.write(file_content)
