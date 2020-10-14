import os
import subprocess
import sys
from tqdm import tqdm


#################################################################
##### CAPTURE THE FOLDER/FILE DETAILS FROM A 'du' BASH COMMAND
##### AND RETURN A LIST OF ALL FILES/FOLDERS/SIZES/DATES
def folderDetails(folderPath):
    print("Seizing Folder Details. Please Wait.\n")
    command = "du -ach --time {}".format(folderPath)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    outputRowResults = []
    while True:
        output = process.stdout.readline()
        if len(output) == 0 and process.poll() is not None:
            break
        if output:
            outputRow = output.strip().decode("utf-8")
            outputRowResults.append(str(outputRow))
    return(outputRowResults)


#################################################################
##### APPEND THE FOLDER PATH TO HAVE A CLOSING "/"
##### NOT NEEDED BUT THIS IS A BEST PRACTICE 
def cleanPath(pathToClean):
    if pathToClean[-1] != "/":
        cleanPath = str(pathToClean) + str("/")
        return cleanPath
    else:
        return pathToClean
    
    
#################################################################
##### THIS IS THE MAIN LOOP THAT ITERATES OVER THE LIST SENT FROM
##### THE folderDetails FUNCTION. OUTPUT IS A SIMPLE DICTIONARY
def dirWalker(folderPath):
    folderPath = cleanPath(folderPath)
    payload = folderDetails(folderPath)
    print("Parsing Folder Details.\n")

    lastTouch =[]
    dirDetails = {}
    dirCount = 0
    fileCount = 0
    for item in tqdm(payload):
        fileDirRow = item.split("\t")
        lastTouch.append(fileDirRow[1])
        path=fileDirRow[2]  
        if os.path.isdir(path):  
            dirCount += 1 
        elif os.path.isfile(path):  
            fileCount += 1  
        elif fileDirRow[-1].lower() == "total":  
            directorySize = fileDirRow[0]
        else:
            None
    lastTouch = sorted(list(set(lastTouch)))
    dirDetails["dirCount"] = dirCount
    dirDetails["fileCount"] = fileCount
    dirDetails["totalFileSize"] = directorySize
    dirDetails["fileLastModifiedDate"] = lastTouch[-1]
    dirDetails["folderPath"]=folderPath
    print("\n")
    return(dirDetails)


if __name__ == "__main__": 
#     topLevelDir = "/ifs/gsb/usf_interns" ## HEAVEY TEST ON YEN
#     topLevelDir = "/ifs/gsb/smancuso"  ## LIGHT TEST ON YEN
    topLevelDir = sys.argv[1]
    print(dirWalker(topLevelDir))
