#Optimize:

# STEP 1 - Sort each row prior to creating tuples, which allows to create the same tuple regardless of the Artists order in this particular row. Artists [A,B] and [B,A] will generate same tuple [A,B] with itertools. Combinations method if the row is sorted. 

# STEP 2 - The input file is iterated once.

# STEP 3 - The output file is populated while counting tuples. As soon as tuple count reaches 50, the line is written into the otput csv file.


import collections
import itertools
import sys
import argparse
import os.path
import csv 

# This is the error handler if file does not exist
def checkInputFile(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s you requested does not exist!" % arg)
    else:
        return arg

def parseArgs():

  parser = argparse.ArgumentParser(description='Take input from ${inputFile} and create an output file ${outputfile} with a list of pairs of artists that appear TOGETHER in at least ${listcount} different lists. If no matches are found - return an empty list.')

  parser.add_argument('--inputfile', metavar='FILE',default='input.txt',type=lambda x: checkInputFile(parser, x),
                    help='TXT Input File location. - default: input.txt')

  parser.add_argument('--outputfile', metavar='FILE',default='output.csv',
                    help='CSV Output File location. Running the program again will override the file if already present or create a new file if it doesnt exist. - default: output.csv')

  parser.add_argument('--listcount', metavar='N', type=int, default=50,
                    help='This is the number of times that a tuple should appear in before being written into the output file. In this case it is 50. Range [1-1000]. - default: 50')

  args = parser.parse_args()

  return args


def createMatches(inputFileLocation,outputFileLocation,tupleSize,listCount):

 print ("Checking all favorite artists with the arguments listed below:")
 print ('Input File: {}. Output File: {}. Tuple Size: {}. List Count: {}'.format(inputFileLocation,outputFileLocation,tupleSize,listCount));
 
 favoritesDict = collections.defaultdict(int)
 matches = 0

 #Open file to write results into it. This will create an empty file if there are no matches from the algorithm
 with open(outputFileLocation,'w') as outputFile:
  csv_out=csv.writer(outputFile)
  #Opening the file in order to analyze inputs
  with open(inputFileLocation, 'r') as inputFile:
   reader = csv.reader(inputFile)
   for row in reader:
    if row: # if row is not empty, order it, generate possible combinations taking into account the size of a tuple.
     combinations=list(itertools.combinations(sorted(row), tupleSize))    
     for combination in combinations: #iterate over the above combinations, increment occurence by one if the pair is found in the iteration.
      favoritesDict[combination] += 1
      if favoritesDict[combination] == listCount: #if a combination count reaches 50, write it to the destination file.  
       csv_out.writerow(combination)      
       matches+=1

 print ('We are done here. Number of matches found: {}.  Please check the output file: {}. for detailed matches. '.format(matches,outputFileLocation))
 
def main():
    args = parseArgs()
    createMatches(args.inputfile,args.outputfile,2,args.listcount)

if __name__ == "__main__":
    main()
    