# 存放表单相关代码
# i love nuonuo
# author:KRzhao

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired, InputRequired
from flask_wtf.file import FileRequired, FileAllowed
from .models import db, User


class RegisterForm(FlaskForm):
    """ 注册表单 """
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_user(self):
        """ 创建新用户的方法 """
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        """ 自定验证器, 验证用户名是否已存在数据表 """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在! ')

    def validate_email(self, field):
        """ 自定验证器, 验证邮箱地址是否已存在数据表 """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')


class LoginForm(FlaskForm):
    """ 登录表单 """
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        """ 自定验证器, 验证邮箱是否注册 """
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        """ 自定验证器, 验证密码是否正确 """
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误, 请重新输入')


class UploadForm(FlaskForm):
    """ 文件上传表单 """
    file = FileField('文件上传', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xlsx格式. ')])
    submit = SubmitField('提交')


class MergeForm(FlaskForm):
    """ excel 表格合并工具表单 """
    left_file = FileField('表格1', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    right_file = FileField('表格2', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    left_on = StringField('表格1依据字段', validators=[DataRequired()])
    right_on = StringField('表格2依据字段', validators=[DataRequired()])
    way = StringField('合并方式: left, right, outer, inner', validators=[DataRequired()])
    submit = SubmitField('执行')

    def validate_way(self, field):
        """ 自定义验证器, 验证合并方式是否正确 """
        if field.data not in ['left', 'right', 'outer', 'inner']:
            raise ValidationError('合并方式选择错误')


class ReceivableForm(FlaskForm):
    """ 管理月报应收生成工具表单 """
    bnys_file = FileField('本年应收表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    bnyye_file = FileField('本年月余额表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    snyye_file = FileField('上年月余额表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    khzl_file = FileField('客户资料表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    sybb_file = FileField('上月报表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], message='只支持xls/xlsx格式. ')])
    submit = SubmitField('执行')
