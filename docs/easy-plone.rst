Plone the easy way
==================

Creating a site with Plone is easy, but developing with Plone might seem 
daunting.

In fact it can be easy, and it does not necessarily involve learning a lot
about various complex frameworks.

Here are the **basics of easy developing with Plone**.

Install it
----------

Installing Plone is very easy (see the `installation documentation
<http://docs.plone.org/manage/installing/installation.html>`_).

Theme it
--------

`Diazo <http://docs.diazo.org/en/latest/>`_ is the Plone theming engine. Diazo
has a brilliant approach to theming: **it applies on top of Plone, not inside**.

Indeed, Plone produces content pages and Diazo can apply any theme on-the-fly to
those pages. So we do not need to know anything about Plone's internal mechanisms
to theme it.

Diazo only requires a **regular static theme** (HTML files, CSS, JS, etc.) and 
**some mapping rules** (specified in :file:`rules.xml`) which allows to specify
where each part of our Plone content pages must fit into our static design.

The Diazo theme can be built directly from the Plone interface in the Theming
editor. The Plone 5 default theme (named Barceloneta) can be copied and we can
modify whatever we want in this copy.

The copy can also be exported as a :file:`.zip` file, and imported back into the
same site (to restore a previous version), or on another site (for instance to
deploy a new theme from development to production).

If we are not comfortable with managing our theme implementation in a web-based
interface, we might also store it on our server in the Plone installation
folder::

    $INSTALL_FOLDER/resources/theme/my-theme

Extend it
---------

Plone can be extended in two ways.

We can `install add-ons <http://training.plone.org/5/add-ons.html>`_ developed
by the Plone community.

And we can also create our own specific content types using
`Dexterity <http://training.plone.org/5/dexterity.html>`_.

Dexterity is the Plone **content-type framework** and it allows to create new
content-types through the Plone web interface.

Like with Diazo, we are able to export what has been created online, so we can
import it again later or import it on another server.

Customize it
------------

Once we have changed the design with Diazo, we might want to re-organize or
enrich the content layouts themselves.

`Mosaic <http://plone-app-mosaic.s3-website-us-east-1.amazonaws.com/latest/>`_
is the **perfect solution to manipulate the content layout**: we can move existing
elements (like the title, description, etc.), but also add new ones.

Once a layout is created, it can be exported and copied in our Diazo
``manifest.cfg`` file so it can be available as a new layout for our users.

Diazo and Mosaic allows us to entirely control how information is displayed
in our web site, but they do not allow changing the _behavior_ of Plone, like
adding new features, new dynamically computed information, etc.

This can be achieved with **Rapido** (as explained in :doc:`./tutorial`), with a very
basic knowledge of HTML and Python (so, still, no need to learn about the
different Plone frameworks).

Our Rapido developments are managed in our existing theme folder, so here again
we can work online in the Plone theming editor, or in the ``/resources/theme``
folder.

Rapido provides easy access to the `Plone API <http://docs.plone.org/develop/plone.api/docs/>`_.
The Plone API gathers in one module many different Plone tools
allowing to search for contents, create contents, access user profiles
information, etc. It makes Plone internal features much more approachable,
and developing with Rapido might be a good opportunity to discover Plone
through its API.

And if we want...
-----------------

It might be sufficient to cover almost anything we might need to implement in
our Plone site.

But if at some point we feel comfortable enough with the Plone technical
environment, and if we want to learn more, then we might consider creating our
own Plone add-on.

Our add-on will handle our Diazo theme (including our Rapido development), our
Dexterity content-type definitions, and all our configuration settings.

This is properly documented in the `Plone documentation <http://docs.plone.org/develop/addons/index.html>`_,
and the `Plone training <http://training.plone.org/5/theming/theme-package.html>`_ might also be very helpful.
