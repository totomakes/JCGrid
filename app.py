# Implements a registration form, storing registrants in a SQLite database, with support for deregistration
from cs50 import SQL
from flask import Flask, redirect, render_template, request
import os
import random
import sqlite3


app = Flask(__name__)
app.debug = True

db = SQL("sqlite:///kidassets.db")


def getDir(someDir):
    ABG=os.listdir(someDir)
    for fichier in ABG[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".png")):
            ABG.remove(fichier)
    templist = []
    for i in ABG:
        templist.append(someDir+i)
    return templist

def getDir2(someDir):
    ABG=os.listdir(someDir)
    for fichier in ABG[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".jpg")):
            ABG.remove(fichier)
    templist = []
    for i in ABG:
        templist.append(someDir+i)
    return templist
# 
# 
# 
# ASSET LISTS
# Extract Back layer files
Backpacksfullpath = getDir("./static/Assets/back/")
backpacks = []
for x in Backpacksfullpath:
    backpacks.append(str(x).split("/")[-1])

Strapsfullpath = getDir("./static/Assets/straps/")
straps = []
for x in Strapsfullpath:
    straps.append(str(x).split("/")[-1])

Eyesfullpath = getDir("./static/Assets/eyes/")
eyes = []
for x in Eyesfullpath:
    eyes.append(str(x).split("/")[-1])

Mouthfullpath = getDir("./static/Assets/mouth/")
mouths = []
for x in Mouthfullpath:
    mouths.append(str(x).split("/")[-1])

Nosefullpath = getDir("./static/Assets/nose/")
noses = []
for x in Nosefullpath:
    noses.append(str(x).split("/")[-1])

Facedecorationfullpath = getDir("./static/Assets/facedecoration/")
facedecos = []
for x in Facedecorationfullpath:
    facedecos.append(str(x).split("/")[-1])

Facetrait1fullpath = getDir("./static/Assets/facetrait1/")
faces1 = []
for x in Facetrait1fullpath:
    faces1.append(str(x).split("/")[-1])

Facetrait2fullpath = getDir("./static/Assets/facetrait2/")
faces2 = []
for x in Facetrait2fullpath:
    faces2.append(str(x).split("/")[-1])

Hairfullpath = getDir("./static/Assets/hair/")
hairs = []
for x in Hairfullpath:
    hairs.append(str(x).split("/")[-1])



# Extract Kidz to show
Kidzfullpath = getDir2("./static/kidz/")
kidz = []
for x in Kidzfullpath:
    kidz.append(str(x).split("/")[-1])


class kid:
    def __init__(self) -> None:
        pass
    currentkid = ""
    def selectrandomkid():
        nextkid = random.choice(kidz) 
        while nextkid in kidlist:
            nextkid = random.choice(kidz)
        kid.currentkid = nextkid
        return nextkid

def updatekidzdone():
    # Check database
    paper = db.execute("SELECT kidasset FROM kidlog")
    for x in paper:
        if x not in kidlist:
            kidlist.append(x['kidasset'])
    print(kidlist)
    kid.selectrandomkid()

kidlist = []
updatekidzdone()

     

@app.route("/")
def index():
    return render_template("index.html", backpacks=backpacks, straps=straps, eyes=eyes, mouths=mouths, noses=noses, facedecos=facedecos, faces1=faces1, faces2=faces2, hairs=hairs, kid=kid.selectrandomkid() )


@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM kidz WHERE id = ?", id)
        db.execute("DELETE FROM kidlog WHERE id = ?", id)
    return redirect("/registrants")


@app.route("/register", methods=["POST"])
def register():

    # Validate submission
    # name = request.form.get("name")
    back = request.form.get("back")
    strap = request.form.get("strap")
    eye = request.form.get("eye")
    mouth = request.form.get("mouth")
    nose = request.form.get("nose")
    facedeco = request.form.get("facedeco")
    face1 = request.form.get("face1")
    face2 = request.form.get("face2")
    hair = request.form.get("hair")
    # if not name or sport not in SPORTS:
    if back not in backpacks:
        return render_template("failure.html")

    # Remember registrant
    # db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)
    db.execute("INSERT INTO kidz (kidasset, back, straps, eyes, mouth, nose, facedecoration, facetrait1, facetrait2, hair) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", kid.currentkid, back, strap, eye, mouth, nose, facedeco, face1, face2, hair)
    db.execute("INSERT INTO kidlog (kidasset) VALUES(?)", kid.currentkid)
    updatekidzdone()



    # Confirm registration
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    kidz = db.execute("SELECT * FROM kidz")
    return render_template("registrants.html", kidz=kidz)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)