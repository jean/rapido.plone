Python API
==========

Any Rapido Python function receives :py:obj:`context` as parameter.

The :py:obj:`context` provides the following properties:

.. contents::
    :local:

:py:obj:`context.app`
---------------------

This property gives access to the Rapido application object.

*Properties*

:py:obj:`acl`
    Returns the Rapido application's access control list object (see below).

:py:obj:`blocks`
    Returns the existing block ids.

:py:obj:`indexes`
    Returns the existing index ids.

:py:obj:`url`
    Returns the application URL.

*Methods*

:py:meth:`create_record(self, id=None)`
    Creates and return a new record.
    If ``id`` is not provided, a default one is generated.
    If ``id`` already exists, it is replaced with another one (like ``...-1``,
    ``...-2``).

:py:meth:`delete_record(self, id=None, record=None, ondelete=True)`
    Delete the record (which can be passed as object or id).
    If ``ondelete`` is truthy,
    the ``on_delete`` function will be called (if it exists)
    before deleting the record.

:py:meth:`get_block(self, block_id)`
    Returns a block.

:py:meth:`get_record(self, id)`
    Returns the record corresponding to the ``id``,
    or ``None`` if it does not exist.

:py:meth:`log(self, message)`
    Logs a message in the server log. If the app is in *debug* mode, logs
    the same message in the browser's javascript console.
    Messages can be strings or any other serializable object.

:py:meth:`records(self)`
    Returns all the records as a list.
    
:py:meth:`_records(self)`
    Returns all the records as a Python generator.

:py:meth:`search(self, query, sort_index=None, reverse=False)`
    Performs a search and returns records as a list.

:py:meth:`_search(self, query, sort_index=None, reverse=False)`
    Performs a search and returns records as a Python generator.

:py:obj:`context.request` and :py:obj:`context.parent_request`
--------------------------------------------------------------

:py:obj:`context.request` is the actual request to Rapido, like:

    http://localhost:8080/Plone/@@rapido/rating/blocks/rate

When a block is embedded in a Plone page,
:py:obj:`context.request` was issued by the user's browser,
it was issued by Diazo.

To get the request issued by the user's browser, we use
:py:obj:`context.parent_request`.

Both of them are HTTP requests objects, see the `reference documentation <http://docs.plone.org/develop/plone/serving/http_request_and_response.html>`_.

Examples:

- Reading submitted values:

.. code-block:: python

    val1 = context.request.get('field_1')  # returns None if key doesn't exist
    val1 = context.request['field_2']  # fail if key doesn't exist

- Reading the ``BODY``:

.. code-block:: python

    request.get('BODY')


:py:obj:`context.portal`
------------------------

Return the Plone portal object.

It is equivalent to:

.. code-block:: python

    context.api.portal.get()

The most common task we will perform through the portal object is to get its contents:

.. code-block:: python

    folder = context.portal['my-folder']

:py:obj:`context.content`
-------------------------

It returns the current Plone content.

The most common tasks we will perform on the content are:

- reading/writing its attributes (read/write):

.. code-block:: python

    the_tile = context.content.title
    context.content.title = "I prefer another title"

- getting its URL:

.. code-block:: python

    context.content.absolute_url()

To manipulate the content, refer to the `Plone API documentation about contents <http://docs.plone.org/develop/plone.api/docs/content.html>`_.

.. note::

    Depending on its content type, the content object might have very different methods and properties.

:py:obj:`context.record`
------------------------

It returns the current Rapido record if any.

See `Record`_ for more information.

:py:obj:`context.api`
---------------------

It gives access to the full `Plone API <http://docs.plone.org/develop/plone.api/docs/index.html>`_.

.. warning::

    There is no need to import the API, as shown in all the Plone API examples:

    .. code-block:: python

        from plone import api  # WRONG

    because the API is already available in the Rapido :py:obj:`context`:

    .. code-block:: python

        catalog = context.api.portal.get().portal_catalog

This API mainly allows:

- to search contents; for example:
    
    .. code-block:: python

        folders = context.api.content.find(portal_type="Folder")
        # be careful, the find() method returns Brain objects, not real objects
        # so only indexed attributes are available.
        desc = folders[0].Description # OK
        folders[0].objectIds() # WRONG!
        folder = folders[0].getObject()
        folder.objectIds() # OK!

- to manipulate contents (create / delete / move / publish / etc.), example:

    .. code-block:: python

        new_page = context.api.content.create(
            type='Document',
            title='My Content',
            container=context.content)
        context.api.content.transition(obj=new_page, transition='publish')


- to access or manage the users and groups information, and send emails. Example:

    .. code-block:: python

        current_user = context.api.user.get_current()
        context.api.portal.send_email(
            recipient=current_user.getProperty("email"),
            sender="noreply@plone.org",
            subject="Hello",
            body="World",
        )

For more detailed examples, refer to the `Plone API documentation <http://docs.plone.org/develop/plone.api/docs/index.html>`_.

:py:meth:`context.rapido`
-------------------------

:py:meth:`context.rapido` is a function able to obtain another Rapido application in our current script.

It takes as mandatory parameter the id of the Rapido application. Example:

.. code-block:: python

    purchase_app = context.rapido('purchase')
    new_purchase_order = purchase_app.create_record()

It might also accept a ``content`` parameter to provide a specific content
context to the app (if not provided, it will take the current content).
Example:

.. code-block:: python

    stat_app = context.rapido('stats', content=context.portal.news)

``context.modules``
-------------------

.. warning:: For security reason, it is not allowed to import a Python module in a Rapido Python file.

Rapido provides some safe modules through :py:obj:`context.modules`:

- :py:mod:`context.modules.datetime`: `Basic date and time types <https://docs.python.org/2/library/datetime.html>`_,
- :py:mod:`context.modules.random`: `Generate pseudo-random numbers <https://docs.python.org/2/library/random.html>`_,
- :py:mod:`context.modules.time`: `Time access and conversions <https://docs.python.org/2/library/time.html>`_.

If we need to add extra modules to :py:obj:`context.modules`, we can do it by adding in our own add-on something like:

.. code-block:: python

    import re
    from rapido.core import app

    app.safe_modules.re = re

In this example, we allow to access :py:mod:`context.modules.re` from our Rapido Python files.

Record
------

*Properties*

``url``
    Returns the record URL.

``id``
    Returns the record identifier.

*Methods*

:py:meth:`display(self, edit=False)`
    Render the record using its associated block (if any).

:py:meth:`get(self, name, default=None)`
    Returns the value of the item (and defaults to ``default`` if the item does
    not exist).

:py:meth:`items(self)`
    Returns all the stored items.

:py:meth:`reindex(self)`
    Re-index the record.

:py:meth:`save(self, request=None, block=None, block_id=None, creation=False)`
    Update the record with the provided items and index it.

    ``request`` can be an actual HTTP request or a dictionnary.

    If a block is mentionned, formulas (``on_save``, computed elements, etc.)
    will be executed.

    If no block (and ``request`` is a dict), we just save the items values.

:py:meth:`set_block(self, block_id)`
    Assign a block to the record. The block will be then used to render the
    record or to save it.

*Python dictionary-like interface*

The record's items can be accessed and manipulated like dictionary items:

.. code-block:: python

    myrecord['fruit'] = "banana"
    for key in myrecord:
        context.app.log(myrecord[key])
    if 'vegetable' in myrecord:
        del myrecord['fruit']

.. note::

    When setting an item value, the record is not reindexed.

Access control list
-------------------

.. note::

    The application access control list can be obtain by :py:obj:`context.app.acl`.

**Methods**

:py:meth:`current_user(self)`
    Returns the current user id.
    Equivalent to:

.. code-block:: python

    context.api.user.get_current().getUserName()

:py:meth:`current_user_groups(self)`
    Returns the groups the current user belongs to.
    Equivalent to:

.. code-block:: python

    api.user.get_current().getGroups()

:py:meth:`has_access_right(self, access_right)`
    Returns ``True`` if the current user has the specified access right (Rapido
    access rights are ``reader``, ``author``, ``editor``, ``manager``)

:py:meth:`has_role(self, role_id)`
    Returns ``True`` if the current user has the specified role.

:py:meth:`roles(self)`
    Returns the existing roles.
