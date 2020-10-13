import os
import subprocess
import re

def folderDetails(folderPath):
    command = "du -ach --time {}".format(folderPath)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    outputRowResults = []
    while True:
        output = process.stdout.readline()
        if len(output) == 0 and process.poll() is not None:
            break
        if output:
            outputRow = output.strip().decode("utf-8")
            outputRowResults.append(str(outputRow)+str("|"))
    return(outputRowResults)

def fileOrDir(testPath):
    if os.path.isdir(testPath):  
        return "dir"
    elif os.path.isfile(testPath):  
        return "file"  
    else:  
        print("error")

# def dirWalker(payload):


if __name__ == "__main__": 
#     topLevelDir = "/ifs/gsb/usf_interns" ## Test on yen
    topLevelDir = "/Volumes/smancusoSecure/experian"  # Test on local syste
    print(folderDetails(topLevelDir))
