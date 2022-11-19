<h1 align="center">Harmony</h1>
<p align="center">
    <em>Easily organize your color pallete</em>
</p>

---

Harmony is an easy-to-use CLI that allow you to order your color using multiple algorithms to achieve the perfect organization for your color palette.


## Requirements

- Python 3.8+

Built over:
- [typer](https://typer.tiangolo.com/)
- [rich](https://rich.readthedocs.io/en/latest/)


## Installing

<<<<<<< HEAD
For installing the CLI, you can download the `.whl` file from [here](https://github.com/AdrianSimionov/color-sorting-cli/releases/download/0.3.0/harmony-0.3.0-py3-none-any.whl) and run the following command:
=======
For installing the CLI, you can download the `.whl` file from [here](https://github.com/AdrianSimionov/color-sorting-cli/releases/download/0.2.1/harmony-0.2.1-py3-none-any.whl) and run the following command:
>>>>>>> main

- On Windows:
```
$ pip install --user harmony-{version}-py3-none-any.whl

---> 100%
```

- On Linux:
```
$ pip3 install --user harmony-{version}-py3-none-any.whl

---> 100%
```


## Example

### Create a colors file

 - The first step is to create a file in which, every line is a color and the color is specified at the beginning of the line using the `(X, X, X)` format for RGB and `#XXX` or `#XXXXXX` for Hexcode. In this example we will use a file named `colors.txt` with the following content:

```
(49, 6, 210) Dark Blue
#0f8fb3 Light Blue
(201, 118, 6) Orange
```


- Now we will run the following command:

```
$ harmony color.txt
```

- After that, a file named `colors_hillbert_sorted.txt` should be generated in the same directory with the following content:

```
(201, 118, 6) Orange
#0f8fb3 Light Blue
(49, 6, 210) Dark Blue
```


<<<<<<< HEAD
## Commands

### sort

The `sort` command sorts a text according to the [above specification](#create-a-colors-file). It receives a text file path and provides the following options:

* --sorting-algorithm [default: hillbert]: determine which algorithm should be used to sort the colors:
  * rgb: Sort the colors based on their RGB values;
  * hsv: Sort the colors based on their HSV values;
  * hsl: Sort the colors based on their HSL values;
  * luminosity: Sort the colors based on their perceived luminosity;
  * step: Sort the colors based on their hue, luminosity and *value* splitting them in 8 steps and sorting them separately;
  * step-alternated: Same as step, but the luminosity step is alternated forward and backward, bringing a sensation of continuity;
  * hillbert: Sort the colors based on their proximity in Hillbert Curves calculated on top of the RGB values;

=======
## Options

* --sorting-algorithm [default: hillbert]: determine which algorithm should be used to sort the colors:
  * rgb: Sort the colors based on their RGB values;
  * hsv: Sort the colors based on their HSV values;
  * hsl: Sort the colors based on their HSL values;
  * luminosity: Sort the colors based on their perceived luminosity;
  * step: Sort the colors based on their hue, luminosity and *value* splitting them in 8 steps and sorting them separately;
  * step-alternated: Same as step, but the luminosity step is alternated forward and backward, bringing a sensation of continuity;
  * hillbert: Sort the colors based on their proximity in Hillbert Curves calculated on top of the RGB values;

>>>>>>> main
* --color-format [default: input]: determine which format to output the colors:
  * input: The output format will be the same as the input format;
  * rgb: The output for all colors will be in RGB format;
  * hexcode: The output for all colors will be in Hexcode format;

* --direction [default: backward]: determine the direction of the sorting:
  * forward: the colors will be sorted in the natural order of the algorithms
  * backward: the colors will be sorted in the reversed order of the algorithms

* --suffix [default: _sorted]: determine the suffix of the output file;

<<<<<<< HEAD
* --help: display the options;


### toase

`toase` command allow to convert a text file that follows the [above specification](#create-a-colors-file) to a `.ase` file. It receives a text file and provide the following options:

* --palette_name [default: Palette {UUID4} sorted by Harmony]: determine the name of the palette to be written to the `.ase` file;
=======
* --help: display the options;
>>>>>>> main
