from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from rapido.core.browser import views as core

class OpenForm(core.OpenForm):

    template = ViewPageTemplateFile('templates/openform.pt')