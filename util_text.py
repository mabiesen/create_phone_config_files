
## read file in whole
def readWhole(filename):
  fh = open(filename,"r")
  return fh.read()

## read file return as array of lines
def readToArray(filename):
  fh = open(filename, "r")
  return fh.readlines()

## write file from array
def writeLineByLine(filename, data):
    with open(filename,'w') as outfile:
        outfile.write("\n".join(data))

## write file in whole
def writeWhole(filename, data):
  fh = open(filename,"w")
  write(data)
  fh.close()

def appendLineByLine(filename, data):
  fh = open(filename, "a")
  fh.writelines(data)
  fh.close

def appendWhole(filename, data):
  fh = open(filename, "a")
  fh.write(data)
  fh.close

## grep file for words: bool
def findWordBool(filename, mymatch):
  myfile = readWhole(filename)
  return(mymatch in myfile)

## grep file for words return line
def findWordLine(filename, mymatch):
  returnarray = []
  myarray = readToArray(filename)
  for thisline in myarray:
    if mymatch in thisline:
      returnarray.append(thisline)
  return returnarray

## delete all from file
def deleteFileData(filename):
  writeWhole(filename, "")

def strip_newline_char(string):
  return string.replace('\r', '').replace('\n', '')
