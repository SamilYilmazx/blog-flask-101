from functools import wraps
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "mydatabase" #it can be generated as random or can be entered manually

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "mydatabase" #your database
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

 
class RegisterForm(Form):
    name = StringField("Name:",validators=[validators.Length(min=4,max=25)])
    username = StringField("Username:",validators=[validators.Length(min=5,max=35)])
    email = StringField("E-mail Address:",validators=[validators.Email(message="Please, enter a valid email.. ")])
    password = PasswordField("Password:",validators=[
        validators.DataRequired(message="Please enter a password."),
        validators.EqualTo(fieldname="confirm",message="Passwords are not matched.")
    ])
    confirm = PasswordField("Confirm Password:")
    
class LoginForm(Form):
    username = StringField("Username:")
    password = PasswordField("Password:")


#Login Decorator 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view the page.","danger")
            return redirect(url_for("login"))
    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

#Article Detail Page
@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE id = %s"
    result = cursor.execute(query,(id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article)
    else:
        return render_template("article.html")

#Dashboard Page
@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE author = %s"
    result = cursor.execute(query,(session["username"],))
    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles=articles)
    else:
        return render_template("dashboard.html")


@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)        
        cursor = mysql.connection.cursor()
        query = "INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash("Successfully registered.","success")

        return redirect(url_for("login")) 
    else:
        return render_template("register.html",form = form)


@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        result = cursor.execute(query,(username,))
        
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Successfully Logged-In...","success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Wrong Password...","danger")
                return redirect(url_for("login"))
        else:
            flash("This user doesn't exist...","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



#Add Article
@app.route("/addarticle",methods=["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO articles(title,author,content) VALUES(%s,%s,%s)"
        cursor.execute(query,(title,session["username"],content))
        mysql.connection.commit()
        cursor.close()
        flash("Article is successfully added.","success")
        return redirect(url_for("dashboard"))
    return render_template("addarticle.html",form = form)


#Update Article
@app.route("/edit/<string:id>",methods=["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM articles WHERE id = %s AND author = %s"
        result = cursor.execute(query,(id,session["username"]))
        if result == 0:
            flash("There is no such an article or you are not authorized.","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form=form)
    else:
        #POST REQUEST
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data

        query2 = "UPDATE articles SET title = %s, content = %s WHERE id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query2,(newTitle,newContent,id))
        mysql.connection.commit()
        flash("Article is updated.","success")
        return redirect(url_for("dashboard"))


#Delete Article
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE author = %s AND id = %s"
    result = cursor.execute(query,(session["username"],id))
    if result > 0:
        query2 = "DELETE FROM articles WHERE id = %s"
        cursor.execute(query2,(id,))
        mysql.connection.commit()
        flash("Article is deleted successfully.","success")
        return redirect(url_for("dashboard"))
    else:
        flash("There's no such an article or you're not authorized.","danger")
        return redirect(url_for("index"))

#Main Articles Page 
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles"
    result = cursor.execute(query)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)
    else:
        return render_template("articles.html")


class ArticleForm(Form):
    title = StringField("Article Title:",validators=[validators.Length(min=5,max=100)])
    content = TextAreaField("Article Content:",validators=[validators.Length(min=10)])


#Search for article
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM articles WHERE title LIKE '%" + keyword + "%' "
        result = cursor.execute(query)

        if result == 0:
            flash("No matches for what you're looking for..","warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)


if __name__ == "__main__":
    app.run(debug=True) 