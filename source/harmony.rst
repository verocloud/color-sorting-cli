Harmony
=======
*Easily organize your color pallete*

-------------------------------------

Harmony is a CLI that provides multiple tools for managing you color palettes.

============
Requirements
============

- Python 3.8+

Built over:

- `typer <https://typer.tiangolo.com/>`_
- `rich <https://rich.readthedocs.io/en/latest/>`_


==========
Installing
==========

For installing the CLI, you can download the `.whl` file from `here <https://github.com/AdrianSimionov/color-sorting-cli/releases/download/0.4.2/harmony-0.4.2-py3-none-any.whl>`_ and run the following command:

- On Windows::


    $ pip install --user harmony-{version}-py3-none-any.whl

    ---> 100%

- On Linux::

    $ pip3 install --user harmony-{version}-py3-none-any.whl
    
    ---> 100%


=================================
Example - Sorting a color palette
=================================

####################
Create a colors file
####################

 - The first step is to write the colors in a file called ``colors.txt`` (for the file specification, see :ref:`file_specification`)::

    (49, 6, 210) Dark Blue
    #0f8fb3 Light Blue
    (201, 118, 6) Orange


###############
Sort the colors
###############

- Now we will run the following command::

    $ harmony sort color.txt

- After that, a file named `colors_hillbert_sorted.txt` should be generated in the same directory with the following content::

    (201, 118, 6) Orange
    #0f8fb3 Light Blue
    (49, 6, 210) Dark Blue
