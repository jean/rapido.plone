Associated Python functions
===========================

For a ``BASIC`` element, the associated Python function (having the same id)
will return the content of the element.

For field elements (``TEXT``, ``NUMBER``, ``DATETIME``), the associated Python
function will return its default value.

For an ``ACTION`` element, the associated Python function will be executed when
the action is triggered.

Special Python functions
------------------------

:py:func:`on_save`
    Executed when a record is saved with the block.
    If it returns a value, it must be a string, and it will be used as a
    redirection URL for the current request.

:py:func:`on_display`
    Executed when a block is displayed. It will be executed before all the element functions.
    It can be used to do some computation and put the result in the :py:obj:`context` so it can be accessed by the different elements.
    It can also be used to redirect to another page (using :py:meth:`context.request.response.redirect()`).

:py:func:`on_delete`
    Executed when a record is deleted.
    If it returns a value, it must be a string, and it will be used as a
    redirection URL for the current request.

:py:func:`record_id`
    Executed at creation time to compute the record id.
