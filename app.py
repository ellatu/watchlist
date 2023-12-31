# -*- coding: utf-8 -*-
import click

import os
import sys

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_babel import Babel,_
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'
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
        {'movieid': '1001', 'title': 'Wolf Warrior2', 'releasedate': '2017/07/27', 'country': 'China', 'Type': 'science fiction', 'year': '2017'},
        {'movieid': '1002', 'title': 'nezha', 'releasedate': '2019/07/26', 'country': 'China', 'Type': 'animation', 'year': '2019'},
        {'movieid': '1003', 'title': 'The Wandering Earth', 'releasedate': '2019/2/5', 'country': 'China', 'Type': 'science fiction', 'year': '2019'},
        {'movieid': '1004', 'title': 'The Advanger4', 'releasedate': '2019/4/24', 'country': 'America', 'Type': 'science fiction','year': '2019'},
        {'movieid': '1005', 'title': 'Operation Red Sea', 'releasedate': '2018/2/16', 'country': 'China', 'Type': 'war','year': '2018'},
        {'movieid': '1006', 'title': 'Detective Chinatown2', 'releasedate': '2018/2/16', 'country': 'China', 'Type': 'comedy','year': '2018'},
        {'movieid': '1007', 'title': 'god of medicine', 'releasedate': '2018/7/5', 'country': 'China', 'Type': 'comedy','year': '2018'},
        {'movieid': '1008', 'title': 'Chinese captain', 'releasedate': '2019/9/30', 'country': 'China', 'Type': 'story','year': '2019'},
        {'movieid': '1009', 'title': 'Fast and Furious8', 'releasedate': '2017/4/14', 'country': 'America', 'Type': 'action','year': '2017'},
        {'movieid': '1010', 'title': 'Xihongshi', 'releasedate': '2018/7/27', 'country': 'China', 'Type': 'comedy','year': '2018'},
        {'movieid': '1011', 'title': 'The advanger3', 'releasedate': '2018/5/11', 'country': 'America', 'Type': 'science fiction','year': '2018'},
        {'movieid': '1012', 'title': 'Monster Hunt2', 'releasedate': '2018/2/16', 'country': 'China', 'Type': 'comedy','year': '2018'},
        {'movieid': '1013', 'title': 'Babai', 'releasedate': '2020/08/21', 'country': 'China', 'Type': 'war','year': '2020'},
        {'movieid': '1014', 'title': 'Jiangziya', 'releasedate': '2020/10/01', 'country': 'China', 'Type': 'animation','year': '2020'},
        {'movieid': '1015', 'title': 'me and hometown', 'releasedate': '2020/10/01', 'country': 'China', 'Type': 'story','year': '2020'},
        {'movieid': '1016', 'title': 'Hello,Li', 'releasedate': '2021/02/12', 'country': 'China', 'Type': 'comedy','year': '2021'},
        {'movieid': '1017', 'title': 'Changjin lake', 'releasedate': '2021/09/30', 'country': 'China', 'Type': 'war','year': '2021'},
        {'movieid': '1018', 'title': 'Fast and Furiou9', 'releasedate': '2021/05/21', 'country': 'China', 'Type': 'action','year': '2021'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(movieid=m['movieid'], title=m['title'], releasedate=m['releasedate'], country=m['country'],
                      Type=m['Type'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

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

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
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
@login_required
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
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))