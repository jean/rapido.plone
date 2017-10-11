Principles
==========

Creating a Rapido app
---------------------

Here are the basic steps to create a Rapido app:

- go to the theme folder (in :menuselection:`Plone setup --> Theme` if we prefer to work inline,
  or, if your prefer to work in the filesystem,
  it might be either in the :file:`static` folder in your theme package,
  or in the :file:`resources` folder in your Plone install if you do not have a custom package),
- add a new folder named :file:`rapido`,
- in :file:`rapido`, add a new folder named :file:`myapp`.

That's it.

Now, we can implement our application in this folder.
Here is a typical layout for a rapido app::

    /rapido
        /myapp
            settings.yaml
            /blocks
                stats.html
                stats.py
                stats.yaml
                tags.html
                tags.py
                tags.yaml

.. note::

    :file:`settings.yaml` is not mandatory, but it allows defining access rights if needed.

.. note::

    A Rapido application can also be located in a non-active theme (see :doc:`./reference/application`)

The app components are ``blocks``. A block is defined by a set of 3 files (HTML,
Python, and YAML) located in the :file:`blocks` folder.

The **YAML file** defines the elements. An element is any dynamically generated
element in a block: it can be a form field (input, select, etc.), but
also a button (``ACTION``), or even just a piece of generated HTML (``BASIC``).

The **HTML file** contains the layout of the block. The templating mechanism is
super simple, elements are just enclosed in brackets, like this:
``{my_element}``.

The **Python file** contains the application logic. It is a set of functions,
each named for the element or the event it corresponds to.

For a ``BASIC`` element, for instance, we need to provide a function with
the same name as the element; its return-value replaces the element in the
block.

For an ``ACTION``, we are supposed to provide a function with the same name as
the element; in this case, it will be *executed* when a user clicks on the
action button.

Here is a basic example:

- :file:`rapido/myapp/blocks/simpleblock.yaml`:

  .. code-block:: yaml
  
      elements:
          result: BASIC
          do_something:
              type: ACTION
              label: Do something

- :file:`rapido/myapp/blocks/simpleblock.html`:

  .. code-block:: html
  
      <p>the answer to life, the universe, and everything is {result}</p>
      {do_something}

- :file:`rapido/myapp/blocks/simpleblock.py`:

  .. code-block:: python
  
      def result(context):
          return "<strong>42</strong>"
  
      def do_something(context):
          context.app.log('Hello')

We can see our block by visiting the following URL:

    http://localhost:8080/Plone/@@rapido/myapp/blocks/simpleblock

It works fine, but where is our Plone site now??

Inserting our block in a Plone page
-----------------------------------

To put our block somewhere in the Plone site, we use a Diazo rule:

.. code-block:: xml

    <before css:content="#content-core">
        <include css:content="form" href="/@@rapido/myapp/blocks/simpleblock" />
    </before>

Now, if we visit any page of our site, we will see our block.

.. note::

    If we want to display it only in the _News_ folder, we would use
    ``css:if-content``:

    .. code-block:: xml

        <before css:content="#content-core" css:if-content=".section-news">
            <include css:content="form" href="/@@rapido/myapp/blocks/simpleblock" />
        </before>

    See the `Diazo <http://docs.diazo.org/en/latest/>`_ documentation for more details.

But unfortunately, when we click on our :guilabel:`Do something` button, we are redirected
to the original bare block.

To remain in the Plone page, we need to activate the ``ajax`` target in
:file:`rapido/myapp/blocks/simpleblock.yaml`:

.. code-block:: yaml

    target: ajax
    elements:
        result: BASIC
        do_something:
            type: ACTION
            label: Do something

Now, when we click our button, the rapido block is reloaded inside the Plone
page.

Instead of adding a block to an existing Plone view, we might need to provide a
new rendering, mapped to a specific URL.
We can do that by declaring our block as a Plone view in its YAML file:

.. code-block:: yaml

    view:
      id: my-custom-view
      with_theme: true

And then we call ``@@my-custom-view`` on any content, like:

    http://localhost:8080/Plone/news/@@my-custom-view

We can create as many views as we might need (like ``@@subscribe``, ``@@unsubscribe``, ``@@stats``, ...).

.. note::

    Adding a lot of rapido rules in our main :file:`rules.xml` is not ideal.
    
    We might prefer to create a :file:`rules.xml` file in our :file:`rapido/myapp`
    folder, and include it in our main :file:`rules.xml` file like this:

    .. code-block:: xml

        <xi:include href="rapido/myapp/rules.xml" />

Running Python code
-------------------

Every function in our Python files takes a parameter named ``context``.
The context gives access to useful objects:

``context.app``
   the current rapido app,

``context.block``
   (if executed in a block context) the current block,

``context.record``
   (if executed in a record context) the current record,

``context.request``
   the current request to rapido (the sub-request, if called from Diazo),

``context.parent_request``
   the current page request (when called from Diazo),

``context.portal``
   the Plone portal object,

``context.content``
   the current Plone content object,

``context.api``
   the `Plone API <http://docs.plone.org/external/plone.api/docs/>`_.

.. warning::

    ``context`` is not the usual ``context`` we know in Plone (like :py:obj:`context`
    in a ZPT template or a PythonScript, or :py:obj:`self.context` in a BrowserView).
    
    The Plone ``context`` is usually the current content. In Rapido
    we can obtain it using :py:obj:`context.content`.

This allows us to interact with Plone in many ways, for instance we can
run catalog queries, create contents, change workflow status, etc.

Nevertheless, it will behave as expected:

- the code will always be executed with the current user's access right, so the
  appropriate Plone access restrictions will be applied,
- the CSRF policy will also be applied (for instance, a Plone operation marked
  as ``PostOnly`` would fail if performed in a GET request).

.. note::

    The code we put in our Python files is compiled and executed in a
    sandboxed environment (provided by `zope.untrustedpython.interpreter 
    <https://github.com/zopefoundation/zope.untrustedpython/blob/master/docs/narr.rst>`_).

To help us debugging our code, we can add:

.. code-block:: yaml

    debug: true

in our app :file:`settings.yaml` file. Then we can add some log message in our code:

.. code-block:: python

    context.app.log("OK")
    context.app.log({"something": 1)

and they will be display in both the server log and the browser's javascript
console.

Storing and retrieving data
---------------------------

A rapido app provides a builtin storage service, based on
`Souper <https://pypi.python.org/pypi/souper>`_.

.. note::

    Souper is designed to store (and index) huge amounts of small data (it can
    easily store survey results, comments, ratings, etc., but it will not be
    appropriate for attached files for instance).

The Rapido storage service stores **records**, and records contain **items**.

There are 3 ways to create records in Rapido:

- we can create records by submitting a block: if a
  block contain some fields elements (like ``TEXT`` or ``NUMBER`` elements for
  instance), and if the block contains a :guilabel:`save` button (by adding ``{_save}`` in
  its layout), every time the user enters values in the fields and clicks
  save, the submitted values will be saved in a new record,
- we can create records by code::
    
    record = context.app.create_record(id='myrecord')

- we can create records using the Rapido JSON REST API::

    POST /:site_id/@@rapido/:app_id
    Accept: application/json
    {"item1": "value1"}

  or::

    PUT /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    {"item1": "value1"}

The same goes for accessing data:

- we can display records by calling their URL, and they will be rendered using
  the block they were created with::

    /@@rapido/myapp/record/myrecord

- we can get a record by code:

  .. code-block:: python
  
      record = context.app.get_record(id='myrecord')
      some_records = context.app.search('author=="JOSEPH CONRAD"')

- we can get records using the Rapido JSON REST API::

    GET /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json

Integration with Plone
----------------------

In addition to the Diazo injection of Rapido blocks in our theme, we can also
integrate our Rapido developments in Plone using:

- Mosaic: Rapido provides a Mosaic tile which enables us to insert a Rapido
  block in our page layout.

- Content Rules: Rapido provides a Plone *content rule action* allowing us to
  call a Python function from a block when a given Plone event happens.

- `Mockup <http://plone.github.io/mockup/dev/>`_ patterns:
  the *modal* and the *content loader* patterns can load and display Rapido blocks.

See :doc:`reference/display`.
