import os
import sys
from tkinter import Canvas, Misc, Tk
from dataclasses import dataclass
from typing import List, Tuple

TOTAL_WIDTH = 1000
AMOUNT_OF_COLORS = 6


def get_colors_file(file_name: str):
    this_directory_path = os.path.dirname(__file__)
    this_directory_absolute_path = os.path.abspath(this_directory_path)

    return os.path.join(this_directory_absolute_path, file_name)


@dataclass
class ColorSliceData:
    slice_start: float
    slice_end: float
    hexcode: str


class ColorSliceSetFactory:
    def make_set(self, colors_file_name: str) -> Tuple[ColorSliceData, ...]:
        color_strings: List[str] = []

        colors_file_path = get_colors_file(colors_file_name)

        with open(colors_file_path, "r", encoding="utf8") as colors_file:
            color_strings = colors_file.readlines()

        return self._get_color_slices(color_strings)

    def _get_color_slices(self, color_strings: List[str]) -> Tuple[ColorSliceData, ...]:
        color_slices: List[ColorSliceData] = list()
        slice_start: float = 0
        slice_end: float = (1 / AMOUNT_OF_COLORS) * TOTAL_WIDTH

        for color_string in color_strings:
            hexcode = color_string.replace("\n", "")
            hexcode = hexcode.replace(" ", "")

            new_color_slice = ColorSliceData(
                slice_start=slice_start, slice_end=slice_end, hexcode=hexcode
            )
            color_slices.append(new_color_slice)

            slice_start += (1 / AMOUNT_OF_COLORS) * TOTAL_WIDTH
            slice_end += (1 / AMOUNT_OF_COLORS) * TOTAL_WIDTH

        return tuple(color_slices)


class ColorSpectrum(Canvas):
    def __init__(
        self,
        master: Misc,
        colors_file_name: str,
        **kwargs: object,
    ) -> None:
        super().__init__(master=master, cnf={}, **kwargs)

        factory = ColorSliceSetFactory()
        color_slices = factory.make_set(colors_file_name)

        for slice in color_slices:
            self.create_rectangle(
                slice.slice_start,
                0,
                slice.slice_end,
                100,
                outline=slice.hexcode,
                fill=slice.hexcode,
            )


class Application(Tk):
    """Main application"""

    def __init__(self, colors_file_name: str) -> None:
        super().__init__(className=str(self.__class__))
        self.title("Color Visualization")
        self.geometry(f"{TOTAL_WIDTH}x100")

        color_spectrum = ColorSpectrum(
            self, colors_file_name=colors_file_name, width=TOTAL_WIDTH
        )
        color_spectrum.pack()


if __name__ == "__main__":
    colors_file_name = "colors_hillbert_sorted.txt"

    passed_arguments = sys.argv
    arguments_was_passed = len(passed_arguments) > 1

    if arguments_was_passed:
        colors_file_name = passed_arguments[1]

    app = Application(colors_file_name)
    app.mainloop()
