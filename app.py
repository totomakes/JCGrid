import os
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import shutil
# Gen requirements
import random
import json
from PIL import Image
random.seed(1)

# List files in directory
# Get files in directories
def getDir(someDir):
    ABG=os.listdir(someDir)
    for fichier in ABG[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".png")):
            ABG.remove(fichier)
    templist = []
    for i in ABG:
        templist.append(someDir+i)
    return templist

# Get asset directory list
a = os.listdir("./static/assets/")
assetfolders = []
for x in a:
    if x != ".DS_Store":
        assetfolders.append(x)  
assetfolders.sort()
# print(assetfolders)


# 




UPLOAD_FOLDER = './static/assets'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
        
        # RESET THE FILES IN ASSETS FOLDER
        shutil.rmtree("./static/assets")
        os.mkdir("./static/assets")

        # GET THE NEW FILES
        files = request.files.getlist("file")
        assetcategories = []

        # CREATE FOLDERS NEEDED IN SERVER
        for file in files:
            filename = secure_filename(file.filename)
            #   Asset Category
            assetcategory = (filename.split('_', 3)[1])

            if not filename.endswith('DS_Store'):
                if str(assetcategory) not in assetcategories:
                    if not os.path.exists("./static/assets/"+str(assetcategory)):
                    # Create folder for category
                        os.mkdir("./static/assets/"+str(assetcategory)) 
                        assetcategories.append(str(assetcategory))
                    print("categories:")
                    print(assetcategories)

        # COPY FILES TO THE SERVER
        for file in files:
            filename = secure_filename(file.filename)
            assetname = (filename.split('_', 2)[-1])
            assetcategory = (filename.split('_', 3)[1])
            if not filename.endswith('DS_Store'):
                file.save("./static/assets/"+assetcategory+"/"+assetname)
        

        # a = getDir("./static/assets/"+assetfolders[0]+"/")
        list1 = []
        for x in a:
            list1.append(str(x).split("/")[-1])
        print(list1)
        
        
              
        # GENERATE KIDZ
        amountofkidz = 15
        # Get a random asset function
        def get_asset(number):
            return(random.choice(getDir("./static/assets/"+assetfolders[number]+"/")))
        
        # check duplicates variable
        kidz = []

        # For every cat -> create an assembled cat array
        for n in range(amountofkidz):
            if len(kidz) == amountofkidz:
                break
            else:
                assembledkid = []
                # pick an asset from everyfolder.
                
                for m in range(len(assetfolders)):
                    assembledkid.append(get_asset(m))
                # print(assembledburukat)

                if assembledkid not in kidz:
                    kidz.append(assembledkid)
        
        amountoflayers = len(kidz[0])
        
        print(len(kidz[0]))
        

        


        
        return render_template("generate.html", list1=list1, kidz=kidz, amountoflayers=amountoflayers)





# Create a list of all the files in each folder.
# PASS IT to the generate.html as variables






if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
