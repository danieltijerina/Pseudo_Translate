import sys
#from reserved import py_reserved, cpp_reserved
import shlex

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/cpp", methods=['GET', 'POST'])
def cpp():
	print(str(request.values))
	return render_template('index.html')

if __name__ == "__main__":
	app.run()

current_line = 0

indent = ''

my_file = open(sys.argv[1], 'r')
language = sys.argv[2]
if language == "c++":
	output_file = open("output.cpp", 'w')
elif language == "py":
	output_file = open("output.py", 'w')
content = my_file.readlines()
variables_dict = dict()

def startfile():
	if language == "c++":
		output_file.write('#include <iostream>\n')
		output_file.write('using namespace std;\n\n')

def makeprintcpp(printOutput):
	printOutput.pop(0)
	output_string = indent + "cout"
	for word in printOutput:
	        output_string += " << "
	        output_string += word
	output_string += ";"
	output_file.write(output_string)
	output_file.write('\n')

def makeforcpp(words_in_line):
	global indent
	output_string = indent + "for(int " + words_in_line[1]
	output_string += " = " + words_in_line[3] + "; "
	output_string += words_in_line[1] + " <= " + words_in_line[5] + "; "
	output_string += words_in_line[1] + "++) {\n"
	output_file.write(output_string)
	next_line = nextline()
	indent += "\t"
	while next_line[0] != 'endfor':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-3]
	output_file.write(indent + '}\n') 

def makefunccpp(words_in_line):
	global indent
	output_string = indent + words_in_line[3]
	output_string += " " 
	output_string += words_in_line[1]
	output_string += "() {\n"
	output_file.write(output_string)
	next_line = nextline()
	indent += "\t"
	while next_line[0] != 'endfunc':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-3]
	output_file.write('}\n')

def makewhilecpp(words_in_line):
	global indent
	output_string = indent + "while( "
	words_in_line.pop(0)
	for word in words_in_line:
		output_string += word + " "
	output_string += ") {\n"
	output_file.write(output_string);
	next_line = nextline()
	indent += "\t"
	while next_line[0] != 'endwhile':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-3]
	output_file.write(indent + '}\n')


def printvariable(words_in_line):
	if words_in_line[0] in variables_dict:
		output_string = indent
	elif words_in_line[0][-1] != ')':
		if language == "c++":
			output_string = indent + "auto "
		else :
			output_string = indent
		variables_dict[words_in_line[0]] = "True"
	else:
		output_string = indent
	for word in words_in_line:
 		output_string += word + " "
	output_string += ";\n"
	output_file.write(output_string)

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

def makeElseIfcpp(words_in_line):
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

def makeprintpy(words_in_line):
	words_in_line.pop(0)
	if len(words_in_line) == 0:
		output_file.write(indent + "print()")
		return
	if words_in_line[0][0] == '"':
		output_string = indent + "print(" + words_in_line[0]
	else:
		output_string = indent + "print(str(" + words_in_line[0] + ")"
	words_in_line.pop(0)
	for word in words_in_line:
		if word[0] == '"':
			output_string += " + " + word
		else:
			output_string += " + str(" + word + ")"
	output_string += ")"
	output_file.write(output_string+"\n")

def makeforpy(words_in_line):
	global indent
	output_string = indent + "for " + words_in_line[1] + " in range( "
	output_string += words_in_line[3] + ", " + words_in_line[5] + "):\n"
	output_file.write(output_string)
	next_line = nextline()
	indent += "\t"
	while next_line[0] != 'endfor':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-1]

def makewhilepy(words_in_line):
	global indent
	output_string = indent + "while "
	words_in_line.pop(0)
	for word in words_in_line:
		output_string += word + " "
	output_string += ": \n"
	output_file.write(output_string);
	next_line = nextline()
	indent += "\t"
	while next_line[0] != 'endwhile':
	    checkToken(next_line)
	    next_line = nextline()
	indent = indent[0:len(indent)-3]
	output_file.write(indent + '\n')

def makefuncpy(words_in_line):
	global indent
	output_string = indent + "def " + words_in_line[1] + "():\n"
	output_file.write(output_string)
	indent += "\t"
	next_line = nextline()
	while next_line[0] != 'endfunc':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-1]
	output_file.write('\n')

def makeIfpy(words_in_line):
	words_in_line.pop(0)
	global indent
	output_string = indent + "if "
	for word in words_in_line:
		output_string += word + " "
	output_string += ": \n "
	output_file.write(output_string)
	indent += "\t"
	next_line = nextline()
	while next_line[0] != 'endif' and next_line[0] != 'else' and next_line[0] != 'elif':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-1]
	checkToken(next_line)

def makeEndIfpy(words_in_line):
	global indent
	output_file.write("\n")

def makeElseIfpy(words_in_line):
	global indent
	words_in_line.pop(0)
	output_string = indent + "elif "
	for word in words_in_line:
		output_string += word + " "
	output_string += ": \n"
	output_file.write(output_string)
	indent += "\t"
	next_line = nextline()
	while next_line[0] != 'endif' and next_line[0] != 'else':
		checkToken(next_line)
		next_line = nextline()
		indent = indent[0:len(indent)-1]
		checkToken(next_line)

def makeElsepy(words_in_line):
	global indent
	#print len(indent)
	#indent = indent[0:len(indent)-1]
	output_string = indent + "else: \n"
	output_file.write(output_string)
	indent += "\t"
	next_line = nextline()
	while next_line[0] != 'endif':
		checkToken(next_line)
		next_line = nextline()
	indent = indent[0:len(indent)-1]
	checkToken(next_line)

def nextline():
	global current_line
	if current_line >= len(content):
		return "-1"
	line = content[current_line]
	current_line += 1
	words = shlex.split(line, posix=False)
	return words

def checkToken(words_in_line):
	if len(words_in_line) == 0:
		output_file.write('\n')
		return
	if language == 'c++':
		if words_in_line[0] in cpp_reserved:
			cpp_reserved[words_in_line[0]](words_in_line)
		else:
			printvariable(words_in_line)
	elif language == 'py':
		if words_in_line[0] in py_reserved:
			py_reserved[words_in_line[0]](words_in_line)
		else:
			printvariable(words_in_line)
		
cpp_reserved = {
        # print tokens
        'var' : 'auto',
        'print' : makeprintcpp,
        ',' : '<<',
        'for' : makeforcpp,
	'func' : makefunccpp,
	',' : '<<',
	'while' : makewhilecpp,
        # loop tokens

        # condition tokens
	'if' : makeIfcpp,
        'else' : makeElsecpp,
        'elif' : makeElseIfcpp,
        'endif' : makeEndIfcpp,

}

py_reserved = {
        'print' : makeprintpy,
        'for' : makeforpy,
	'func' : makefuncpy,
	'if' : makeIfpy,
	'elif' : makeElseIfpy,
	'else' : makeElsepy,
	'endif' : makeEndIfpy,	
	'while' : makewhilepy,
	',' : '+',
}		

startfile()
while current_line < len(content):
	words_in_line  = nextline()
	checkToken(words_in_line)
