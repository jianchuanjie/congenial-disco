from . import db


class User(db.Model):
    '''
    This is Users model, very very simple because of laziness.
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %s>' % self.username

    def verify(self, pd):
        if pd == password:
            return True
        else:
            return False


class Photo_Path(db.Model):
    '''
    This is a model used for save paths of photos that users generate.
    '''

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='user', lazy=True)

    def __repr__(self):
        return '<Photo_Path %s>' % self.path
