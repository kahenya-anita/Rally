from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_quote
# from .forms import PostForm,CommentForm,SubscribeForm,UnsubscribeForm,ContactForm,UpdateProfile
# from ..models import Post,Comment,Subscriber,Contact,User
# from ..email import mail_message

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    author = User.query.first() 
    return render_template('index.html',quote=quote, author=author)

@main.route('/user',methods = ['GET','POST'])
def user(): 
    form=PostForm()
    quote=get_quote()        
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        
        
        # Updated post instance
        this_post = Post(title=title, text=text,  post_pic_path='photos/sample-image.jpeg')

        # save post method
        this_post.save_post()

        mail_list=[]
        subscribers=Subscriber.query.order_by(Subscriber.id.desc())
        for sub in subscribers:
            mail_list.append(sub.email)
        
        mail_message("New posts on Blog post","email/new_post",mail_list,this_post=this_post)

        return redirect(url_for('.index'))
      
    title = 'New Post'

    return render_template('user.html', title=title, post_form=form, quote=quote)

