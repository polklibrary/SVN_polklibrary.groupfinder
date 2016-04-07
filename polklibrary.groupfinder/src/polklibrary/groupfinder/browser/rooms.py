
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from polklibrary.google.hours.browser.hours import Hours
import datetime,json

class Rooms(BrowserView):

    template = ViewPageTemplateFile('rooms.pt')
   
    def __call__(self):
        return self.template()

    