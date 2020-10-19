import re

directorySize = "240.49tb"
sizeNumber = float(re.findall(r'(\d+\.\d+)',str(directorySize))[0])
print (sizeNumber)