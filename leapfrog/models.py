from leapfrog import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True)

    def serializeable(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }


class Transfer(db.Model):
    """
    This relation represents the transfer of a leapfrog from one user to another.
    """

    __tablename__ = 'transfers'
    id = db.Column(db.Integer, primary_key=True)
    old_holder_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    new_holder_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    leapfrog_id = db.Column(db.ForeignKey('leapfrogs.id'), nullable=False)
    transfer_number = db.Column(db.Integer)

    old_holder = db.relationship('User', foreign_keys=[old_holder_id])
    new_holder = db.relationship('User', foreign_keys=[new_holder_id])
    leapfrog = db.relationship('Leapfrog', foreign_keys=[leapfrog_id])

    def serializeable(self):
        return {
            'id': self.id,
            'old_holder_id': self.old_holder_id,
            'new_holder_id': self.new_holder_id,
            'leapfrog_id': self.leapfrog_id,
            'transfer_number': self.transfer_number,
        }


class Leapfrog(db.Model):
    __tablename__ = 'leapfrogs'
    id = db.Column(db.Integer, primary_key=True)
    current_holder_id = db.Column(db.ForeignKey('users.id'), nullable=False)

    holder = db.relationship('User', foreign_keys=[current_holder_id])

    def serializeable(self):
        return {
            'id': self.id,
            'current_holder_id': self.current_holder_id
        }