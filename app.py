import os
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import shutil
# Gen requirements
import random
import json
from PIL import Image
from flask import send_file


# List files in directory
# Get files in directories
def getDir(someDir):
    ABG=os.listdir(someDir)
    for fichier in ABG[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".jpg")):
            ABG.remove(fichier)
    templist = []
    for i in ABG:
        templist.append(someDir+i)
    return templist




UPLOAD_FOLDER = './static/assets'
GRID = './static/grid/grid.jpg'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html")

# DOWNLOAD FILE
@app.route('/download', methods=['GET', 'POST'])
def download():
    return send_file(GRID, as_attachment=True)

@app.route('/generate', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
        
        # RESET THE FILES IN ASSETS FOLDER
        shutil.rmtree("./static/assets")
        os.mkdir("./static/assets")

        shutil.rmtree("./static/resized")
        os.mkdir("./static/resized")

        # GET THE NEW FILES
        files = request.files.getlist("file")
        # assetcategories = []

        # CREATE FOLDERS NEEDED IN SERVER
        # for file in files:
        #     filename = secure_filename(file.filename)
            #   Asset Category
            # assetcategory = (filename.split('_', 3)[1])

            # if not filename.endswith('DS_Store'):
            #     if str(assetcategory) not in assetcategories:
            #         if not os.path.exists("./static/assets/"+str(assetcategory)):
            #         # Create folder for category
            #             os.mkdir("./static/assets/"+str(assetcategory)) 
            #             assetcategories.append(str(assetcategory))
            #         print("categories:")
            #         print(assetcategories)

        # COPY FILES TO THE SERVER
        for file in files:
            filename = secure_filename(file.filename)
            assetname = (filename.split('_', 2)[-1])
            if not filename.endswith('DS_Store'):
                file.save("./static/assets/"+assetname)
        
        # DEFINE asset folders
        # global assetfolders
        # assetfolders = getdirectories() 


                    
        # create image grid
        def get_concat_h(im1, im2, im3, im4, im5, im6, im7, im8, im9):
            dst = Image.new('RGB', (5000, 5000))
            dst.paste(im1, (985, 235))
            dst.paste(im2, (985+im1.width+15, 235))
            dst.paste(im3, (985+im1.width+im2.width+30, 235))
            dst.paste(im4, (985, im1.height+15+235))
            dst.paste(im5, (985+im1.width+15, im1.height+15+235))
            dst.paste(im6, (985+im1.width+im2.width+30, im1.height+15+235))
            dst.paste(im7, (985, im1.height+im3.height+30+235))
            dst.paste(im8, (985+im1.width+15, im1.height+im3.height+30+235))
            dst.paste(im9, (985+im1.width+im2.width+30, im1.height+im3.height+30+235))
        
            return dst

        images = getDir('./static/assets/')
        print("IMAGES")
        print(images)

        for image in images:
            name = os.path.basename(image)
            print(name)
            x = Image.open(image)
            x.thumbnail((1000, 1500))
            x.save('./static/resized/'+name) 


        images2 = getDir('./static/resized/')  
        print("resized images")
        print(images2)

        get_concat_h(Image.open(images2[0]), Image.open(images2[1]), Image.open(images2[2]), Image.open(images2[3]), Image.open(images2[4]), Image.open(images2[5]), Image.open(images2[6]), Image.open(images2[7]), Image.open(images2[8])).save('./static/grid/grid.jpg')

        grid = './static/grid/grid.jpg'

        return render_template("generate.html", grid=grid)

@app.route('/generate2', methods = ['GET', 'POST'])
def randomizekidz():
    # GENERATE KIDZ
    amountofkidz = 15
    # Get a random asset function
    def get_asset(number):
        return(random.choice(getDir("./static/assets/"+assetfolders[number]+"/")))
        print("GOT ASSETS")
    
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
    return render_template("generate2.html", kidz=kidz, amountoflayers=amountoflayers)
        





# Create a list of all the files in each folder.
# PASS IT to the generate.html as variables






if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)
