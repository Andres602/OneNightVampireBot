from pydub import AudioSegment

path="./files/mp3/"
def buildFile(selection,fileOut,duration):
    inFiles=[]
    outFile="".join([path,'out/',fileOut,".mp3"])
    for name in selection:
        if name in ['Vampire', 'The Count', 'The Master'] and "Renfield" in selection:
            inFiles.append(path+'Vampires_Renfield.mp3')
            if name ==  'The Count':
                inFiles.append("".join([path,name,".mp3"]))
        elif name in ['Vampire', 'The Count', 'The Master']:
            inFiles.append(path+'Vampires.mp3')
            if name ==  'The Count':
                inFiles.append("".join([path,name,".mp3"]))
        elif name == "Assassin" and "Apprentice Assassin" in selection:
            inFiles.append(path+'Assasin_apprentince.mp3')
        else:
            inFiles.append("".join([path,name,".mp3"]))
    inFiles=f7(inFiles)
    print inFiles
    inFiles.append("".join([path,"endCharacters.mp3"]))
    inFiles.append("".join([path,duration,".mp3"]))

    data=AudioSegment.from_mp3("".join([path,"begin.mp3"]))
    for inFile in inFiles:
        voice = AudioSegment.from_mp3(inFile)
        data=data+voice
    data.export(outFile, format="mp3")
    print "archivo %s creado"%(fileOut)
    return outFile

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
