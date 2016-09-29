
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import datetime,json,urllib

class GroupFinder(BrowserView):

    template = ViewPageTemplateFile('groupfinder.pt')
   
    def __call__(self):
        self.request.response.setHeader('Cache-Control', 'max-age=60, s-maxage=60, public, must-revalidate')
        return self.template()

    def get_today(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')
    
    def get_locations_json(self):
        return json.dumps(self.get_locations())
    
    def get_locations(self):
        locations = []
        brains = api.content.find(context=api.portal.get(), portal_type='polklibrary.groupfinder.models.location')
        for brain in brains:
            location = brain.getObject()
            body = ''
            if location.body:
                body = location.body.output
            locations.append({
                'Title': str(location.Title()),
                'calendar_id': str(location.calendar_id),
                'image': location.absolute_url() + '/@@download/image/' + str(location.image.filename),
                'getURL': location.absolute_url(),
                'body': body,
            })
        return locations
   
    @property
    def portal(self):
        return api.portal.get()
        