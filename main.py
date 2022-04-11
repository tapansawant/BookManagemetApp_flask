from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect('BookManagementApp.db', check_same_thread=False)

cursor = con.cursor()

listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOK_DETAILS'").fetchall()

if listOfTables:
    print("Table Already Exists ! ")
else:
    con.execute(''' CREATE TABLE BOOK_DETAILS(
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            BOOKNAME TEXT,
                            AUTHOR TEXT,
                            CATEGORY TEXT,
                            PRICE TEXT,
                            PUBLISHER TEXT ); ''')
    print("Table has created")

listOfTable2 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='USER'").fetchall()

if listOfTable2:
    print("Table2 Already Exists ! ")
else:
    con.execute(''' CREATE TABLE USER(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT,
                            ADDRESS TEXT,
                            EMAIL TEXT,
                            PHONE TEXT,
                            PASSWORD TEXT ); ''')
    print("Table has created")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def navbar():
    return render_template("Home.html")


@app.route("/login-user", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        getEmail = request.form["email"]
        getPswd = request.form["pswd"]

        # print(getEmail)
        # print(getPswd)

        try:
            query = "SELECT * FROM USER WHERE EMAIL = '" + getEmail + "' AND PASSWORD = '" + getPswd + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid User")
            else:
                print(len(result))
                return render_template("base_user.html")
        except Exception as e:
            print(e)
    return render_template("login_user.html")


@app.route("/register-user", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        getUsername = request.form["uname"]
        getAddr = request.form["address"]
        getEmail = request.form["email"]
        getPhone = request.form["mno"]
        getPswd = request.form["pswd"]

        print(getUsername)
        print(getAddr)
        print(getEmail)
        print(getPhone)
        print(getPswd)

        try:
            data = (getUsername, getAddr, getEmail, getPhone, getPswd)
            insert_query = '''INSERT INTO USER(NAME, ADDRESS, EMAIL, PHONE, PASSWORD) 
                                VALUES (?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            con.commit()
            print("User added successfully")
            return redirect("/login-user")

        except Exception as e:
            print(e)
    return render_template("register_user.html")


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        getUsername = request.form["uname"]
        getPswd = request.form["pswd"]
        if getUsername == "admin" and getPswd == "9875":
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def addbook():
    if request.method == "POST":
        getName = request.form["name"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]
        print(getName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        try:
            data = (getName, getAuthor, getCategory, getPrice, getPublisher)
            insert_query = '''INSERT INTO BOOK_DETAILS(BOOKNAME, AUTHOR, CATEGORY, PRICE, PUBLISHER) 
                                VALUES (?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            con.commit()
            print("Book added successfully")
            return redirect("/view")

        except Exception as e:
            print(e)

    return render_template("dashboard.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getName = request.form["bname"]
        print(getName)
        try:
            cursor.execute("SELECT * FROM BOOK_DETAILS WHERE BOOKNAME = '" + getName + "'")
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid book name")
            else:
                print(len(result))
                return render_template("search.html", book=result, status=True)
        except Exception as e:
            print(e)

    return render_template("search.html", book=[])


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        getName = request.form["bname"]
        print(getName)
        try:
            con.execute("DELETE FROM BOOK_DETAILS WHERE BOOKNAME = '" + getName + "'")
            print("SUCCESSFULLY DELETED!")
            con.commit()
            return redirect("/view")
        except Exception as e:
            print(e)
    return render_template("delete.html")


@app.route("/update", methods=['GET', 'POST'])
def Update():
    return render_template("update.html")


@app.route("/view")
def View():
    cursor.execute("SELECT * FROM BOOK_DETAILS")
    result = cursor.fetchall()
    return render_template("view.html", books=result)


@app.route("/cardview")
def cardview():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM BOOK_DETAILS")
    result = cursor.fetchall()
    return render_template("cardview.html", books=result)


@app.route("/searchforuser")
def search_user():
    if request.method == "POST":
        getName = request.form["bname"]
        print(getName)
        try:
            cursor.execute("SELECT * FROM BOOK_DETAILS WHERE BOOKNAME = '" + getName + "'")
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid book name")
            else:
                print(len(result))
                return render_template("user_search.html", book=result, status=True)
        except Exception as e:
            print(e)

    return render_template("user_search.html", book=[])


@app.route("/viewforuser")
def View_user():
    cursor.execute("SELECT * FROM BOOK_DETAILS")
    result = cursor.fetchall()
    return render_template("view_user.html", books=result)


if __name__ == "__main__":
    app.run()
