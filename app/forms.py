# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ tôi')
    submit = SubmitField('Đăng nhập')

class RegistrationForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    password2 = PasswordField(
        'Lặp lại mật khẩu', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Mời bạn chọn tên đăng nhập khác!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Mời bạn chọn địa chỉ email khác!')

class EditProfileForm(FlaskForm):
    username = StringField('Tên tài khoản', validators=[DataRequired()])
    about_me = TextAreaField('Về tôi', validators=[Length(min=0, max=140)])
    submit = SubmitField('Đăng')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Mời bạn hãy chọn tên tài khoản khác.')

class PostForm(FlaskForm):
    post = TextAreaField('Đăng gì đó nào!', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Đăng bài')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Yêu cầu email hướng dẫn cài đặt lại mật khẩu')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Mật khẩu mới', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cài đặt lại mật khẩu')