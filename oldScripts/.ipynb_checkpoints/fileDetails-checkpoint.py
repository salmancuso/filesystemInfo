import glob
import time
import os
import math
import time


#### CONVERT FILESIZE FROM BYTES TO HUMAN READABLE
def convertSize(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 4)
   return "%s %s" % (s, size_name[i])


#### ENSURE CONSISTANCY IN TOP LEVEL PATH WITH "/" AT END
#### OF THE PASSED PATH STRING
def cleanPath(pathToClean):
    if pathToClean[-1] != "/":
        cleanPath = str(pathToClean) + str("/")
        return pathToClean
    else:
        return pathToClean


####  THIS IS THE MAIN FUNCTION THAT RETURNS THE FOLLOWING
####     dirCount == Number of sub dirtories
####     fileCount == Number of files in total
####     totalFileSize == The total size (recursively) from the top dir in human readable format
####     lastModified == The last time a file was modifid in the directory.
def dirWalker(pathToWalk):
    dirDetails = {}
    dirCount = 0
    fileCount = 0
    totalFileSize = 0
    lastTouched = float(0)
    walkPath = cleanPath(pathToWalk)
    for root, dirs, files in os.walk(walkPath, topdown=True):
        for name in dirs:
            # dirNamePath = (os.path.join(root, name))
            dirCount += 1

        for name in files:
            # fileNamePath = (os.path.join(root, name))
            fileCount += 1
            fp = os.path.join(root, name)
            #### SKIP IF IT IS A SYMBOLIC LINK
            if not os.path.islink(fp):
                totalFileSize += os.path.getsize(fp)
                lastModified = os.path.getctime(fp)
                if float(lastTouched) < float(lastModified):
                    lastTouched = lastModified
                else:
                    None


    dirDetails["dirCount"] = dirCount
    dirDetails["fileCount"] = fileCount
    dirDetails["totalFileSize"] = convertSize(totalFileSize)
    dirDetails["fileLastModifiedDate"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastTouched))
    return dirDetails


if __name__ == "__main__": 
#     topLevelDir = "/ifs/gsb/usf_interns"
    topLevelDir = "/ifs/gsb/smancuso"
    print(dirWalker(topLevelDir))