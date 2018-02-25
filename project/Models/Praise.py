import uuid
from project import db

class Praise(db.Model):
    __tablename__ = "praise"
    id = db.Column(db.String(16), primary_key=True, nullable=False)
    card_id = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.String(16), nullable=False)
    # 希望这两个方法成功后返回True,失败返回False
    # 不需要insert方法和update方法了，集成在这两个方法中

    def create_praise(self, user_id, card_id):
        try:
            id = str(uuid.uuid1()).split("-")[0]
            self.card_id = card_id
            self.user_id = user_id
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

    def del_praise(self, user_id, card_id):
        try:
            i = self.query.filter_by(
                card_id=card_id, user_id=user_id).first()
            db.session.delete(i)
            db.session.commit()
        except:
            return False
        else:
            return True

    def find_praise_number(card_id):  # 查找某卡片的获赞的数量
        _all = Praise.query.filter(Praise.card_id == card_id).all()
        p_number = len(_all)
        return p_number

    def find_all_praise(self, card_id):  # 查找赞过该卡片的所有人，只显示人的nickname
        _all = self.query.filter_by(card_id=card_id).all()
        p_people = []
        for p in _all:
            that_one = User.query.filter_by(user_id=p.user_id).first()
            p_people.append(that_one.user_nickname)
        return p_people
        # 返回所有赞过的人的昵称的列表（这个如果要返回更多信息待议)
    
    def check_praise(user_id,card_id):
        if Praise.query.filter(Praise.user_id == user_id,
                                Praise.card_id == card_id).first():
            return True
        else:
            return False
