from flask import render_template
from app import app

@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    author = User.query.first() 
    return render_template('index.html',quote=quote, author=author)