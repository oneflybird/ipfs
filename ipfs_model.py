# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 操作数据库的扩展包
app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@129.211.27.244/ipfs"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 创建数据库实例对象
db = SQLAlchemy(app)

class hashid(db.Model):
    """创建hashid类 """
    # 设置表名
    __tablename__ = 'users'
    # 添加主键
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    hash = db.Column(db.String(64), unique=True)
    is_public = db.Column(db.Boolean(),default=False)
if __name__ == '__main__':
    # 先删除表
    db.drop_all()
    # 创建表
    db.create_all()
    app.run()