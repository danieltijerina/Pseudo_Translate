var editor = ace.edit("editor");
var print = "print <foo>";
var if_text = "if <condition> \n \t <body> \n else \n \t <body> \n endif";

function addText(type){
	var if_text = "if <condition> \n \t <body> \n else \n \t <body> \n endif";
	var print_text = "print <foo>";
	var loop_text = "loop <from> : <end> \n \t <body> \n endloop";
	if(type=="if")
		editor.session.insert(editor.getCursorPosition(), if_text);
	if(type=="loop")
		editor.session.insert(editor.getCursorPosition(), loop_text);
	if(type=="print")
		editor.session.insert(editor.getCursorPosition(), print_text);
}