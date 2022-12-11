txt2clr
=======

============
Introduction
============

Command to convert a given color palette file (see :ref:`file_specification`) to Apple ``.clr`` format.

.. versionadded:: 0.4.0

    Created the command with the name ``txt2clr``


=======
Example
=======

Given the file ``colors.txt`` with the following content (see :ref:`file_specification`)::

    (49, 6, 210) Dark Blue
    #0f8fb3 Light Blue
    (201, 118, 6) Orange
    (84, 62, 115) Violet
    #b52871 Dark Pink
    (84, 16, 13) Dark Red


All we need to do is run the following command::

    $ harmony txt2clr colors.txt


And we have a ``colors.clr`` in the MacOS CLR format.

=========
Arguments
=========

.. program:: harmony txt2clr

.. option:: colors-file

    The Harmony color palette file (see :ref:`file_specification`) to be converted to ``.clr`` format.


=======
Options
=======

.. program:: harmony txt2clr

.. option:: --help

    Display the options and information about the command;