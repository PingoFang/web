# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from markupsafe import escape
from flask import Flask
from flask import url_for
from flask import request
from flask import render_template

app = Flask(__name__)

#test watchlist.html

user= {
       'username': 'Grey Li ',
       'bio':'A boy who loves movies and music .' ,
          }


movies= [
    { 'name':' My Neighbor Totaro ','year ' : ' 1988 ' },
    { 'name' : 'Three Colours 七rilogy ' ,' year ' : ' 1993 ' },
    { 'name' : ' Forrest Gump ', ' year ':' 1994 ' },
    { 'name' : 'Perfect Blue ',' year ':' 1997 ' },
    { 'name': 'The Matrix','year ':'1999 ' },
    { 'name': 'Memento ' , ' year ' :'2000 ' },
    { 'name' :' The Bucket lis 七',' year ': ' 2007 ' } ,
    { 'name':' Black Swan ',' year ' : ' 2010 ' },
    { 'name':' Gone Girl ', ' year ' :'2014 ' },
    { 'name':' CoCo ',' year ':' 2017 ' } ,
]
 
@app.route ('/watchlist')
def watchlist () :
    return render_template( 'watchlist.html', user=user , movies=movies )
    



@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('myweb.html') 

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#       return do_the_login()
#    else:
#        return show_the_login_form()
    
#url_for('static', filename='style.css')

#@app.route("/<name>")
#def hello(name):
#    return f"Hello, {escape(name)}!"

@app.route('/user/<username>')
def profile(username):
    # show the user profile for that user
    return f'{username}\'s profile'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'