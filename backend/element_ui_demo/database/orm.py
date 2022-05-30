from database.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    sex = db.Column(db.String(8))
    bir = db.Column(db.Date)
    address = db.Column(db.String(128))

    __tablename__ = "t_user"

    def __repr__(self):
        return '<User %r>' % self.name

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

if __name__ == '__main__':

    u = User(
        id=1,
        name="张三",
        sex="男",
        bir="2022-05-25",
        address="广州市天河区网易"
    )
    db.session.add(u)
    db.session.commit()