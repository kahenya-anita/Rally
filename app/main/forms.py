from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField,ValidationError
from wtforms.validators import Required,Email
from ..models import Subscriber
import email_validator


class PostForm(FlaskForm):
    title = StringField('Post title',validators=[Required()])
    text = TextAreaField('Your post', validators=[Required()],render_kw={'class': 'form-control', 'rows': 10})
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Your comment',validators = [Required()])
    submit = SubmitField('Post')

class SubscribeForm(FlaskForm):
    email = StringField('Your Email',validators=[Required(),Email()])
    submit = SubmitField('Subscribe')

    def validate_email(self,data_field):
        if Subscriber.query.filter_by(email =data_field.data).first():
            raise ValidationError("You've already subscribed.")

class UnsubscribeForm(FlaskForm):
    email = StringField('Your Email',validators=[Required(),Email()])
    submit = SubmitField('Unsubscribe')

    def validate_email(self,data_field):
        if Subscriber.query.filter_by(email =data_field.data).first() == None:
            raise ValidationError("You are not subscribed.")

class ContactForm(FlaskForm):
    name = StringField('Your name',validators=[Required()])
    email = StringField('Your Email',validators=[Required(),Email()])
    title = StringField('Title',validators=[Required()])
    message = TextAreaField('Message', validators=[Required()],render_kw={'class': 'form-control', 'rows': 6})    
    submit = SubmitField('Send')

class UpdateProfile(FlaskForm):
    name = StringField('Your name',validators=[Required()])
    bio = TextAreaField('Bio',validators = [Required()])
    submit = SubmitField('Update')