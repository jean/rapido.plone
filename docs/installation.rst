Installation
============

Install Plone, then modify :file:`buildout.cfg` to add Rapido as a dependency:

.. code-block:: ini

   eggs =
       ...
       rapido.plone

   [versions]
   plone.resource = 1.2

Then, run your buildout:

.. code-block:: console

    $ bin/buildout -N
