import sys
#from reserved import py, cpp 
import shlex

def endfile() :
        output_file.write('}\n')

def startfile():
        output_file.write('#include <iostream>\n')
        output_file.write('using namespace std;\n\n')
	output_file.write('int main() {\n')

def makeprint(printOutput):
        output_string = "cout  "
        for word in printOutput:
                output_string += "<<"
                output_string += word
        output_string += ";"
        output_file.write(output_string)
	output_file.write('\n')

my_file = open(sys.argv[1], 'r')
output_file = open("output.cpp", 'w')
startfile()
content = my_file.readlines()
for line in content:
	words = shlex.split(line, posix=False)
	if words[0] == "print":
		words.pop(0)
		makeprint(words)
endfile()
