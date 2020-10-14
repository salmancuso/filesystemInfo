import re

numberList = ["4k", "200m", "2T", "94g"]
sizeLabel = {"b":"byte",
             "k":"Kilobyte",
             "m":"Megabyte",
             "g":"Gigabyte",
             "t":"Terabyte",
             "p":"Petabyte",
             "kb":"Kilobyte",
             "mb":"Megabyte",
             "gb":"Gigabyte",
             "tb":"Terabyte",
             "pb":"Petabyte",}


for numberCombo in numberList:
    sizeNumber = re.findall(r'(\d+)',str(numberCombo))[0]
    sizeType = sizeLabel(re.findall(r'(\D+)',str(numberCombo))[0].lower())
    