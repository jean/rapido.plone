from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.actions import ActionAddForm, ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zExceptions import NotFound
from zope.component import adapts
from zope.interface import implements, Interface
from zope import schema

from rapido.plone import _
from rapido.plone.app import get_app


class IAction(Interface):
    """Interface for the configurable aspects of a rapido action.

    This is also used to create add and edit forms, below.
    """

    app = schema.TextLine(title=_(u"Rapido application"),
        description=_(u"The targeted Rapido application."),
        required=True)

    form = schema.TextLine(title=_(u"Form"),
        description=_(u"The form containing the method."),
        required=True)

    method = schema.TextLine(title=_(u"Method"),
        description=_(u"The name of the method to execute."),
        required=True)


class Action(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IAction, IRuleElementData)

    app = ''
    form = ''
    method = ''

    element = 'rapido.plone.Action'

    @property
    def summary(self):
        return _(u"Call Rapido method ${method} from ${app}/${form}",
            mapping=dict(app=self.app, method=self.method, form=self.form))


class ActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        try:
            app = get_app(self.element.app, request)
        except NotFound:
            api.portal.show_message(
                message="Rapido application %s cannot be found." % (
                    self.element.app,),
                request=request,
                type='error',
            )
            return True
        form = app.get_form(self.element.form)
        form.compute_field(self.element.method, {'form': form})
        return True


class AddForm(ActionAddForm):
    """An add form for rapido action.
    """
    schema = IAction
    label = _(u"Add Rapido Action")
    description = _(u"A Rapido action executes a Rapido method.")
    form_name = _(u"Configure element")
    Type = Action


class AddFormView(ContentRuleFormWrapper):
    form = AddForm


class EditForm(ActionEditForm):
    """An edit form for rapido action.
    """
    schema = IAction
    label = _(u"Edit Rapido Action")
    description = _(u"A Rapido action executes a Rapido method.")
    form_name = _(u"Configure element")


class EditFormView(ContentRuleFormWrapper):
    form = EditForm