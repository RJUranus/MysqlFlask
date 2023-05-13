from ext import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #也是视频收藏号，与视频收藏表关联，得到收藏号去视频收藏表中查找收藏的视频id
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    stu_id = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class VideoUri(db.Model):
    __tablename__ = 'videouri'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    #视频id
    video_title = db.Column(db.Text, nullable=False)                    #视频标题
    video_label = db.Column(db.Text, nullable=False)                    #视频分类
    video_uri = db.Column(db.String(100), nullable=False)


class FavoriteVideo(db.Model):
    __tablename__ = 'favorite'
    favorite_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videouri.id'), primary_key=True)


class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)