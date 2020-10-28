import re
import subprocess

def fileNameMaker(folderPath):
    if folderPath[-1] == "/":
        filePathStrip = folderPath[1:-1]
    else:
        filePathStrip = folderPath[1:]
    fileName = re.sub(r'\/', '-', str(filePathStrip))
    return(fileName)


def bundleUp(folderPath, saveDir):
    fileName = "{}/{}.tar.gz".format(saveDir,fileNameMaker(folderPath))
    command = "tar cvf - {} | gzip -9 - > {}".format(folderPath, fileName)
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


if __name__ == "__main__":
    folderPath = "/ifs/gsb/jthuang/"
    saveDir = "/oak/stanford/projects/gsb-eval/freezer"

    bundleUp(folderPath,saveDir)