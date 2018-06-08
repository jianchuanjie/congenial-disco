from . import db


class User(db.Model):
    '''
    This is Users models, very very simple because of laziness
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def verify(self, pd):
        if pd == password:
            return True
        else:
            return False

