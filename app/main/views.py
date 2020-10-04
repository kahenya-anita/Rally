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

@main.route('/comment/delete/<post_id>/<comment_id>',methods = ['GET','POST'])
@login_required
def delete_comment(comment_id, post_id):
    comment= Comment.query.filter_by(id = comment_id).first() 
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('.blog_post', post_id=post_id))



@main.route('/subscribe',methods = ['GET','POST'])
def subscribe():
    quote=get_quote()
    form=SubscribeForm()

    if form.validate_on_submit():
        new_email = form.email.data             

        # Updated subscriber instance
        this_subscriber = Subscriber(email=new_email)

        # save subscriber method
        this_subscriber.save_subscriber()

        mail_list=[]
        mail_list.append(new_email)
        
        mail_message("You subscribed to the Blog post.","email/new_subscriber",mail_list)
        
        return redirect(url_for('.index'))   
    
    title = 'Subscribe'
    return render_template('subscribe.html',title = title, subscription_form=form, quote=quote)
    

@main.route('/unsubscribe',methods = ['GET','POST'])
def unsubscribe():
    quote=get_quote()
    form=UnsubscribeForm()

    if form.validate_on_submit():
        new_email = form.email.data             

        unsubscriber= Subscriber.query.filter_by(email = new_email).first() 
        db.session.delete(unsubscriber)
        db.session.commit()

        mail_list=[]
        mail_list.append(new_email)
        
        mail_message("You've unsubscribed from  The Blog post.","email/bye",mail_list)
        
        return redirect(url_for('.index'))   
    
    title = 'Unsubscribe'
    return render_template('unsubscribe.html',title = title, unsubscribe_form=form, quote=quote)


@main.route('/contact',methods = ['GET','POST'])
def contact():
    quote=get_quote()
    form=ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        title = form.title.data
        message = form.message.data        
        
        # Updated contact instance
        this_contact = Contact(name=name, email=email, title=title, message=message)

        # save contact method
        this_contact.save_contact()

        mail_list=[]
        mail_list.append(email)
        
        mail_message("We've received your message","email/receipt",mail_list, this_contact=this_contact)

        to_me=[]
        to_me.append("anitakahenya1@gmail.com")
        
        mail_message("You've been contacted","email/mail_me",to_me, this_contact=this_contact)
        
        return redirect(url_for('.contact'))   
    
    title = 'Contact'
    return render_template('contact.html',title = title, contact_form=form, quote=quote)


@main.route('/profile')
def profile():
    quote=get_quote() 
    blog_posts=Post.query.order_by(Post.posted.desc())
    author = User.query.first()

    if author is None:
        abort(404)

    title='Author profile'
    return render_template('profile.html', author=author, posts=blog_posts, quote=quote)


@main.route('/update_profile',methods = ['GET','POST'])
@login_required
def update_profile(): 
    quote=get_quote()
    author = User.query.first()

    if author is None:
        abort(404)
    form = UpdateProfile()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        author.prof_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile'))

    if form.validate_on_submit():
        author.bio = form.bio.data
        author.name = form.name.data

        db.session.add(author)
        db.session.commit()

        return redirect(url_for('.profile'))

    title='Update profile'
    return render_template('update_profile.html', form=form, quote=quote, title=title)




