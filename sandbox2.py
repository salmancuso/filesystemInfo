import csv
import sys
import os
import subprocess
from tqdm import tqdm
from multiprocessing import Pool
import re

sizeLabel = {"b":"byte","k":"Kilobyte","m":"Megabyte","g":"Gigabyte","t":"Terabyte","p":"Petabyte","kb":"Kilobyte","mb":"Megabyte","gb":"Gigabyte","tb":"Terabyte","pb":"Petabyte"}

#################################################################
##### CAPTURE THE FOLDER/FILE DETAILS FROM A 'ls -d' BASH COMMAND
##### AND RETURN A LIST OF ALL DIRECTORIES 
def firstLevelDirs(folderPath):
    folderPath = cleanPath(folderPath)
    # print(folderPath)
    # print("Seizing Folder Details. Please Wait.\n")
    command = "ls -d {}*/".format(folderPath)
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
    # print("Seizing Folder Details. Please Wait.\n")
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
        dataOut.writerow(["folderPath","totalFileSize","sizeType","fileLastModifiedDate","dirCount","fileCount"])

        
#################################################################
##### APPEND TO THE LOG FILE
##### 
def fileAppend(dirDetails):
    with open('./dirLog.csv', 'a') as rawDataOutput:
        dataOutAppend = csv.writer(rawDataOutput, delimiter=",", quotechar='"')
        dataOutAppend.writerow([dirDetails["folderPath"],dirDetails["totalFileSize"],dirDetails["sizeType"],dirDetails["fileLastModifiedDate"],dirDetails["dirCount"],dirDetails["fileCount"]])


#################################################################
##### BUILD THE ERROR LOG
##### 
def errorFileMaker():
    with open('./errorLog.csv', 'w') as rawDataOutput:
        dataOut = csv.writer(rawDataOutput, delimiter=",", quotechar='"')

        
#################################################################
##### APPEND TO THE ERROR LOG FILE
##### 
def errorFileAppend(fullPath):
    with open('./errorLog.csv', 'a') as rawDataOutput:
        dataOutAppend = csv.writer(rawDataOutput, delimiter=",", quotechar='"')
        dataOutAppend.writerow([fullPath])

    
#################################################################
##### THIS IS THE MAIN LOOP THAT ITERATES OVER THE LIST SENT FROM
##### THE folderDetails FUNCTION. OUTPUT IS A SIMPLE DICTIONARY
def dirWalker(folderPath):
    print(folderPath)
    folderPath = cleanPath(folderPath)
    payload = folderDetails(folderPath)
    # print("Parsing Folder Details.\n")

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
            try:
                directorySize = fileDirRow[0]
                print("_______{}________".format(directorySize))
                sizeNumber = float(re.findall(r'(\d+\.\d+)',str(directorySize))[0])
                directorySizeStripped = re.sub(r'[^A-Za-z]+', "", directorySize)
                sizeType = sizeLabel[re.findall(r'(\D+)',str(directorySizeStripped))[0].lower()]
                print(sizeNumber, sizeType)
            except:
                errorFileAppend(fullPath)
        else:
            None
    lastTouch = sorted(list(set(lastTouch)))

    dirDetails["totalFileSize"] = sizeNumber
    dirDetails["sizeType"] = sizeType
    dirDetails["fileLastModifiedDate"] = lastTouch[-1]
    dirDetails["folderPath"]=folderPath
    dirDetails["dirCount"] = dirCount
    dirDetails["fileCount"] = fileCount
    fileAppend(dirDetails)

#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
if __name__ == "__main__":
    fileMaker()
    errorFileMaker()
    cpuCores = int(sys.argv[1])
    topLevelDir = sys.argv[2]

    directoryList = firstLevelDirs(topLevelDir)
    for i in tqdm(range(len(directoryList))):
        dirWalker(directoryList[i])


