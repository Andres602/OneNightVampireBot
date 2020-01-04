def buildFile2(selection):
    path="./files/text/"
    inFiles=""
    sleep=""
    end=""
    with open("".join([path,"Begin",".txt"]),'r') as myfile:
        inFiles = myfile.read()
    with open("".join([path,"UndostresDormir.txt"]), 'r') as myfile:
        sleep = myfile.read()
    with open("".join([path,"End.txt"]), 'r') as myfile:
        end = myfile.read()
    cFile=None
    vampires= False
    for name in selection:
        imMaster=False
        if name in ['Vampire', 'The Count', 'The Master'] and not vampires:
            vampires = True
            imMaster = True if name == "The Master" else False
            with open("".join([path,"Vampires",".txt"]),'r') as myfile:
                cFile = myfile.read()
            if "Renfield" in selection:
                with open("".join([path,"Vampires_Renfield",".txt"]),'r') as myfile:
                    cFile = cFile+myfile.read()
                cFile=cFile+sleep
                with open("".join([path,"Renfield",".txt"]),'r') as myfile:
                    cFile = cFile+myfile.read()
                selection.remove("Renfield")
                if name ==  "The Count":
                    cFile=cFile+sleep
                    with open("".join([path,name,".txt"]),'r') as myfile:
                        cFile = cFile+myfile.read()
        elif name == "Assassin" and "Apprentice Assassin" in selection:
            with open("".join([path,name,".txt"]),'r') as myfile:
                cFile = myfile.read()
            with open("".join([path,"Apprentice Assassin",".txt"]),'r') as myfile:
                cFile = cFile+myfile.read()
            selection.remove("Apprentice Assassin")
        elif name == "Next" and "Cupid" in selection:
            with open("".join([path,name,".txt"]),'r') as myfile:
                cFile = myfile.read()
            cFile=cFile+sleep
            with open("".join([path,"Love",".txt"]),'r') as myfile:
                cFile = cFile+myfile.read()
        elif not name=="The Master":
            with open("".join([path,name,".txt"]),'r') as myfile:
                cFile = myfile.read()
        if imMaster or not name=="The Master":
            cFile=cFile+sleep
            inFiles=inFiles+cFile
    inFiles=inFiles+end
    return inFiles


if __name__ == "__main__":
    characters=["Renfield","Apprentice Assassin","Next","Marksman"]
    textOut=buildFile2(characters,path)
    print textOut