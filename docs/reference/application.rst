Application
===========

A Rapido application is defined by a folder in the :file:`rapido` folder in the
current theme.

The application folder might contain a :file:`settings.yaml` file in its root but
that is not mandatory. It allows to define the access control settings
(see :doc:`./access`), or to enable the ``debug`` mode.

It always contains a :file:`blocks` folder containing its blocks (see :doc:`./blocks`).

It might also contain regular theme items (:file:`rules.xml`, CSS, Javascript, etc.).

Locating a Rapido application outside the current theme
-------------------------------------------------------

If we use a lot of Rapido applications,
or if the theme and the Rapido apps are managed by different persons,
it might be preferable to locate the Rapido apps in a dedicated theme.

To do so, we just need to reference it using a :file:`.lnk` text file in the current theme.
The filename should be the app id, and its content must be the theme id.

For instance, our active theme would be structured like this::

    /rapido
        myapp.lnk

The :file:`myapp.lnk` content would be just::

    dev-theme

The ``dev-theme`` theme would contain the full ``myapp`` Rapido app::

    /rapido
        /myapp
            settings.yaml
            /blocks
                stats.html

And everything will work just like if the :file:`myapp` folder was in our active theme.
