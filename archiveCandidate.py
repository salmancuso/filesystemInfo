import csv
import sys
import os
import subprocess
from tqdm import tqdm
from multiprocessing import Pool  

#################################################################
##### CAPTURE THE FOLDER/FILE DETAILS FROM A 'ls -d' BASH COMMAND
##### AND RETURN A LIST OF ALL DIRECTORIES 
def firstLevelDirs(folderPath):
    folderPath = cleanPath(folderPath)
    print(folderPath)
    print("Seizing Folder Details. Please Wait.\n")
    command = "ls -d {}*/".format(folderPath)
    print (command)
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
##### BUILD THE PRODUCT FILE THAT LOGS THE DATA
##### 
def fileMaker():
    with open('./dirLog.csv', 'w') as rawDataOutput:
        dataOut = csv.writer(rawDataOutput, delimiter=",", quotechar='"')
        dataOut.writerow(["folderPath","totalFileSize","fileLastModifiedDate","dirCount","fileCount"])

        
#################################################################
##### APPEND TO THE LOG FILE
##### 
def fileAppend(dirDetails):
    with open('./dirLog.csv', 'a') as rawDataOutput:
        dataOutAppend = csv.writer(rawDataOutput, delimiter=",", quotechar='"')
        dataOutAppend.writerow([dirDetails["folderPath"],dirDetails["totalFileSize"],dirDetails["fileLastModifiedDate"],dirDetails["dirCount"],dirDetails["fileCount"]])

    
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
        item = item.replace("|","")
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
    fileAppend(dirDetails)


#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
if __name__ == "__main__":
    fileMaker()
#     cpuCores = sys.argv[1]
#     topLevelDir = sys.argv[2]

#     cpuCores = 10
#     topLevelDir = "/ifs/gsb"
    directoryList = firstLevelDirs(topLevelDir)
    
    p = Pool(processes=cpuCores)
    result = p.map(dirWalker, directoryList)   ## Pass values from someList to function
    p.close()
    p.join()