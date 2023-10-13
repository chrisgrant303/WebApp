from database import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Association table for many-to-many relationship between Group and Resource
group_resources_association = db.Table('group_resources',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
)

# ... Inside the Group class definition ...

resources = db.relationship('Resource', secondary=group_resources_association, backref='groups')
