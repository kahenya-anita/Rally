from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_quote
from .forms import PostForm,CommentForm,SubscribeForm,UnsubscribeForm,ContactForm,UpdateProfile
from ..models import Post,Comment,Subscriber,Contact,User
from ..email import mail_message

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
        
        mail_message("New posts on Rally","email/new_post",mail_list,this_post=this_post)

        return redirect(url_for('.index'))
      
    title = 'New Post'

    return render_template('user.html', title=title, post_form=form, quote=quote)

@main.route('/post/<post_id>',methods = ['GET','POST'])
def blog_post(post_id):
    quote=get_quote()
    post=Post.query.filter_by(id=post_id).first()
    form = CommentForm()
      
    if form.validate_on_submit():
        new_comment = form.comment.data             

        # Updated comment instance
        this_comment = Comment(comment_text=new_comment,post=post)

        # save comment method
        this_comment.save_comment()
        return redirect(url_for('.blog_post', post_id=post_id))
    
    
    comments=Comment.query.filter_by(post_id=post_id).order_by(Comment.posted.desc())  
    title = post.title
    return render_template('post.html',title = title, comments=comments, comment_form=form, post=post, quote=quote)
    
@main.route('/post/update/<post_id>',methods = ['GET','POST'])
@login_required
def update_blog(post_id):
    form=PostForm()
    post = Post.query.filter_by(id = post_id).first()
    if post is None:
        abort(404)       
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data       

        db.session.add(post)
        db.session.commit()
       
        return redirect(url_for('.blog_post', post_id=post_id))
    
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        post.post_pic_path = path
        db.session.commit()
        return redirect(url_for('.blog_post', post_id=post_id))
      
    title = 'Update post'

    return render_template('update_post.html', title=title, post_form=form, post=post)  

