# -*- coding: utf-8 -*-
import click

import os
import sys

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['JSON_AS_ASCII'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'zh'  # 设置默认语言为中文
app.config['SECRET_KEY'] = 'dev'


babel = Babel(app)

app.config["DEFAULT_BABEL_LOCALE"] = "zh"

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'ellatu'
    movies = [
        {'movieid': '1001', 'title': '战狼2', 'releasedate': '2017/07/27', 'country': 'China', 'Type': '科幻', 'year': '2017'},
        {'movieid': '1002', 'title': '战狼', 'releasedate': '2019/07/26', 'country': 'China', 'Type': '动画', 'year': '2019'},
        {'movieid': '1003', 'title': '流浪地球', 'releasedate': '2019/2/5', 'country': 'China', 'Type': '科幻', 'year': '2019'},
        {'movieid': '1004', 'title': '复仇者联盟4', 'releasedate': '2019/4/24', 'country': 'America', 'Type': '科幻','year': '2019'},
        {'movieid': '1005', 'title': '红海行动', 'releasedate': '2018/2/16', 'country': 'China', 'Type': '战争','year': '2018'},
        {'movieid': '1006', 'title': '唐人街探案2', 'releasedate': '2018/2/16', 'country': 'China', 'Type': '喜剧','year': '2018'},
        {'movieid': '1007', 'title': '我不是药神', 'releasedate': '2018/7/5', 'country': 'China', 'Type': '喜剧','year': '2018'},
        {'movieid': '1008', 'title': '中国机长', 'releasedate': '2019/9/30', 'country': 'China', 'Type': '剧情','year': '2019'},
        {'movieid': '1009', 'title': '速度与激情8', 'releasedate': '2017/4/14', 'country': 'America', 'Type': '动作','year': '2017'},
        {'movieid': '1010', 'title': '西虹市首富', 'releasedate': '2018/7/27', 'country': 'China', 'Type': '喜剧','year': '2018'},
        {'movieid': '1011', 'title': '复仇者联盟3', 'releasedate': '2018/5/11', 'country': 'America', 'Type': '科幻','year': '2018'},
        {'movieid': '1012', 'title': '捉妖记2', 'releasedate': '2018/2/16', 'country': 'China', 'Type': '喜剧','year': '2018'},
        {'movieid': '1013', 'title': '八佰', 'releasedate': '2020/08/21', 'country': 'China', 'Type': '战争','year': '2020'},
        {'movieid': '1014', 'title': '姜子牙', 'releasedate': '2020/10/01', 'country': 'China', 'Type': '动画','year': '2020'},
        {'movieid': '1015', 'title': '我和我的家乡', 'releasedate': '2020/10/01', 'country': 'China', 'Type': '剧情','year': '2020'},
        {'movieid': '1016', 'title': '你好，李焕英', 'releasedate': '2021/02/12', 'country': 'China', 'Type': '喜剧','year': '2021'},
        {'movieid': '1017', 'title': '长津湖', 'releasedate': '2021/09/30', 'country': 'China', 'Type': '战争','year': '2021'},
        {'movieid': '1018', 'title': '速度与激情9', 'releasedate': '2021/05/21', 'country': 'China', 'Type': '动作','year': '2021'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(movieid=m['movieid'], title=m['title'], releasedate=m['releasedate'], country=m['country'],
                      Type=m['Type'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名

class  Movie(db.Model):  # 表名将会是movie_info（自动生成，小写处理）
    movieid = db.Column(db.String(10), primary_key=True)  # 主键
    title = db.Column(db.String(20))  # 名字
    releasedate = db.Column(db.String(20))  # 时间日期
    country = db.Column(db.String(20))  # 国家
    Type = db.Column(db.String(10))  # 类型
    year = db.Column(db.String(4))  # 年份

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movieid = request.form['movieid']
        title = request.form['title']
        releasedate = request.form['releasedate']
        country = request.form['country']
        Type = request.form['Type']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(movieid =movieid, title=title, releasedate =releasedate, country = country, Type = Type, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    movies = Movie.query.all()  # 读取用户记录
    return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        movieid = request.form['movieid']
        title = request.form['title']
        releasedate = request.form['releasedate']
        country = request.form['country']
        Type = request.form['Type']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))