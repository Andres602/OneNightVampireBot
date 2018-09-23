from pydub import AudioSegment
from os import listdir
from os.path import isfile, join
path='./files/'
Files = [f for f in listdir(path) if isfile(join(path, f))]

for inFile in Files:
    data=AudioSegment.from_wav("".join([path,inFile]))
    data.export("".join([path,"mp3/",inFile.split(".")[0],".mp3"]), format="mp3")
print "done"