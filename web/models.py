# 存放数据模型相关代码
# i love nuonuo
# author:KRzhao

from datetime import datetime
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# 注意这里不再传入 app 了
db = SQLAlchemy()


class Base(db.Model):
    """ 所有 model 的一个基类， 默认添加了时间戳 """
    # 不将这个类当作 Model 类
    __abstract__ = True
    # 设置了 default 和 onupdate，这两个时间戳不需要手动维护
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class User(Base, UserMixin):
    """ 用户数据模型, 使用 flask_login 的 UserMixin 提供 session 管理功能, 实现用户
    的登录 登出 记住用户等功能 """
    __tablename__ = 'user'

    # 用数值表示角色, 用于判断是否有权限
    ROLE_USER = 10
    ROLE_ADMIN = 20
    ROLE_MASTER = 777

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    # sqlalchemy 会以属性名来定义数据表字段名, 这里需要使用私有属性, 所以明确指定数据表字段名
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    articles = db.relationship('Article')

    def __repr__(self):
        """ 显示一个可读字符串, 方便调试 """
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """ Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, orig_password):
        """ Python 风格的 setter, 设置 user.password 时,
        自动将 password 生成哈希值再存入数据数据表 """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 判断输入的密码和数据表储存的密码是否相等 """
        return check_password_hash(self._password, password)

    @property
    def is_nuonuo(self):
        return self.role == self.ROLE_NUONUO

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class Article(Base):
    """ 文章数据模型 """
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    # 文章描述信息
    description = db.Column(db.String(256))
    # 封面图片地址
    image_url = db.Column(db.String(256))
    # 关联到用户, 且删除用户时将该字段设置为空
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    author = db.relationship('User')
    chapters = db.relationship('Chapter')

    def __repr__(self):
        return '<Article:{}>'.format(self.name)

    @property
    def url(self):
        """ 返回详情页的 url, 并把当前文章实例对象的 id 作为参数传给路由函数 """
        return url_for('article.detail', article_id=self.id)


class Chapter(Base):
    """ 文章章节数据模型 """
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    # 章节描述信息
    description = db.Column(db.String(256))
    # 章节内容
    content = db.Column(db.String(1024))
    # 关联到文章, 且文章删除时删除相关章节
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'))
    article = db.relationship('Article')
