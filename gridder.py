from PIL import Image
import os


def getDir(someDir):
    ABG=os.listdir(someDir)
    for fichier in ABG[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".jpg")):
            ABG.remove(fichier)
    templist = []
    for i in ABG:
        templist.append(someDir+i)
    return templist

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

images = getDir('./JCGrid/static/assets/')
print(images)


for image in images:
    name = os.path.basename(image)
    print(name)
    x = Image.open(image)
    x.thumbnail((1000, 1500))
    x.save('./JCGrid/static/resized/'+name) 

images2 = getDir('./JCGrid/static/resized/')  
print(images2)

get_concat_h(Image.open(images2[0]), Image.open(images2[1]), Image.open(images2[2]), Image.open(images2[3]), Image.open(images2[4]), Image.open(images2[5]), Image.open(images2[6]), Image.open(images2[7]), Image.open(images2[8])).save('./JCGrid/static/grid/grid.jpg')


