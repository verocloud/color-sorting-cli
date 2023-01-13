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

For installing the CLI, you can download the `.whl` file from [here](https://github.com/AdrianSimionov/color-sorting-cli/releases/download/0.5.0/harmony-0.5.0-py3-none-any.whl) and run the following command:

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

### Sort the colors

- Now we will run the following command:

```
$ harmony sort color.txt
```

- After that, a file named `colors_hillbert_sorted.txt` should be generated in the same directory with the following content:

```
(201, 118, 6) Orange
#0f8fb3 Light Blue
(49, 6, 210) Dark Blue
```


## More Information

For more information on how to use the Harmony, check the [full documentation](https://xlurio.github.io/harmony-docs/).