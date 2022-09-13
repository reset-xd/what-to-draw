from codecs import escape_encode
from csv import reader, writer
import sqlite3 as sql
from random import choice
from turtle import home
from bs4 import BeautifulSoup
from hashlib import md5

connection = sql.connect("./database/ideas.db")
userconnection = sql.connect("./database/user_info.db")
cursor = connection.cursor()
usercursor = userconnection.cursor()
usercursor.execute("CREATE TABLE IF NOT EXISTS USERS (username TEXT primary key, description TEXT, completed TEXT, liked TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS IDEAS (id INTEGER primary key, title TEXT, description TEXT, tag TEXT, reference TEXT, likes INTEGER)")

def gen_homepage_ideas():
    template= """
    <div class="d-lg-flex justify-content-lg-center" id="main" style="text-align: center;margin-top: 42px; width: 100%">
        <div id=" main-box" style="background: #000000; border-radius: 10px; color: white;padding-bottom: 22px;padding-top: 22px; width: 100%">
            <div onclick="window.location.href =  '/idea/{3}';" style="padding-top: 22px;padding-bottom: 22px;">
                <h1>{0}</h1>
                <p style="text-align: right;padding-right: 22px;padding-left: 22px;color: rgb(205,205,205);">{2}</p>
                <p  style="text-align: left;padding-right: 22px;padding-left: 22px;">{1}</p>
            </div>
            <button id="clickablebutton-{3}" onclick="likeIdea({3})" class="btn btn-primary" type="button" style="color: black;background: white;padding: 6px 20px;border-radius: 9px;border-style: none;border-color: black;"><i class="far fa-heart"></i>&nbsp;LIKE</button>
        </div>
    </div>
    """
    ret = ""
    cursor.execute("SELECT * FROM IDEAS")
    a = cursor.fetchall()
    for x in a[:10]:
        ret += template.format(x[1], x[2][:200] + "...", x[3], x[0])
    return ret

homepage_content = gen_homepage_ideas()

def gen_recent_ideas():
    template= """
    <div class="d-lg-flex justify-content-lg-center" id="main" style="text-align: center;margin-top: 42px; width: 100%">
        <div id=" main-box" style="background: #000000; border-radius: 10px; color: white;padding-bottom: 22px;padding-top: 22px; width: 100%">
            <div onclick="window.location.href =  '/idea/{3}';" style="padding-top: 22px;padding-bottom: 22px;">
                <h1>{0}</h1>
                <p style="text-align: right;padding-right: 22px;padding-left: 22px;color: rgb(205,205,205);">{2}</p>
                <p  style="text-align: left;padding-right: 22px;padding-left: 22px;">{1}</p>
            </div>
            <button onclick="alert('a')" class="btn btn-primary" type="button" style="color: black;background: white;padding: 6px 20px;border-radius: 9px;border-style: none;border-color: black;"><i class="far fa-heart"></i>&nbsp;LIKE</button>
        </div>
    </div>
    """
    ret = ""
    cursor.execute("SELECT * FROM IDEAS")
    a = cursor.fetchall()
    for x in a[::-1][:10]:
        ret += template.format(x[1], x[2][:200] + "...", x[3], x[0])
    return ret

recent_content = gen_recent_ideas()

def gen_id():
    a = cursor.execute("SELECT * FROM IDEAS").fetchall()
    return len(a) + 1

def usercheck(username, password:str):
    with open("./database/users.csv") as file:
        data = reader(file)
        if [username, md5(password.encode()).hexdigest()] in list(data):
            return True
    return False

def usernamecheck(username):
    with open("./database/users.csv") as file:
        data = reader(file)
        for x in list(data):
            if username == x[0]:
                return True
    return False

def adduser(username:str, password:str):
    try:
        if not usernamecheck(username) and username.isalpha():
            with open("./database/users.csv", "a", newline="") as file:
                data = writer(file)
                data.writerow([username, md5(str(password).encode()).hexdigest()])
                usercursor.execute("INSERT INTO USERS(username, description, completed, liked) VALUES(?, ?, ?, ?)", (username, "no description.", "[]", "[]"))
                userconnection.commit()
            return True
    except:
        return False
    return False

def add_idea(title, description, tag, images=""):
    title = title_validator(title)
    description = description_validator(description)
    tag = tag_validator_and_returner(tag)
    images = reference_validator_and_returner(images) if images != "" else ""
    if title_validator(title) != False and tag != False and description != False and images != False:
        cursor.execute("INSERT INTO IDEAS (id, title, description, tag, reference, likes) VALUES (?, ?, ?, ?, ?, ?)", (gen_id(), title, description, tag, images, 0))
        connection.commit()
        global recent_content 
        recent_content = gen_homepage_ideas()
        return True


def add_like(idea_id):
    try:
        cursor.execute("UPDATE IDEAS SET likes = likes + 1 WHERE id = ?", (idea_id,))
        connection.commit()
        return True
    except:
        return False

def remove_like(idea_id):
    try:
        cursor.execute("UPDATE IDEAS SET likes = likes - 1 WHERE id = ?", (idea_id,))
        connection.commit()
        return True
    except:
        return False

def title_validator(x:str):
    """
    title should be less than 200 characters
    """
    if len(x) <= 200:
        return BeautifulSoup(x.strip(), "html.parser").text
    return False

def description_validator(x:str):
    """
    title should be less than 4000 characters
    """
    if len(x) <= 4000:
        return BeautifulSoup(x.strip(), "html.parser").text
    return False

def reference_validator_and_returner(x:str):
    """
    image seperator ";"
    must have imgur
    must start with https
    """
    x = x.strip().split(";")
    for y in x:
        if not y.startswith("https://i.imgur.com/"):
            return False
    return BeautifulSoup(x, "html.parser").text

def tag_validator_and_returner(x:str):
    """
    tags seperated with spaces
    should start with #
    """
    x1 = x.strip().split(" ")
    for y in x1:
        if not y.startswith("#"):
            return False
    return BeautifulSoup(x, "html.parser").text


def get_userinfo(username):
    try:
        usercursor.execute("SELECT * FROM USERS WHERE username = ?", (username, ))
        data = usercursor.fetchone()
        if data is not None:
            return data
        return ("no user", "if no user then ofc no description", "[]", "[]")
    except:
        return ("no user", "if no user then ofc no description", "[]", "[]")

def get_idea_by_id(idea_id):
    try:
        cursor.execute("SELECT * FROM IDEAS WHERE id = ?", (idea_id,))
        resp = cursor.fetchone()
        return resp
    except:
        return ("None", "None", "None", "None", "")


def edit_description(username, description):
    try:
        usercursor.execute("UPDATE USERS SET description = ? WHERE username = ?", (description, username))
        userconnection.commit()
    except:
        return False

# edit_description("resetxd", "wow such a cool thing to have here.")

# get_userinfo("resetxd")

def user_add_like(idea_id):
    try:
        usercursor
    except:
        return False

def edit_completed():
    pass