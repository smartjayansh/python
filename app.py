from flask import Flask,render_template,request,session,url_for,redirect
from cs50 import SQL
from flask_session import Session
import os,sys,random,json
from helpers import *
import smtplib,random 
import colorama
colorama.init()

app = Flask(__name__)

db = SQL("sqlite:///books.db")


@app.route("/send")
def send():
    num=random.randint(100,800)
    session['code']= num
    link = "http://127.0.0.1:5000/passchange?code="+ str(num)
    # your Gmail account 
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login("sender gmail", "password") 

    # message to be sent 
    msg = "\r\n".join([
    "From: trialdubey@gmail.com",
    "To: jaitechy@gmail.com",
    "Subject: Just a message",
    "",
    link
    ])
    # sending the mail 
    s.sendmail("trialdubey@gmail.com", "jaitechy@gmail.com", msg) 

    # terminating the session 
    s.quit() 
    return "successful" + str(num)





@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return index()

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        result = db.execute("INSERT INTO users(username,password)\
                        VALUES(:username,:password)",\
                        username = request.form.get("username"),password = request.form.get("password"))
        return render_template("login.html")
    else:
        return render_template("signup.html")
@app.route("/logout",methods=["POST","GET"])
def logout():
    session['logged_in'] = False
    return home()

@app.route("/login",methods=["POST","GET"])
def login():
    
    session['username']= request.form.get("username")
    session['password']= request.form.get("password")

    # ensure username was submitted
    if not request.form.get("username"):
        message="Must provide username"
        return render_template("success.html",message=message)
    # ensure password was submitted
    elif not request.form.get("password"):
        message="Must provide password"
        return render_template("success.html",message=message)
    # query database for username 
    rows = db.execute("SELECT * FROM users \
                       WHERE username = :username and password = :password", \
                       username=session['username'],password=session['password'])
    # ensure username exists and password is correct
    if len(rows) != 1:
        message="invalid username and/or password"
        return render_template("success.html",message=message)
    session['logged_in'] = True

    return index()
@app.route("/forgot",methods=["POST","GET"])
def forgot():
    if request.method == "POST":
        session['temp']=request.form.get('username')
        row = db.execute("Select * from users where username=:username",\
        username=session['temp'])
        if len(row) == 0:
            return render_template("success.html",message="invalid username")
        else:
            return send()
            # return render_template("newpass.html")
    else:
        return render_template("forgotpassword.html") 
#################################################################################
@app.route("/passchange",methods=["POST","GET"])
def passchange():
    if int(request.args.get('code')) == int(session['code']):
        return render_template("newpass.html")
    else:
        return render_template("success.html",message="Otp Link is not valid")

@app.route('/realchange',methods=["POST","GET"])
def realchange():
    newpass = request.form.get('newpass')
    confirmpass = request.form.get('confirmpass')
    if newpass  == confirmpass:
        row= db.execute("UPDATE users SET password=:password WHERE username=:username",\
                        username=session['temp'],password= newpass)
        if row:
            return render_template("success.html",message="password successfully changed")

@app.route("/index")
def index():
    title=[]
    descr=[]
    isbn=[]
    sub=["comedy","adventure","technology","cooking"]
    imglink=[]
    for i in range(0,4):
        if i<1:
            result = lookupsub(sub[0])
        elif i<2:
            result = lookupsub(sub[1])
        elif i<3:     
            result = lookupsub(sub[2])
        else:        
            result = lookupsub(sub[3])
        for j in range(0,4):    
            title.append(result['items'][j]['volumeInfo']['title'])
            descr.append(result['items'][j]['volumeInfo']['publisher'])
            imglink.append(result['items'][j]['volumeInfo']['imageLinks']['thumbnail'])
            isbn.append(result['items'][j]['volumeInfo']['industryIdentifiers'][0]['identifier'])
    #return render_template("success.html",message=isbn)

    return render_template('indexfinal.html',user = session['username'],password = session['password'],\
                             title=title,descr=descr,sub=sub,imglink=imglink,isbn=isbn)

@app.route('/search',methods=["POST","GET"])
# googleapikey="AIzaSyAaVB1rnJ5Yi5o4MBb4gMAzv6pHi6scTfA"
def search():
    # makelist of everyone
    result = lookup(request.form.get("tit"))
    title=[]
    author=[]
    imglink=[]
    publish_date=[]
    page_count=[]
    isbn10=[]
    isbn13=[]
    for i in range(0,4):
        title.append(result['items'][i]['volumeInfo']['title'])
        author.append(result['items'][i]['volumeInfo']['authors'])
        imglink.append(result['items'][i]['volumeInfo']['imageLinks']['thumbnail'])
        publish_date.append(result['items'][i]['volumeInfo']['publishedDate'])    
        page_count.append(result['items'][i]['volumeInfo']['pageCount'])
        isbn10.append(result['items'][i]['volumeInfo']['industryIdentifiers'][0]['identifier'])
        isbn13.append(result['items'][i]['volumeInfo']['industryIdentifiers'][1]['identifier'])

    return render_template("searchresult.html",title=title,author=author,imglink=imglink,publish_date=publish_date,page_count=page_count,\
                            isbn10=isbn10,isbn13=isbn13)
@app.route("/details",methods=['POST','GET'])
def details():
    result = lookupisbn(request.form.get("isbn"))
    templist=[]
    row = db.execute("Select bookid from userbooks where username=:username",username=session['username'])
    for item in row:
        templist.append(item['bookid'])
    trulist=[]
    title=[]
    author=[]
    imglink=[]
    publish_date=[]
    page_count=[]
    isbn10=[]
    isbn13=[]
    prelink=[]
    title.append(result['items'][0]['volumeInfo']['title'])
    author.append(result['items'][0]['volumeInfo']['authors'])
    imglink.append(result['items'][0]['volumeInfo']['imageLinks']['thumbnail'])
    publish_date.append(result['items'][0]['volumeInfo']['publishedDate'])    
    page_count.append(result['items'][0]['volumeInfo']['pageCount'])
    isbn10.append(result['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'])
    isbn13.append(result['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier'])
    if int(result['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']) in templist :
        trulist.append(bool(None))
    else:
        trulist.append(bool("true"))

    prelink.append(result['items'][0]['volumeInfo']['previewLink'])

    rows = db.execute("Select * from comments where bookid=:bookid",bookid=request.form.get("isbn"))

    return render_template("subpage.html",title=title,author=author,imglink=imglink,publish_date=publish_date,page_count=page_count,\
                            isbn10=isbn10,isbn13=isbn13,prelink=prelink,rows=rows,trulist=trulist)
    # return render_template("success.html",message=trulist)
@app.route("/addbook",methods=['POST','GET'])
def addbook():
    db.execute("INSERT INTO userbooks(username,password,bookid)\
                 VALUES(:username,:password,:bookid)",\
                 username=session['username'],password = session['password'],bookid= request.form.get("bookisbn"))
    return render_template("success.html",message="successfully inserted")

@app.route("/mybooks",methods=['POST','GET'])
def mybooks():
    
    results= db.execute("SELECT bookid FROM userbooks where username=:username and password=:password",
                    username=session['username'],password = session['password'])
    rows=len(results)
    author=[]
    imglink=[]
    publish_date=[]
    page_count=[]
    isbn10=[]
    isbn13=[]
    prelink=[]
    title=[]
    for i in range(0,rows):
        result = lookupisbn(str(results[i]['bookid']))
        author.append(result['items'][0]['volumeInfo']['authors'])
        imglink.append(result['items'][0]['volumeInfo']['imageLinks']['thumbnail'])
        publish_date.append(result['items'][0]['volumeInfo']['publishedDate'])    
        page_count.append(result['items'][0]['volumeInfo']['pageCount'])
        isbn10.append(result['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'])
        title.append(result['items'][0]['volumeInfo']['title'])
        isbn13.append(result['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier'])
        prelink.append(result['items'][0]['volumeInfo']['previewLink'])
    return render_template("mybooklist.html",rows=rows,title=title,author=author,imglink=imglink,publish_date=publish_date,page_count=page_count,isbn10=isbn10,isbn13=isbn13,prelink=prelink)
                 
    # return render_template("success.html",message=result['items'][0]['volumeInfo']['title'])

@app.route("/comment",methods=['POST','GET'])
def comment():
    db.execute("INSERT INTO comments(bookid,comment)\
                 VALUES(:bookid,:comment)",\
                 comment=request.form.get('comment'),bookid= request.form.get("bookisbn"))
    return render_template("success.html",message="successfully inserted")

@app.route("/home",methods=['POST','GET'])
def transfer():
    return render_template("indexfinal.html")
app.secret_key = "secret"
if __name__ == "__main__":    
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()
 