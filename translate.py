import sys
#from reserved import py_reserved, cpp_reserved 
import shlex

current_line = 0

my_file = open(sys.argv[1], 'r')
language = sys.argv[2]
output_file = open("output.cpp", 'w')
content = my_file.readlines()

def endfile() :
        output_file.write('}\n')

def startfile():
        output_file.write('#include <iostream>\n')
        output_file.write('using namespace std;\n\n')
	output_file.write('int main() {\n')

def makeprint(printOutput):
	printOutput.pop(0)
        output_string = "cout  "
        for word in printOutput:
                output_string += "<<"
                output_string += word
        output_string += ";"
        output_file.write(output_string)
	output_file.write('\n')

def nextline():
	global current_line
	if current_line >= len(content):
		return "-1"
	line = content[current_line]
	current_line += 1
	words = shlex.split(line, posix=False)
	return words

def checkToken(words_in_line):
	if language == 'c++':
		cpp_reserved[words_in_line[0]](words_in_line)
		
cpp_reserved = {
        # print tokens
        'var' : 'auto',
        'print' : makeprint,
        ',' : '<<'

        # loop tokens

}

py_reserved = {
        'print' : 'print(',
        ',' : '+',
}		

startfile()
while current_line < len(content):
	words_in_line  = nextline()
	checkToken(words_in_line)
endfile()
