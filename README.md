#Lisp Interpreter in Python. Made for final project in CIS4930

##How to run:
-python3 main.py
-Requires Python3

##Supports 9 basic lisp functions
-define: Binds a symbol to an expression
-eq?: Checks if 2 values are equal
-quote: Returns the symbols it is passed
-cons: Returns a list containing the 2 arguments
-car: Returns the first element of a list
-cdr: Returns a list of all but the first element in a list
-atom?: Returns true if the argument is an atom
-lambda: Creates a user defined function. Used with the define function to bind a symbol to a function
-cond: Creates a block if if/then/else statements
-Also supports 4 basic arithmatic operations + - * /

-Use !quit to quit the program
-Use !load to load in lisp definitions from a given file
-example: !load test.file

-test.file is provided with simple function definitions for boolean operations
