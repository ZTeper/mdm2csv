
# Zachary Teper
# March 17, 2024

class dataBase:
  columns = []
  iccap_vars = {}
  dataRows = []

  def __init__(self, columns=[], iccap_vars={}, dataRows=[]):
    self.columns = []
    self.iccap_vars = {}
    self.dataRows = []

  def clear(self):
    self.columns = []
    self.iccap_vars = {}
    self.dataRows = []
    

inputFileName = input("MDM file name (*.mdm file extension): ")
inputFile = open(inputFileName, 'r')
fileLines = [line.rstrip() for line in inputFile]
inputFile.close()

print("Parsing input file...")

# Parse input file
dataBaseList = []
dataBaseStartIndex = 0
dataBaseEndIndex   = 0
while True:
  try:
    dataBaseStartIndex = fileLines.index("BEGIN_DB", dataBaseEndIndex+1)
    dataBaseEndIndex   = fileLines.index("END_DB",   dataBaseEndIndex+1)
    dataBaseLines = fileLines[dataBaseStartIndex+1 : dataBaseEndIndex-1]
  except ValueError:
    if not dataBaseList:
      print("ERROR: no databases")
      exit()
    else:
      break

  db = dataBase()
  db.clear()
  for line in dataBaseLines:
    if not line: # Skip blank lines
      continue

    # Process the line
    words = line.split()
    if words[0] == "ICCAP_VAR": # ICCAP variables
      db.iccap_vars[words[1]] = words[2]
    elif words[0][0] == '#': # title row
      words[0] = words[0][1:] # Remove initial '#'
      db.columns = words + list(db.iccap_vars.keys())
    else: # data row
      db.dataRows.append(words + list(db.iccap_vars.values()))

  dataBaseList.append(db)

print("Done parsing input")
print(len(dataBaseList), " databases detected")

outputFileName = input("CSV file name (*.csv file extension): ")
outputFile = open(outputFileName, 'w')

print("Writing output file...")

# Write output file

# write the columns; assume all databases have the same columns
for column in dataBaseList[0].columns:
  outputFile.write(column + ',')
outputFile.write('\n')

# write the data rows
for db in dataBaseList:
  for row in db.dataRows:
    for word in row:
      outputFile.write(word + ',')
    outputFile.write('\n')

outputFile.close()
print("Done writing output")

