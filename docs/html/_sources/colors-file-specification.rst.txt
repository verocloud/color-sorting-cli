.. _file_specification:

Color Palette File Specification
================================

============
Introduction
============

Most of the commands of Harmony receives the colors through a special text file. this tutorial shows how to write colors in this file.


==========
The Colors
==========

To pass colors to the file, all you need to do is pass the hexcode or the RGB format in to it. Every color must be in a separated line::

    (49, 6, 210)
    #0f8fb3
    (201, 118, 6)


RGB format must be written in the format ``(X, X, X)`` being ``d`` the components red, green and blue as an integer from 0 to 255. The hexcode format must be in the format ``#XXXXXX`` or ``#XXX`` being ``X`` the components red, green and blue as hex digits.


======
Labels
======

Being to facilitate the reading or to generate files as `.clr` and `.ase`, you can add labels to the colors. For that just write it after the color spefication, separated by a whitespace::

    (49, 6, 210) Dark Blue
    #0f8fb3 Light Blue
    (201, 118, 6) Orange