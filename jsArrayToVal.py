#!/usr/bin/python
import argparse
import re
from ast import literal_eval

parser = argparse.ArgumentParser(description="Performs array[index] substitution with its actual value.")
parser.add_argument('--infile', dest='inFile', required=True, help='Input filename.')
parser.add_argument('--outfile', dest='outFile', required=True, help='Output filename.')
parser.add_argument('--array', dest='jsArray', nargs='+', required=True, help='Name of Array(s) to substitute.')

args = parser.parse_args()

def copyFile(filein, fileout):
	fObjIn = open(filein,'r')
	fObjContent = fObjIn.readlines()
	fObjOut = open(fileout, 'w+')
	for line in fObjContent:
		fObjOut.write(line)
	fObjIn.close()
	fObjOut.close()

def subArrays(filename, arrName):
	print "subArrays: filename=%s, arrName=%s" % (filename, arrName)
	fObj = open(filename, 'r')
	fObjContent = fObj.readlines()
	fObj.close()
	expr = 'var\s+'+arrName+'.*?(\[.*?\]);$'
	print "Expression: %s" % expr
	for line in fObjContent:
		hit = re.match(expr,line)
		if(hit):
			jsArr = literal_eval(hit.group(1))
			print "Found jsArray: %s" % jsArr
			changeData(filename, jsArr, arrName)
			break

def changeData(filename, jsArr, arrName):
	for idx, ele in enumerate(jsArr):
		fObj = open(filename, 'r')
		fObjContent = fObj.readlines()
		fObj.close()
		fObj = open(filename, 'w+')
		for line in fObjContent:
			if(arrName+'['+str(idx)+']' in line):
				print "Replacing: %s with %s" % (arrName+'['+str(idx)+']',ele)
				fObj.write(line.replace(arrName+'['+str(idx)+']',ele))
			else:
				fObj.write(line)
		fObj.close()

def main(args):
	copyFile(args.inFile, args.outFile)
	for item in args.jsArray:
		subArrays(args.outFile,item)
		

if(__name__)=="__main__":
	main(args)

