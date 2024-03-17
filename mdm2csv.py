
# Zachary Teper
# March 16, 2024

import csv

inputFileName = input("MDM file name (*.mdm file extension): ")
inputFile = open(inputFileName, 'r')
fileLines = [line.rstrip() for line in inputFile]
inputFile.close()

print("Parsing input file...")

# Parse input file
header = []
try:
  headerStartIndex = fileLines.index("BEGIN_HEADER")
  headerEndIndex   = fileLines.index("END_HEADER")
  headerLines = fileLines[headerStartIndex+1 : headerEndIndex-1]
except ValueError:
  print("ERROR: missing header")
  exit()

for line in headerLines:
  if not line: # Skip blank lines
    continue
  header.append([line.split()])

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

  dataBase = []
  for line in dataBaseLines:
    if not line: # Skip blank lines
      continue
    dataBase.append([line.split()])
  dataBaseList.append(dataBase)

print("Done parsing input")

outputFileName = input("CSV file name (*.csv file extension): ")
outputFile = open(outputFileName, 'w')

print("Writing output file...")

# Write output file
for line in header:
  for word in line[0]:
    outputFile.write(word + ',')
  outputFile.write('\n')


for dataBase in dataBaseList:
  outputFile.write('\n')
  for line in dataBase:
    for word in line[0]:
      if word[0] == '#': # Remove initial '#'
        word = word[1:]
      outputFile.write(word + ',')
    outputFile.write('\n')

outputFile.close()
print("Done writing output")

