import csv
import sys
import os
import subprocess
from tqdm import tqdm
from multiprocessing import Pool
import re
import time


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
    command = "du -acb --time {}".format(folderPath)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    outputRowResults = []
    while True:
        output = process.stdout.readline()
        if len(output) == 0 and process.poll() is not None:
            break
        if output:
            try:
                outputRow = output.strip().decode("utf-8")
                outputRowResults.append(str(outputRow))
            except:
                errorFileAppend(fullPath)
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
        dataOut.writerow(["folderPath","terabyteSize","byteSizeHumanReadable","fileLastModifiedDate","dirCount","fileCount","topFiles"])

#################################################################
##### MAKE HUMAN READABLE FILE/FOLDER SIZES
##### 
def sizeConvert(numb, suffix='b'):
    byteSize = int(numb)
    for unit in ['','k','m','g','t','p','e','z']:
        if abs(byteSize) < 1024.0:
            return "%3.1f%s%s" % (byteSize, unit, suffix)
        byteSize /= 1024.0
    return "%.1f%s%s" % (byteSize, 'Yi', suffix)
        
#################################################################
##### APPEND TO THE LOG FILE
##### 
def fileAppend(dirDetails):
    with open('./dirLog.csv', 'a') as rawDataOutput:
        dataOutAppend = csv.writer(rawDataOutput, delimiter=",", quotechar='"')
        dataOutAppend.writerow([dirDetails["folderPath"],dirDetails["terabyteSize"],dirDetails["byteSizeHumanReadable"],dirDetails["fileLastModifiedDate"],dirDetails["dirCount"],dirDetails["fileCount"],dirDetails["topFiles"]])


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
    try:
        folderPath = cleanPath(folderPath)
        payload = folderDetails(folderPath)

        lastTouch =[]
        dirDetails = {}
        dirCount = 0
        fileCount = 0
        topFilesTemp = {}
        for item in tqdm(payload):
            item = item.replace("|","")
            fileDirRow = item.split("\t")
            lastTouch.append(fileDirRow[1])
            path=fileDirRow[2]  
            if os.path.isdir(path): 
                dirCount += 1 
            elif os.path.isfile(path):  
                fileCount += 1
                fileSize = fileDirRow[0]
                topFilesTemp[int(fileSize)] = path
            elif fileDirRow[-1].lower() == "total":
                byteSize = float(fileDirRow[0])
                terabyteSize = float(fileDirRow[0])/float(1099511627775.9978)
                byteSizeHumanReadable = sizeConvert(byteSize) 
            else:
                None
        lastTouch = sorted(list(set(lastTouch)))
        
        top5Count = 0
        topFiles = {}
        for key, value in sorted(topFilesTemp.items(), key=lambda item: item[0], reverse=True):
            if top5Count <11:
                topFiles[key]=[sizeConvert(key),value]
                top5Count +=1

        dirDetails["terabyteSize"] = terabyteSize
        dirDetails["byteSizeHumanReadable"] = byteSizeHumanReadable
        dirDetails["fileLastModifiedDate"] = lastTouch[-1]
        dirDetails["folderPath"]=folderPath
        dirDetails["dirCount"] = dirCount
        dirDetails["fileCount"] = fileCount
        dirDetails["topFiles"] = topFiles
        fileAppend(dirDetails)
    except:
        errorFileAppend(fullPath)


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
    
    p = Pool(processes=cpuCores)
    result = p.map(dirWalker, directoryList)   ## Pass values from someList to function
    p.close()
    p.join()
    # for row in tqdm(directoryList):
    #     dirWalker(row)
