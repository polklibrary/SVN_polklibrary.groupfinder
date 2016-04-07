
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import datetime,json

class Location(BrowserView):

    template = ViewPageTemplateFile('location.pt')
   
    def __call__(self):
        return self.template()

    