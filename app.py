from flask import Flask,render_template,request,session,url_for,redirect
from cs50 import SQL
from flask_session import Session
import os,sys,random,json
from helpers import *
app = Flask(__name__)

db = SQL("sqlite:///books.db")

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    result = db.execute("INSERT INTO users(username,password)\
                        VALUES(:username,:password)",\
                        username = request.form.get("username"),password = request.form.get("password"))

    return "Registered Successfuly"

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
    message="login successful"
    title=[]
    descr=[]
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

    #return render_template("success.html",message=title)  
    #return render_template('practice.html',user = session['username'],password = session['password'])
    return render_template('indexfinal.html',user = session['username'],password = session['password'],\
                             title=title,descr=descr,sub=sub,imglink=imglink)

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
    prelink.append(result['items'][0]['volumeInfo']['previewLink'])


    return render_template("subpage.html",title=title,author=author,imglink=imglink,publish_date=publish_date,page_count=page_count,\
                            isbn10=isbn10,isbn13=isbn13,prelink=prelink)

@app.route("/addbook",methods=['POST','GET'])
def addbook():
    db.execute("INSERT INTO userbooks(username,password,bookid)\
                 VALUES(:username,:password,:bookid)",\
                 username=session['username'],password = session['password'],bookid= request.form.get("bookisbn"))
    return render_template("success.html",message="successfullu inserted")

@app.route("/mybooks",methods=['POST','GET'])
def mybooks():
    books = db.execute("SELECT * FROM userbooks where username=:username and password=:password",
                    username=session['username'],password = session['password'])
    rows = len(books)
    author=[]
    imglink=[]
    publish_date=[]
    page_count=[]
    isbn10=[]
    isbn13=[]
    prelink=[]
    for book in books:
        result = lookupisbn(book.isbn)
        title.append(result['items'][0]['volumeInfo']['title'])
        author.append(result['items'][0]['volumeInfo']['authors'])
        imglink.append(result['items'][0]['volumeInfo']['imageLinks']['thumbnail'])
        publish_date.append(result['items'][0]['volumeInfo']['publishedDate'])    
        page_count.append(result['items'][0]['volumeInfo']['pageCount'])
        isbn10.append(result['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'])
        isbn13.append(result['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier'])
        prelink.append(result['items'][0]['volumeInfo']['previewLink'])


    return render_template("mybooklist.html",title=title,author=author,imglink=imglink,publish_date=publish_date,page_count=page_count,\
                            isbn10=isbn10,isbn13=isbn13,prelink=prelink)

        
    return render_template("mybooklist.html",title=title,author=author,result=result)
                 
    
@app.route("/home",methods=['POST','GET'])
def transfer():
    return render_template("indexfinal.html")
app.secret_key = "secret"
if __name__ == "__main__":    
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()
 