import os
from tkinter import Canvas, Misc, Tk
from dataclasses import dataclass
from typing import List, Tuple

TOTAL_WIDTH = 300


def get_colors_file():
    this_directory_path = os.path.dirname(__file__)
    this_directory_absolute_path = os.path.abspath(this_directory_path)

    return os.path.join(this_directory_absolute_path, "colors_file_sorted.txt")


@dataclass
class ColorSliceData:
    slice_start: float
    slice_end: float
    hexcode: str


class ColorSliceSetFactory:
    def make_set(
        self, colors_file_path: str = get_colors_file()
    ) -> Tuple[ColorSliceData, ...]:
        color_strings: List[str] = []

        with open(colors_file_path, "r", encoding="utf8") as colors_file:
            color_strings = colors_file.readlines()

        return self._get_color_slices(color_strings)

    def _get_color_slices(self, color_strings: List[str]) -> Tuple[ColorSliceData, ...]:
        color_slices: List[ColorSliceData] = list()
        slice_start: float = 0
        slice_end: float = (1 / 1000) * TOTAL_WIDTH

        for color_string in color_strings:
            hexcode = color_string.replace("\n", "")
            hexcode = hexcode.replace(" ", "")

            new_color_slice = ColorSliceData(
                slice_start=slice_start, slice_end=slice_end, hexcode=hexcode
            )
            color_slices.append(new_color_slice)

            slice_start += (1 / 1000) * TOTAL_WIDTH
            slice_end += (1 / 1000) * TOTAL_WIDTH

        return tuple(color_slices)


class ColorSpectrum(Canvas):
    def __init__(self, master: Misc) -> None:
        super().__init__(master=master, cnf={})

        factory = ColorSliceSetFactory()
        color_slices = factory.make_set()

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

    def __init__(self) -> None:
        super().__init__(className=str(self.__class__))
        self.title("Color Visualization")
        self.geometry(f"{TOTAL_WIDTH}x100")

        color_spectrum = ColorSpectrum(self)
        color_spectrum.pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
