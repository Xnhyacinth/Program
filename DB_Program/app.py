# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta
import random
import sqlalchemy
from faker import Faker
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, UserMixin, logout_user, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, SelectField, \
    EmailField
from wtforms.validators import DataRequired, Length
from xpinyin import Pinyin

app = Flask(__name__)
app.secret_key = "asbelgihaoiueghlieh"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:529990@127.0.0.1:3306/lab'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '你必须登陆后才能访问该页面'
login_manager.login_message_category = "info"
default_password = "123456"
default_lab = "未指定"

p = Pinyin()
fake = Faker('zh_CN')


## 数据库模型
## 角色（权限）
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    # lazy = "dynamic" 只可以用在一对多和多对多关系中，不可以用在一对一和多对一中

    @staticmethod
    def roles_init():
        roles = ('student', 'admin')
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


## 用户
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # id = db.Column(db.String(20), primary_key=True, nullable=True)
    # id = db.Column(db.Integer, db.Sequence('article_aid_seq', start=20001, increment=1), primary_key=True, )
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128), default=generate_password_hash(default_password))
    email = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    devices = db.relationship('DeviceStorage', backref='user', lazy='dynamic')
    warranties = db.relationship('Warranty', backref='user', lazy='dynamic')
    scraps = db.relationship('Scrap', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r, role_id %r>' % (self.username, self.role_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return self.password == password

    def verify_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    # 初次运行程序时生成初始管理员的静态方法
    @staticmethod
    def generate_admin():
        admin = Role.query.filter_by(name='admin').first()
        u = User.query.filter_by(role=admin).first()
        if u is None:
            # print(Role.query.filter_by(name='admin').first().id)
            u = User(id=10001, name='admin', email='zhaowrenee@gmail.com', username='admin',
                     role=Role.query.filter_by(name='admin').first())
            u.set_password('admin')
            db.session.add(u)
        db.session.commit()


## 实验室
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)  # 实验室编号
    name = db.Column(db.String(64), index=True)  # 实验室名
    device_num = db.Column(db.Integer, default=0)  # 实验室设备数

    lab_name = db.relationship('DeviceStatus', backref='lab', uselist=False)

    def __repr__(self):
        return '<id %r, name %r>' % (self.id, self.name)

    @staticmethod
    def generate_default():
        r = Room(id=30001, name=default_lab)
        db.session.add(r)
        db.session.commit()


## 设备入库批次
class DeviceStorage(UserMixin, db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)  # 入库记录编号

    name = db.Column(db.String(64))  # 设备名 (规格)
    category = db.Column(db.String(64))  # 类别
    type = db.Column(db.String(128),
                     default="X-" + category + "-" + name)  # 设备型号 设备名和类别的组合
    batch = db.Column(db.String(64))  # 入库批次
    price = db.Column(db.Float)  # 单价
    amount = db.Column(db.Integer)  # 数量
    time = db.Column(db.DATE, default=datetime.now())  # 购置日期
    manufacturer = db.Column(db.String(64), default="华电")  # 生产厂家 (品牌)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 购买人

    device_status = db.relationship('DeviceStatus', backref='device')

    # device_status = db.relationship('DeviceStatus', backref='device', uselist=False)
    # device_warranties = db.relationship('Warranty', backref='device', uselist=False)
    # device_scraps = db.relationship('Scrap', backref='device', uselist=False)

    def __repr__(self):
        return '<Device %r>' % self.name

    def set_batch(self):
        dev1_query = DeviceStorage.query.filter_by(type=self.type)
        if dev1_query.first() is None:
            self.batch = datetime.now().strftime("%Y") + "-" + p.get_initials(self.category, "") + "-" \
                         + p.get_initials(self.name, "") + "#%03d" % 1
        else:
            # print(DeviceStorage.query.filter_by(type=self.type).order_by(db.desc(DeviceStorage.id)).limit(1).one().id)
            dev1 = dev1_query.order_by(db.desc(DeviceStorage.id)).limit(1).one()
            type_split_list = dev1.batch.split("#")
            self.batch = type_split_list[0] + "#%03d" % (int(type_split_list[-1]) + 1)

    def set_type(self):  # 设置设备型号
        # self.type = "X-" + p.get_initials(self.category, "") + "-" + p.get_pinyin(self.name, "")
        self.type = "X-" + p.get_pinyin(self.name, "")


## 状态类型
class DeviceStatusType(db.Model):
    __tablename__ = 'status_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)  # 设备状态名称

    status_name = db.relationship('DeviceStatus', backref='status')

    @staticmethod
    def device_status_types_init():
        status_types = ("全部", "正常", "损坏", "维修中")
        for type_name in status_types:
            st = DeviceStatusType.query.filter_by(name=type_name).first()
            # print(type_name)
            if st is None:
                st = DeviceStatusType(name=type_name)
                db.session.add(st)

        db.session.commit()


## 设备状态
### 设备放入具体实验室后 具体设备的各种状态信息
class DeviceStatus(db.Model):
    __tablename__ = 'statuses'
    # id = db.Column(db.Integer, db.Sequence('article_aid_seq', start=20001, increment=1), primary_key=True, autoincrement=True)
    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 设备编号
    dev_id = db.Column(db.String(64))  # 设备编号
    storage_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    lab_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))  # 所在实验室编号
    status_id = db.Column(db.Integer, db.ForeignKey('status_types.id'))  # 设备状态编号
    time = db.Column(db.DateTime, default=datetime.now(), primary_key=False)  # 记录时间

    device_warranties = db.relationship('Warranty', backref='device')
    device_scraps = db.relationship('Scrap', backref='device')

    def set_dev_id(self):
        dev1_query = DeviceStatus.query.filter_by(storage_id=self.storage_id)
        dev = DeviceStorage.query.filter_by(id=self.storage_id).first()
        if dev1_query.first() is None:
            self.dev_id = dev.batch + "-%03d" % 1
        else:
            # print(DeviceStorage.query.filter_by(type=self.type).order_by(db.desc(DeviceStorage.id)).limit(1).one().id)
            dev1 = dev1_query.order_by(db.desc(DeviceStatus.device_id)).limit(1).one()
            type_split_list = dev1.dev_id.split("-")
            self.dev_id = dev.batch + "-%03d" % (int(type_split_list[-1]) + 1)
        # self.dev_id = dev.batch + "-%03d" % 1


## 保修
class Warranty(db.Model):
    __tablename__ = 'warranties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 保修记录编号
    device_id = db.Column(db.Integer, db.ForeignKey('statuses.device_id'))  # 设备编号
    manufacturer = db.Column(db.String(64))  # 修理厂家
    price = db.Column(db.Float)  # 修理费
    time = db.Column(db.DateTime, default=datetime.now(), primary_key=False)  # 保修时间
    responsible_person_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 负责人
    warranty_status = db.Column(db.String(64))  # 保修状态


## 报废
class Scrap(db.Model):
    __tablename__ = 'scraps'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 报废记录编号
    device_id = db.Column(db.Integer, db.ForeignKey('statuses.device_id'), unique=True)  # 设备编号
    time = db.Column(db.DateTime, default=datetime.now(), primary_key=True)  # 保修时间
    responsible_person_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 负责人


### 触发器
@db.event.listens_for(DeviceStatus.lab_id, 'set')
def trigger_lab_insert(target, value, oldvalue, initiator):
    # print("trigger DeviceStatus.lab_id:", value)
    lab = Room.query.filter_by(id=value).first()
    if lab:
        lab.device_num += 1
        db.session.commit()


# @db.event.listens_for(DeviceStorage.name, 'set')
# def trigger_update_room_devicenum(target, value, oldvalue, initiator):
#     print("***********")
#     print(target.type)
#     print(value)
#     print(oldvalue)
#     print(initiator)
#     print("***********")

# def trigger_put_into_lab(target, value, oldvalue, initiator):
#     print(target)
#     print(value)
#
# db.event.listen(DeviceStorage.id, "set", trigger_put_into_lab)


###############################################################################################################
### 数据库初始化

def dbinit():
    print("*************initializing*************")
    db.drop_all()
    db.create_all()

    Role.roles_init()
    User.generate_admin()
    DeviceStatusType.device_status_types_init()
    # Room.generate_default()

    u1 = User(id=123, username="zhangsan", role=Role.query.filter_by(name="student").first())
    u1.set_password("666666")
    db.session.add(u1)

    members = ["李洋", "廖语轩", "廖桓萱", "郑雨轩", "邵锐祥"]

    for name in members:
        name_p = p.get_pinyin(name, "")
        u1 = User(id=int(fake.ean8()), name=name, username=name_p, email=name_p + "@163.com",
                  role=Role.query.filter_by(name='admin').first())
        u1.set_password("666666")
        db.session.add(u1)

    u1 = User(id="4865", username="liyang1", role_id=1)
    u1.set_password("666666")
    db.session.add(u1)

    db.session.commit()

    id0 = 100001
    num = 10
    for k in range(id0, id0 + num):
        profile = fake.simple_profile()
        user = User(name=profile['name'], username=profile['username'], email=profile['mail'],
                    role=Role.query.filter_by(name='admin').first())
        db.session.add(user)

    id0 = 30001
    num = 20
    for k in range(id0, id0 + num):
        profile = fake.simple_profile()
        user = User(name=profile['name'], username=profile['username'], email=profile['mail'],
                    role=Role.query.filter_by(name='student').first())
        db.session.add(user)

    num = 15
    for i in range(1, num):
        room = Room(name="Lab%03d" % i)
        db.session.add(room)
    db.session.commit()

    category_list = ['DSP实验箱', '功率变换器', '双踪示波器', '联想电脑', '曙光天阔服务器', u'ZigBee开发套件']
    # fake.pystr(min_chars=3, max_chars=5)

    all_users = User.query.all()
    all_labs = Room.query.all()
    status_normal = DeviceStatusType.query.filter_by(name="正常").first()
    for ct in category_list:
        dev = DeviceStorage(
            name=ct + fake.pystr(min_chars=3, max_chars=5),
            category=ct,
            price=random.uniform(800, 3000),
            amount=random.randint(3, 13),
            manufacturer=fake.company(),
            buyer_id=all_users[random.randint(2, len(all_users) - 2)].id
        )
        dev.set_type()
        dev.set_batch()
        db.session.add(dev)
        db.session.commit()

        for i in range(dev.amount):
            st = DeviceStatus(
                storage_id=dev.id,
                lab_id=all_labs[random.randint(2, len(all_labs) - 1)].id,
                status_id=status_normal.id,
            )
            st.set_dev_id()
            db.session.add(st)

    db.session.commit()

    # db.session.commit()
    print("***************done***************")


# dbinit()


# dbinit()


###############################################################################################################


### forms
class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 32)])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(1, 32)])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class SearchForm(FlaskForm):
    name = StringField(u'设备名', validators=[DataRequired()])
    submit = SubmitField(u'搜索')


class SearchFormWarranty(FlaskForm):
    category = StringField(u'设备类别')
    manufacturer = StringField(u'保修厂家')
    name = StringField(u'责任人')
    submit = SubmitField(u'搜索')


class AddDeviceForm(FlaskForm):
    name = StringField(u'设备名', validators=[DataRequired(), Length(1, 32)])
    category = StringField(u'类别')
    lab = StringField(u'实验室名', validators=[Length(0, 32)])
    price = FloatField(u'单价')
    amount = IntegerField(u'购买数量')
    manufacturer = StringField(u'生产厂家')
    username = StringField(u'购置人', validators=[DataRequired()])
    submit = SubmitField(u'添加')


class AddUserForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 32)])
    name = StringField(u'真实姓名', validators=[Length(0, 32)])
    email = EmailField(u'邮箱')
    role = SelectField(u'身份', validators=[DataRequired('请选择')], choices=[(r.id, r.name) for r in Role.query.all()])
    submit = SubmitField(u'提交')


class ScrapForm(FlaskForm):
    name = StringField(u'责任人', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField(u'确认')


class ModifyUserInfor(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 32)])
    email = EmailField(u'邮箱')
    submit = SubmitField(u'提交')


class ModifyUserPassWord(FlaskForm):
    old_password = PasswordField(u'请输入原密码', validators=[DataRequired(), Length(6, 32)])
    new_password1 = PasswordField(u'请输入新密码', validators=[DataRequired(), Length(6, 32)])
    new_password2 = PasswordField(u'再次输入新密码', validators=[DataRequired(), Length(6, 32)])
    submit = SubmitField(u'提交')


class AddLabInfoForm(FlaskForm):
    # id = StringField(u'实验室编号', validators=[Length(2, 12)])
    id = StringField(u'实验室编号')
    name = StringField(u'实验室名', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField(u'提交')


class ModifyLabForm(FlaskForm):
    name = StringField(u'实验室名', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField(u'确认')


### views
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        print(username)
        print(password)

        user: User = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password_hash(password):
            login_user(user, login_form.remember_me.data)

            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=20)  # 持续20分钟未操作则注销

            return redirect(url_for("index"))
        else:
            flash(u'用户名或密码错误！')

    return render_template("login.html", form=login_form)


## 主页
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # print(current_user.name)
    rooms = Room.query.all()
    chart_data = {}
    chart_data["lab_name"] = []
    chart_data["dev_num"] = []
    chart_data["device_name"] = []
    chart_data["warranty_device_num"] = []
    chart_data["scrap_device_num"] = []

    ## 设备实验室数目分配表
    for room in rooms:
        if room.name != "未指定":
            chart_data["lab_name"].append(room.name)
            chart_data["dev_num"].append(room.device_num)

    ##  保修 报废设备类别树目表
    devices = DeviceStorage.query.all()
    for dev in devices:
        if dev.name not in chart_data["device_name"]:
            chart_data["device_name"].append(dev.name)
            chart_data["warranty_device_num"].append(0)
            chart_data["scrap_device_num"].append(0)

    warranties = Warranty.query.all()
    for s in warranties:
        name = s.device.device.name
        i = chart_data["device_name"].index(name)
        chart_data["warranty_device_num"][i] += 1

    scraps = Scrap.query.all()
    for s in scraps:
        name = s.device.device.name
        i = chart_data["device_name"].index(name)
        chart_data["scrap_device_num"][i] += 1
    # print(chart_data["scrap_device_name"])
    # print(chart_data["scrap_device_num"])

    ## 设备运行情况状态表
    st_types = DeviceStatusType.query.all()
    statuses = DeviceStatus.query.all()
    chart_data["pie_data"] = []
    datas = {}
    for type in st_types:
        if type.name != "全部":
            datas[type.name] = 0

    for st in statuses:
        datas[st.status.name] += 1

    for k, v in datas.items():
        chart_data["pie_data"].append({
            "name": k,
            "value": v,
        })

    # print(chart_data["pie_data"])

    return render_template('index.html', rooms=rooms, chart_data=chart_data)


## 实验室信息
@app.route('/lab_info', methods=['GET', 'POST'])
@login_required
def lab_info():
    labs = Room.query.all()

    add_info_form = AddLabInfoForm()

    if add_info_form.validate_on_submit():

        id = add_info_form.id.data
        name = add_info_form.name.data
        if Room.query.filter_by(name=name).first():
            flash("该实验室名已存在！")
            return redirect(url_for('lab_info'))

        if len(id) > 1:
            id = int(id)
            new_room = Room(id=id, name=name)
            db.session.add(new_room)
            db.session.commit()
        else:
            new_room = Room(name=name)
            db.session.add(new_room)
            db.session.commit()

        flash("新实验室添加成功！")
        return redirect(url_for('lab_info'))

    return render_template("labs_info.html", labs=labs, labs_num=len(labs), add_info_form=add_info_form)


# 修改实验室信息
@app.route('/lab_info/modify/<int:lab_id>/<new_name>', methods=['GET', 'POST'])
@login_required
def lab_info_modify(lab_id, new_name):
    print(lab_id, new_name)
    room = Room.query.filter_by(id=lab_id).first()
    room.name = new_name
    db.session.commit()
    flash("修改成功！")
    return redirect(url_for("lab_info"))


# 删除实验室信息
@app.route('/lab_info/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lab_info_delete(id):
    lab = Room.query.filter_by(id=id).first()
    if lab.device_num != 0:
        flash("该实验室中还有设备，不可以删除记录！")
        return redirect(url_for("lab_info"))

    db.session.delete(lab)
    db.session.commit()
    flash("该实验室记录删除成功！")

    return redirect(url_for("lab_info"))


## 设备入库
@app.route('/device_storage', methods=['GET', 'POST'])
@login_required
def device_storage():
    form = SearchForm()

    admin = Role.query.filter_by(name='admin').first()

    if form.validate_on_submit():
        devices = DeviceStorage.query.filter(DeviceStorage.name.like('%{}%'.format(form.name.data))).all()
    else:
        devices = DeviceStorage.query.order_by(DeviceStorage.id.asc(), DeviceStorage.name.desc()).all()

    return render_template('device_storage.html', form=form, devices=devices, records_num=len(devices), admin=admin)


# 增加新设备
@app.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    form = AddDeviceForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash(u'购置人填写错误，该用户不存在！')
            return redirect(url_for('add_device'))

        if len(form.lab.data) > 1:  # 输入了实验室名
            room = Room.query.filter_by(name=str(form.lab.data)).first()
            if not room:
                flash(u'实验室不存在！')
                return redirect(url_for('add_device'))
            try:
                device = DeviceStorage(
                    name=form.name.data,
                    category=form.category.data,
                    price=form.price.data,
                    amount=form.amount.data,
                    manufacturer=form.manufacturer.data,
                    buyer_id=User.query.filter_by(username=form.username.data).first().id
                )
                device.set_type()
                device.set_batch()
                db.session.add(device)
                db.session.commit()

                status_normal = DeviceStatusType.query.filter_by(name="正常").first()
                for i in range(device.amount):
                    dev_st = DeviceStatus(
                        storage_id=device.id,  # storage_id 入库记录编号
                        lab_id=room.id,
                        status_id=status_normal.id
                    )
                    dev_st.set_dev_id()
                    db.session.add(dev_st)

                room.device_num += device.amount
                db.session.commit()

            except Exception as e:
                print(e)
                flash("添加失败1: " + str(e))
                return redirect(url_for('add_device'))

            flash(u'成功添加设备')
            return redirect(url_for('device_storage'))

        else:  # 没输入实验室名 还未归入实验室
            try:
                device = DeviceStorage(
                    name=form.name.data,
                    category=form.category.data,
                    price=form.price.data,
                    amount=form.amount.data,
                    manufacturer=form.manufacturer.data,
                    buyer_id=User.query.filter_by(username=form.username.data).first().id
                )
                device.set_type()
                device.set_batch()
                db.session.add(device)
                db.session.commit()

                status_normal = DeviceStatusType.query.filter_by(name="正常").first()
                for i in range(device.amount):
                    dev_st = DeviceStatus(
                        storage_id=device.id,  # storage_id 入库记录编号
                        status_id=status_normal.id
                    )
                    db.session.add(dev_st)

                db.session.commit()

            except Exception as e:
                print(e)
                flash(u'添加失败2' + str(e))
                return redirect(url_for('add_device'))

            flash(u'成功添加设备')
            return redirect(url_for('device_storage'))

    return render_template('add_device.html', form=form)


# 删除设备
@app.route('/remove-device/<int:id>', methods=['GET', 'POST'])
@login_required
def remove_device(id):
    device = Warranty.query.get_or_404(id)
    device.warranty_status = "Done"
    # db.session.delete(device)
    # dev = DeviceStatus.query.get_or_404(dev_id)
    device = DeviceStatus.query.get_or_404(device.device_id)
    device.status_id = 2
    db.session.commit()
    flash(u'成功回收此设备')

    return redirect(url_for('warranty'))


# # 保修设备
# @app.route('/warranty_device/<int:id><username>', methods=['GET', 'POST'])
# @login_required
# def warranty_device(id, username):
#     device = DeviceStatus.query.get_or_404(id)
#     num = len(Warranty.query.all())
#
#     dev = Warranty(
#         id=num + 1,
#         device_id=device.device_id,
#         user=User.query.filter_by(username=username).first(),
#         warranty_status="Doing"
#     )
#     device.status_id = 4
#     db.session.add(dev)
#     db.session.commit()
#
#     flash(u'成功保修此设备')
#     return redirect(url_for('status', type_id=1))


### 设备状态页面的三个按钮

# 修改所在实验室
@app.route('/status/modify/<int:dev_id>/<int:new_lab_id>', methods=['GET', 'POST'])
@login_required
def modify_lab(dev_id, new_lab_id):
    device = DeviceStatus.query.filter_by(device_id=dev_id).first()
    device.lab.device_num -= 1
    if new_lab_id == 0:
        device.lab_id = None
        flash("设备已从实验室移出，实验室信息置为空")
        db.session.commit()
        return redirect(url_for('status', type_id=1))

    device.lab_id = new_lab_id
    db.session.commit()
    flash("设备所在实验室修改成功！")

    return redirect(url_for('status', type_id=1))


# 保修设备
@app.route('/warranty_device/<int:dev_id>/<price>/<manufacturer>/<username>', methods=['GET', 'POST'])
@login_required
def warranty_device(dev_id, price, manufacturer, username):
    try:
        price = float(price)
    except ValueError:
        flash("请输入正确的价格！")
        return redirect(url_for('status', type_id=1))
    # print(dev_id, price, manufacturer)
    device = DeviceStatus.query.get_or_404(dev_id)
    # num = len(Warranty.query.all())
    scrap_exist = Scrap.query.filter_by(device_id=device.device_id).first()
    if scrap_exist is not None:
        flash(u'保修失败，此设备已报废')
        return redirect(url_for('status', type_id=1))

    user = User.query.filter_by(name=username).first()
    if user is None:
        flash("该用户不存在！")
        return redirect(url_for('status', type_id=1))
    war = Warranty.query.filter_by(device_id=device.device_id).first()
    if war is not None and war.warranty_status == "Doing":
        flash("该设备正在保修！")
        return redirect(url_for('status', type_id=1))
    dev = Warranty(
        # id=num + 1,
        device_id=device.device_id,
        user=user,
        price=price,
        manufacturer=manufacturer,
        warranty_status="Doing"
    )
    device.status_id = 4
    db.session.add(dev)
    db.session.commit()
    flash("成功保修此设备！")
    return redirect(url_for("warranty"))


# 回收设备
@app.route('/revoke_device/<int:id>', methods=['GET', 'POST'])
@login_required
def revoke_device(id):
    device = Warranty.query.get_or_404(id)
    # db.session.delete(device)
    # dev = DeviceStatus.query.get_or_404(dev_id)
    device = DeviceStatus.query.get_or_404(device.device_id)
    device.status_id = 2
    dev = Warranty.query.filter_by(device_id=device.device_id).first()
    dev.warranty_status = "Done"
    db.session.commit()
    flash(u'成功回收此设备')

    return redirect(url_for('warranty'))


# 报废设备
@app.route('/scrap_device/<int:id><username>', methods=['GET', 'POST'])
@login_required
def scrap_device(id, username):
    device = DeviceStatus.query.get_or_404(id)
    num = len(Scrap.query.all())
    # form = ScrapForm()
    # if form.validate_on_submit():
    #     dev = Scrap(
    #         id=num + 1,
    #         device_id=device.device_id,
    #         user=User.query.filter_by(username=form.name.data).first()
    #     )
    #     device.status_id = 3
    #     db.session.add(dev)
    #     db.session.commit()
    #
    #     flash(u'成功报废此设备')
    #     return redirect(url_for('status', type_id=1))
    # return render_template("statuses.html", type_id=1, form=form)
    scrap_exist = Scrap.query.filter_by(device_id=device.device_id).first()
    if scrap_exist is not None:
        flash(u'报废失败，此设备已报废')
        return redirect(url_for('status', type_id=1))
    # scraps_list = Scrap.query.all()
    dev = Scrap(
        id=num + 1,
        device_id=device.device_id,
        user=User.query.filter_by(username=username).first()
    )
    # if dev.device_id in scraps_list:
    #     flash(u'报废失败，此设备已报废')
    #     return redirect(url_for('status', type_id=1))
    if device.status_id == 4:
        war = Warranty.query.filter_by(device_id=device.device_id).first()
        war.warranty_status = "Scrap"
    device.status_id = 3
    room = Room.query.filter_by(id=device.lab_id).first()
    room.device_num -= 1
    db.session.add(dev)
    db.session.commit()

    flash(u'成功报废此设备')
    return redirect(url_for('scrap'))


## 设备管理 具体设备 放在实验室
@app.route('/device_management/', methods=['GET', 'POST'])
@login_required
def device_management():
    return render_template('device_management.html')


# ## 运行状态
# @app.route('/status/<int:type_id>')
# @login_required
# def status(type_id):
#     status_types = DeviceStatusType.query.all()
#     form = SearchForm()
#     if form.name is not None:
#         if form.validate_on_submit():
#             statuses = DeviceStatus.query.filter(DeviceStorage.name.like('%{}%'.format(form.name.data))).all()
#         else:
#             statuses = DeviceStatus.query.order_by(DeviceStorage.id.asc(), DeviceStorage.name.desc()).all()
#
#     if type_id == DeviceStatusType.query.filter_by(name="全部").first().id:
#         statuses = DeviceStatus.query.all()
#     else:
#         statuses = DeviceStatus.query.filter_by(status_id=type_id).all()
#     # print(statuses)
#     # print(type_id)
#
#     return render_template('statuses.html', status_types=status_types, type_id=type_id, statuses=statuses,form=form)## 运行状态
@app.route('/status/<int:type_id>', methods=['GET', 'POST'])
@login_required
def status(type_id):
    form = SearchForm()
    status_types = DeviceStatusType.query.all()
    # if type_id == DeviceStatusType.query.filter_by(name="全部").first().id:
    #     statuses = DeviceStatus.query.all()
    # else:
    #     statuses = DeviceStatus.query.filter_by(status_id=type_id).all()

    if form.validate_on_submit():
        if type_id == DeviceStatusType.query.filter_by(name="全部").first().id:
            # print(DeviceStorage.name.like('%{}%'.format(form.name.data)))
            # statuses = DeviceStatus.query.filter(DeviceStorage.name.like('%{}%'.format(form.name.data))).all()
            statuses = DeviceStatus.query.join(DeviceStatus, DeviceStorage.device_status).filter(
                DeviceStorage.name.like('%{}%'.format(form.name.data))).all()
        else:
            statuses = DeviceStatus.query.filter_by(status_id=type_id).join(DeviceStatus,
                                                                            DeviceStorage.device_status).filter(
                DeviceStorage.name.like('%{}%'.format(form.name.data))).all()
    else:
        if type_id == DeviceStatusType.query.filter_by(name="全部").first().id:
            statuses = DeviceStatus.query.all()
        else:
            statuses = DeviceStatus.query.filter_by(status_id=type_id).all()
    # if form.validate_on_submit():
    #     devices = DeviceStorage.query.filter(DeviceStorage.name.like('%{}%'.format(form.name.data))).all()
    # else:
    #     devices = DeviceStorage.query.order_by(DeviceStorage.id.asc(), DeviceStorage.name.desc()).all()

    status_num = len(statuses)
    labs = Room.query.all()
    return render_template('statuses.html', status_types=status_types, type_id=type_id, statuses=statuses, form=form,
                           status_num=status_num, labs=labs)


@app.route('/status/add_status_record', methods=['GET', 'POST'])
@login_required
def add_status_record():
    return "<script>alert(\"弹窗表单\");</script>"


## 保修管理
@app.route('/warranty', methods=['GET', 'POST'])
@login_required
def warranty():
    # warranties = Warranty.query.all()
    form = SearchFormWarranty()
    # print(warranties)

    if form.validate_on_submit():
        warranties1 = Warranty.query.join(DeviceStatus, DeviceStorage.device_status) \
            .join(Warranty, DeviceStatus.device_warranties) \
            .filter(DeviceStorage.category.like('%{}%'.format(form.category.data))) \
            .filter(Warranty.manufacturer.like('%{}%'.format(form.manufacturer.data))).all()

        warranties2 = Warranty.query.join(Warranty, User.warranties) \
            .filter(User.name.like('%{}%'.format(form.name.data))).all()
        warranties = list(set(warranties1).intersection(set(warranties2)))
    else:
        warranties = Warranty.query.all()
    warranty_num = len(warranties)
    return render_template('warranties.html', warranties=warranties, warranty_num=warranty_num, form=form)


## 报废管理
@app.route('/scrap', methods=['GET', 'POST'])
@login_required
def scrap():
    form = SearchFormWarranty()
    if form.validate_on_submit():
        scraps1 = Scrap.query.join(DeviceStatus, DeviceStorage.device_status) \
            .join(Scrap, DeviceStatus.device_scraps) \
            .filter(DeviceStorage.category.like('%{}%'.format(form.category.data))).all()
        # .filter(Scrap.manufacturer.like('%{}%'.format(form.manufacturer.data))).all()

        scraps2 = Scrap.query.join(Scrap, User.scraps) \
            .filter(User.name.like('%{}%'.format(form.name.data))).all()
        scraps = list(set(scraps1).intersection(set(scraps2)))
    else:
        scraps = Scrap.query.all()

    scrap_num = len(scraps)
    # print(scraps)
    return render_template('scraps.html', scraps=scraps, scrap_num=scrap_num, form=form)


## 用户管理
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    users_num = len(users)
    form = AddUserForm()

    if form.validate_on_submit():
        # print(form.username.data)
        # print(form.role.data)
        if User.query.filter_by(username=form.username.data).first():
            flash(u'用户名已存在！')
        else:
            new_user = User(username=form.username.data, name=form.name.data, email=form.email.data,
                            role_id=form.role.data)
            db.session.add(new_user)
            db.session.commit()
            flash(u'新用户添加成功！密码为默认密码' + default_password)
            return redirect(url_for('users'))

    return render_template("users_management.html", users=users, users_num=users_num, form=form)


# 删除用户
@app.route('/users/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    try:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        flash("用户删除成功")
    except sqlalchemy.exc.IntegrityError:
        flash("该用户是设备责任人，不可删除！")

    return redirect(url_for('users'))


# 重置密码
@app.route('/users/reset_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def reset_password(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.set_password(default_password)
    db.session.commit()
    flash("已将该用户的密码重置为默认密码" + default_password + "！")

    return redirect(url_for('users'))


## 个人中心
@app.route('/login_user_center', methods=['GET', 'POST'])
@login_required
def login_user_center():
    modify_info_form = ModifyUserInfor()
    if modify_info_form.validate_on_submit():
        if User.query.filter_by(username=modify_info_form.username.data) is not None:
            flash("用户名已存在")
        current_user.username = modify_info_form.username.data
        current_user.email = modify_info_form.email.data
        db.session.commit()
        flash()

    modify_password_form = ModifyUserPassWord()
    if modify_password_form.validate_on_submit():
        if not current_user.verify_password_hash(modify_password_form.old_password.data):
            flash("原密码输入错误！如忘记密码，请联系管理员重置")
            return redirect(url_for('login_user_center'))

        if modify_password_form.new_password1.data != modify_password_form.new_password2.data:
            flash("新密码两次输入不一致！")
            return redirect(url_for('login_user_center'))

        current_user.set_password(modify_password_form.new_password1.data)
        db.session.commit()
        flash("修改密码成功！请重新登录")
        return redirect(url_for('login'))

    return render_template("user_center.html", modify_info_form=modify_info_form,
                           modify_password_form=modify_password_form)


# # 修改个人信息
# @app.route('/login_user_center/modify_user_info', methods=['GET', 'POST'])
# @login_required
# def modify_user_info():
#     pass
#
# # 修改个人密码
# @app.route('/login_user_center/modify_user_password', methods=['GET', 'POST'])
# @login_required
# def modify_user_password():
#     form = ModifyUserPassWord()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'成功注销！')
    return redirect(url_for('login'))


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


## 测试接口
@app.route('/hello')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
