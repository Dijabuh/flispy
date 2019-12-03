Lisp Interpreter in Python

Description:
For my project I will be creating a Lisp interpreter in Python. I will be implementing the classic version of Lisp described at http://pythonpracticeprojects.com/lisp.html. The interpeter will use a repl and work with a command line interface. The interpreter will support Atoms, Lists, the 4 basic symbols of +,-,*,/, and the 9 symbols eq?, quote, cons, car, cdr, atom?, define, lambda, and cond. The eval symbol will be applied automatically during each repl cycle.

Algorithim:
I will be using a parsing algorithim to tokenize the given Lisp expression, build it into a syntax tree, and then evaluate the syntax tree.

Libraries:
I do not anticipate needing any libraries for this project other than built in Python libraries, however if this changes throughout the development of this project I will update this document accordingly.
Update: I will be using the copy library for creating deep copies of python dictionaries.

Plan of Work:
I will start out by making Python classes to represent atoms, symbols, and lists. Then I will develop the parser to read input and break it up into atoms symbols and lists. After that I will develop the evaluator to evaluate whatever is passed in from the parser. Finally, I will implement the repl and a proper shell to write Lisp commands in.
