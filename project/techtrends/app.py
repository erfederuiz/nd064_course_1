import sqlite3
import global_values

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    increase_DbConns()
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Techtrends CCN project 1
# Define the metrics endpoint
def get_allPosts():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    # Techtrends CCN project 1
    # Define the metrics endpoint
    set_PostsCount(len(posts))
    connection.close()
    return posts 

def increase_DbConns():
    global_values.dbConnections += 1

def get_DbConns():
    return global_values.dbConnections

def get_PostsCount():
    return global_values.postsCount

def set_PostsCount(count):
    global_values.postsCount = count 
    

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application 
@app.route('/')
def index():
    posts = get_allPosts()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('Article id ' + str(post_id) +  " doesn\'t exist!")
      return render_template('404.html'), 404
    else:
      app.logger.info('Article "' + post['title']+  '" retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About page retrieved!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            app.logger.info('Article "' + title +  '" created!')
            # Techtrends CCN project 1
            # Define the metrics endpoint
            posts = connection.execute('SELECT * FROM posts').fetchall()
            set_PostsCount(len(posts))
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

#Techtrends CCN project 1

# Define the healthz endpoint
@app.route('/healthz')
def healthz():
    return jsonify(result='OK - healthy'), 200

# Define the metrics endpoint
@app.route('/metrics')
def metrics():
    #posts = get_allPosts()
    metricsOut = {"db_connection_count": get_DbConns(), "post_count": get_PostsCount()}
    return jsonify(metricsOut), 200

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111', debug=True)
