<p align="center">
  <h1>Harmony</h1>
</p>
<p align="center">
    <em>Easily organize you color pallete</em>
</p>

---

Harmony is an easy-to-use CLI that allow you to order your color using multiple algorithms to achieve the perfect organization for your color palette.


## Requirements

- Python 3.8+

Built over:
- [typer](https://typer.tiangolo.com/)
- [rich](https://rich.readthedocs.io/en/latest/)


## Installing

For installing the CLI, you can download the `.whl` file from [here](#) and run the following command:

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

 - The first step is to create a file where, every line is a color where the color is specified at the beginning of the line using the `(X, X, X)` format for RGB and `#XXX` or `#XXXXXX` for Hexcode. In this example we will use a file named `colors.txt` with the following content:

```
(49, 6, 210) Dark Blue
#0f8fb3 Light Blue
(201, 118, 6) Orange
```


- Now we will run the following command:

```
$ harmony color.txt
```

- After that, a file named `colors_sorted.txt` should be generated in the same directory with the following content:

```
(201, 118, 6) Orange
#0f8fb3 Light Blue
(49, 6, 210) Dark Blue
```


## Parameters

For more information about the parameters of the CLI, you can run the following command:

```
$ harmony --help
```