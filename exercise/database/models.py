from .db import db

class Album(db.Document):
    name = db.StringField(unique=True)
    description=db.StringField()
class Photo(db.Document):
    name = db.StringField(required=True)
    tags=db.ListField(db.StringField())
    location=db.StringField()
    image_file=db.ImageField()
    albums= db.ListField(db.ReferenceField('Album',reverse_delete_rule=2))
    