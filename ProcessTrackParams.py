import os
 
# make_edges reads an image from /pfs/images and outputs the result of running
# edge detection on that image to /pfs/out. Note that /pfs/images and
# /pfs/out are special directories that Pachyderm injects into the container.
def add_text(filename):
    inputfile = open(filename, "r")
    a = inputfile.read() 
    b = a + "added text"
    inputfile.close()
    tail = os.path.split(filename)[1]
    outputfile = open(os.path.join("/pfs/out", os.path.splitext(tail)[0]+".txt"),"w")
    outputfile.write(b)
    outputfile.close()

# walk /pfs/images and call make_edges on every file found
for dirpath, dirs, files in os.walk("/pfs/trackparams"):
    for file in files:
        add_text(os.path.join(dirpath, file))
