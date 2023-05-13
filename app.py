from flask import Flask, render_template, redirect, url_for, request, _app_ctx_stack
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from ext import db, mail
import sql
from datetime import timedelta
from forms import RegisterForm, LoginForm
from Mysql_run import UserModel

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)  # 随机数密钥
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=50)  # 生成过期日期

app.config.from_object(sql)

app.config.from_object(sql)

db.init_app(app)
mail.init_app(app)

migration = Migrate(app, db)




@app.route('/reader_login', methods=['POST', 'GET'])
def reader_login():
    # if get_flashed_messages() != "":   # 想要使用 get_flashed_messages() 函数，需要先从 flask 模块中导入该函数。
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱未注册")
                return redirect('/login')
            # 下面是验证密码是否正确,check_password_hash()函数的第一个参数是数据库中的密码，第二个参数是用户输入的密码
            if check_password_hash(user.password, password):
                # print("登录成功")
                # return jsonify({'code': 200, 'message': '登录成功'})
                username = user.username
                return redirect('/resources')
            else:
                print("密码错误")
                return redirect('/login')
        else:
            print(form.errors)
            return redirect('/login')
        # username = request.form.get("username", None)
        # password = request.form.get('password', None) 写在上面了

        session['username'] = user.username  # 将用户名存入session中
        # 出现一个闪现信息;
        flash("用户%s密码错误， 请重新登录....." % username)  # flash将内容存在session中，通过messages = get_flashed_messages()获取
        return render_template('reader_login.html')
    return render_template('reader_login.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/manager_login')
def manager_login():
    return render_template('manager_login.html')


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.commit()
    app.run(debug=True)
