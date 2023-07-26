from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Firebase Configuration
firebase_config = {
  "apiKey": "AIzaSyAfXlUbEmCoAMLL2R8dZAAnCGV-1blGlZc",
  "authDomain": "soundly-d366d.firebaseapp.com",
  "databaseURL": "https://soundly-d366d-default-rtdb.firebaseio.com/",
  "projectId": "soundly-d366d",
  "storageBucket": "soundly-d366d.appspot.com",
  "messagingSenderId": "264812583072",
  "appId": "1:264812583072:web:e9a0321b47cf0f629211c5",
  "measurementId": "G-JL047EFH3J"
  
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


def add_comment(user_id, genre, recommendation):
    data = {'user_id': user_id, 'genre': genre, 'recommendation': recommendation}
    db.child('comments').push(data)

def get_comments(genre):
    comments = db.child('comments').order_by_child('genre').equal_to(genre).get()
    return comments.val()


@app.route('/recommendation-rock')
def recommendation_rock():
    return render_template('recommendation-rock.html')


@app.route('/recommendation-country')
def recommendation_country():
    return render_template('recommendation-country.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username= request.form['username']
        bio= request.form['bio']
        try:
            print("0")
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            print("1")
            UID = login_session['user']['localId']
            print("2")
            account={"username":username,"password":password,"full_name":full_name,"email":email,"bio":bio}
            print("3")
            db.child('Users').child(UID).set(account)
            print("4")
            return redirect(url_for('landing_page'))
        except:
            error = "Authentication failed"
   return render_template("signup.html",error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("login.html",error=error)



def add_comment(user_id, comment):
    data = {'user_id': user_id, 'comment': comment}
    db.child('comments').push(data)

def get_comments():
    comments = db.child('comments').get()
    return comments.val()

def delete_comment(comment_id):
    db.child('comments').child(comment_id).remove()

@app.route('/')
def home():
    comments = get_comments()
    return render_template('landing.html', comments=comments)

@app.route('/comment', methods=['POST', 'GET'])
def comment():
    if request.method == 'POST':
        comment = request.form['comment']
        user_id = login_session['user']
        add_comment(user_id, comment)
    return redirect(url_for('home'))

@app.route('/delete/<comment_id>')
def delete(comment_id):
    user_id = login_session['user_id']
    comment = db.child('comments').child(comment_id).get().val()
    if comment['user_id'] == user_id:
        delete_comment(comment_id)
    return redirect(url_for('home'))





































if __name__ == '__main__':
    app.run(debug=True)