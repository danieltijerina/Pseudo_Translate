import sys
#from reserved import py_reserved, cpp_reserved 
import shlex

current_line = 0

indent = ''

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
	global indent
	indent += "\t"

def makeprintcpp(printOutput):
	printOutput.pop(0)
	output_string = indent + "cout  "
	for word in printOutput:
		output_string += "<<"
		output_string += word
	output_string += ";"
	output_file.write(output_string)
	output_file.write('\n')

def makeforcpp(words_in_line):
	global indent
	output_string = indent "for(int "
	output_string += words_in_line[1]
	output_string += " = "
	output_string += words_in_line[3]
	output_string += "; "
	output_string += words_in_line[1]
	output_string += " <= "
	output_string += words_in_line[5]
	output_string += "; "
	output_string += words_in_line[1]
	output_string += "++) {\n"
	output_file.write(output_string)
	next_line = nextline()
	indent =+ "\t"
	while next_line[0] != 'endfor':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-3]
	output_file.write('}\n') 

def makeIfcpp(words_in_line):
	words_in_line.pop(0)
	global indent
	output_string = indent + "if ( "
	for word in words_in_line:
		output_string += word + " "
	output_string += ") { \n"
	output_file.write(output_string+"\n")
	indent += "\t"

def makeElsecpp(words_in_line):
	global indent
	indent = indent[0:len(indent)-3]
	output_string = indent + "} else { \n"
	output_file.write(output_string+"\n")
	indent += "\t"

def makeElseIfcpp(words_in_line)
	global indent
	indent = indent[0:len(indent)-3]
	output_string = indent + "} else if ( "
	for word in words_in_line:
		output_string += word + " "
	output_string += ") { \n"
	output_file.write(output_string+"\n")
	indent += "\t"

def makeEndIfcpp(words_in_line):
	global indent
	indent = indent[0:len(indent)-3]
	output_string = indent + "} \n"
	output_file.write(output_string+"\n")

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
        'print' : makeprintcpp,
        ',' : '<<',
        'for' : makeforcpp,

        # loop tokens

        # condition tokens
	'if' : makeIfcpp,
        'else' : makeElsecpp,
        'elif' : makeElseIfcpp,
        'endif' : makeEndIfcpp,

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
