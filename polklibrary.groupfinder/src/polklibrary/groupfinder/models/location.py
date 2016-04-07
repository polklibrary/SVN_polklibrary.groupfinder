from plone import api
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema


class ILocation(model.Schema):

    title = schema.TextLine(
            title=u"Room Name",
            required=True,
        )

    location = schema.TextLine(
            title=u"Location",
            required=False,
        )
        
    calendar_id = schema.TextLine(
            title=u"Calendar ID",
            required=False,
        )
        
    body = RichText(
            title=u"Information on the room",
            default_mime_type='text/structured',
            required=False,
            default=u"",
        )
        
    image = NamedBlobImage(
            title=u"Room Image",
            required=False,
        )
        






         