from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
import datetime,json,urllib


class RoomAPI(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        alsoProvides(self.request, IDisableCSRFProtection)
        action = self.request.form.get('action', '').lower()
        fmt = self.request.form.get('fmt', 'json')
        callback = self.request.form.get('callback', '?')
        room_id = self.request.form.get('id', None)
        title = self.request.form.get('title', '')
        email = self.request.form.get('email', '')
        start = float(self.request.form.get('start', 0))
        end = float(self.request.form.get('end', 0))
        
        # print 'RoomAPI ================================================'
        # print 'Action: ' + action
        # print 'RoomId: ' + room_id
        # print 'Title: ' + title
        # print 'Email: ' + email
        # print 'Start: ' + str(start)
        # print 'End: ' + str(end)
        
        status = {
            'code' : 403,
        }
        
        if action == 'add' and room_id != None and email != '' and title != '' and start != 0 and end != 0:
            self.add_event(room_id,email,title,start,end)
            status['code'] = 200
        if action == 'get' and room_id != None and start != 0:
            status['data'] = self.get_event(room_id,start)
        status['code'] = 200
        if action == 'remove' and room_id != None and start > 0 and end > 0:
            self.remove_event(room_id,start,end)
            status['code'] = 200
        
        if fmt == 'jsonp':
            return callback + '(' + json.dumps(status) + ')'
        return json.dumps(status)

    def add_event(self,room_id,email,title,start,end):
        brains = api.content.find(context=api.portal.get(), id=room_id, portal_type='polklibrary.groupfinder.models.room')
        if len(brains) == 1:
            obj = brains[0].getObject()
            
            cache = obj.cached
            if cache == None:
                cache = '{}'
            cache = json.loads(cache)
            
            start_dt = datetime.datetime.fromtimestamp(start/1000.0)
            DateID = str(start_dt.strftime('%Y%m%d'))

            if DateID not in cache:
                cache[DateID] = []

            cache[DateID].append({
                'start' : int(start),
                'end' : int(end),
                'title' : title,
                'email' : email,
            })
            
            obj.cached = json.dumps(cache)
                
                
    def get_event(self,room_id,start):
        brains = api.content.find(context=api.portal.get(), id=room_id, portal_type='polklibrary.groupfinder.models.room')
        if len(brains) == 1:
            obj = brains[0].getObject()
            
            cache = obj.cached
            if cache == None:
                cache = '{}'
            cache = json.loads(cache)
            
            dt = datetime.datetime.fromtimestamp(start/1000.0)            
            dtID = str(dt.strftime('%Y%m%d'))
            if dtID in cache:
                return cache[dtID]
        return []
        
    def remove_event(self,room_id,start,end):
        if api.user.has_permission('Modify portal content', obj=self.context) or api.user.has_permission('Edit', obj=self.context):
            brains = api.content.find(context=api.portal.get(), id=room_id, portal_type='polklibrary.groupfinder.models.room')
            if len(brains) == 1:
                obj = brains[0].getObject()
                
                cache = obj.cached
                if cache == None:
                    cache = '{}'
                cache = json.loads(cache)
                
                start_dt = datetime.datetime.fromtimestamp(start/1000.0)
                DateID = str(start_dt.strftime('%Y%m%d'))

                if DateID in cache:
                    cache[DateID] = list(filter(lambda d: d['start'] != start and d['end'] != end, cache[DateID]))
                    obj.cached = json.dumps(cache)

    @property
    def portal(self):
        return api.portal.get()
        