from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)
name = 'ellatu'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class  movieinfo(db.Model):  # 表名将会是movie_info（自动生成，小写处理）
    movie_id = db.Column(db.String(10), primary_key=True)  # 主键
    movie_name = db.Column(db.String(20))  # 名字
    release_date = db.Column(db.DateTime)  # 时间日期
    country = db.Column(db.String(20))  # 国家
    type = db.Column(db.String(10))  # 类型
    year = db.Column(db.INT)  # 年份

class movebox(db.Model):  # 表名将会是 movie_box
    movie_id = db.Column(db.String(10), primary_key=True)  # 主键
    box = db.Column(db.Float(60))  # 电影box

class  actorinfo(db.Model):  # 表名将会是actor_info
    actor_id = db.Column(db.String(10), primary_key=True)  # 主键
    actor_name = db.Column(db.String(20))  # 名字
    gender = db.Column(db.String(2))  
    country = db.Column(db.String(20))  # 国家

class  movieactorrelation(db.Model):
    id = db.Column(db.String(10), primary_key=True) 
    movie_id = db.Column(db.String(10))
    actor_id = db.Column(db.String(10))
    relation_type = db.Column(db.String(20))

import click


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

