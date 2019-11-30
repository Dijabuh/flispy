#functions to test if a given variable is an int/float
def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#class to represent a lisp atom
#can be either a number literal or a string
#if it is a string it will be interpreted as a symbol
class Atom():
    def __init__(self, data):
        self.is_num = False
        self.is_str = False
        if is_int(data):
            self.data = int(data)
            self.is_num = True
        elif is_float(data):
            self.data = int(float(data))
            self.is_num = True
        else:
            self.data = data
            self.is_str = True

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def __add__(self, other):
        if self.is_num and other.is_num:
            return self.data + other.data
        else:
            raise RuntimeError("Cant add 2 atoms that arent both numbers")

    def __sub__(self, other):
        if self.is_num and other.is_num:
            return self.data - other.data
        else:
            raise RuntimeError("Cant subtract 2 atoms that arent both numbers")

    def __mul__(self, other):
        if self.is_num and other.is_num:
            return self.data * other.data
        else:
            raise RuntimeError("Cant multiply 2 atoms that arent both numbers")

    def __floordiv__(self, other):
        if self.is_num and other.is_num:
            return int(self.data / other.data)
        else:
            raise RuntimeError("Cant divide 2 atoms that arent both numbers")

    def __eq__(self, other):
        if isinstance(other, Atom) and other.data == self.data:
            return True
        return False

#class to represent a lisp environment
class Environment():
    def __init__(self, upper_env = None):
        self.env = dict()
        self.upper_env = upper_env
        #if an environemnt was passed in, copy its environment to the new one
        #used for procedure calls
        if upper_env:
            self.env = upper_env.env.copy()

    #binds a symbol to an expression
    def add_symbol(self, symbol, expr):
        self.env[symbol] = expr

    #retreives the expression from a given symbol
    def get_expr(self, symbol):
        if symbol in self.env:
            return self.env[symbol]
        elif self.upper_env:
            return self.upper_env.get_expr(symbol)
        else:
            raise SyntaxError("Symbol not defined")

#class to represent user defined procedures
class Procedure():
    #procedures are created with an environment, body of the procedurem and arguements
    def __init__(self, env, body, args):
        #the procedures environment has an upper_env of the passed environment
        self.env = Environment(env)
        self.body = body
        self.args = args
        self.num_args = len(args)

    #evals procedure
    def eval_proc(self, args):
        if len(args) is not self.num_args:
            raise SyntaxError("Wrong number of arguements for procedure call")
        
        #add arguements to environment
        for i in range(self.num_args):
            self.env.add_symbol(self.args[i], args[i])

        return eval(self.body, self.env)

#tuple represtinig all the primitives in this lisp
Primitives = ("+", "-", "*", "/",
              "eq?", "quote", "cons",
              "car", "cdr", "atom?",
              "define", "lambda", "cond")


#function to break down a line of text into a list valid tokens in lisp
def tokenize(line):
    #list to hold all tokens
    tokens = list()

    #variable to hold the current token
    cur_token = ""

    #loop through the line, construction tokens as we go
    for i in range(len(line)):
        #if the current char is a whitespace, 
        #add the current token to the list of tokens and start making a new one
        #only add token if length is greater than 0
        if line[i].isspace():
            if len(cur_token) > 0:
                tokens.append(cur_token.strip())
                cur_token = ""

        #if current char is a ( or a ) or a '
        #then add the current token to list, and add the ( or ) to list
        #only add current token if length is greater than 0
        elif line[i] in (")", "(", "'"):
            if len(cur_token) > 0:
                tokens.append(cur_token.strip())
                cur_token = ""
            tokens.append(line[i])

        #otherwise, add the current character to the cur_token and loop again
        else:
            cur_token += line[i]
   
    #add last token
    if len(cur_token) > 0:
        tokens.append(cur_token.strip())

    return tokens



#function to parse a list of tokens and create a syntax tree
def parse(tokens):
    syntax_tree = list()

    #if we have no tokens at start, there is an error
    if len(tokens) is 0:
        raise SyntaxError("Expected tokens")
    
    #get current token and take it off tokens list
    cur_token = tokens.pop(0)

    #if we get a ) token, then there is an error
    # ) shouldnt come before ( 
    if cur_token is ")":
        raise SyntaxError("Expected (")

    #if we get a ( then recursivley call parse, adding the output to our parse tokens list
    elif cur_token is "(":
        #loop until we get a ), ending the list
        while tokens[0] is not ")":
            syntax_tree.append(parse(tokens))

        #once we get a ), remove it from the tokens list and return the syntax tree
        tokens.pop(0)
        return syntax_tree

    #if none of the above, token is an atom
    #create an atom and return it
    else:
        atom = Atom(cur_token)
        return atom

#function to replace 'symbol with (quote symbol)
#finds ' in the syntax tree and replaces it with a list that is [quote, symbol]
def insert_quote(syntax_tree):
    #loop through all expressions in the tree
    for index, expr in enumerate(syntax_tree):
        #if the expression is a list, recursivley call insert_quote on the list
        if isinstance(expr, list):
            insert_quote(expr)
        #if the expression is the ' atom, replace it with (quote symbol)
        elif expr.data is "'":
            syntax_tree[index] = [Atom("quote"), syntax_tree[index+1]]
            syntax_tree.pop(index+1)
    
#evaluates a syntax tree
def eval(expr, env):
    #if the expression is a number atom, return the number
    if isinstance(expr, Atom) and expr.is_num:
        return expr
    #if the expression is not a number but still an atom,
    #return the expression defined by the symbol
    elif isinstance(expr, Atom):
        return env.get_expr(expr.data)

    #otherwise, the expression is a list
    #first check if the first expression in the list is one of the primitives
    #plus
    if expr[0].data is "+":
        #must be 2 arguements for the + function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function +")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) + eval(expr[2], env))

    #minus
    if expr[0].data is "-":
        #must be 2 arguements for the - function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function -")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) - eval(expr[2], env))

    #multiply
    if expr[0].data is "*":
        #must be 2 arguements for the * function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function *")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) * eval(expr[2], env))

    #divide
    if expr[0].data is "/":
        #must be 2 arguements for the / function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function /")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) // eval(expr[2], env))

    #define binds a symbol to an expression
    if expr[0].data == "define":
        if expr[1].data in Primitives:
            raise SyntaxError("Cant define a primitive")
        #must be 2 arguements for the define function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function define")
        env.add_symbol(expr[1].data, eval(expr[2], env))

        return None

    #eq? checks if 2 things are equal
    if expr[0].data == "eq?":
        #must be 2 arugements for eq? function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function eq?")
        return expr[1] == expr[2]
    
    #quote returns the symbols passed in instead of evaluating them
    if expr[0].data == "quote":
        #must be 1 arguement for quote function
        if len(expr[1:]) is not 1:
            raise SyntaxError("Expected 1 arguements for function quote")
        return expr[1]

    #cons returns a list containing the 2 arguements
    if expr[0].data == "cons":
        #must be 2 arguements for cons function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function cons")
        l = list()
        l.append(eval(expr[1], env))
        l.append(eval(expr[2], env))
        return l
    
    #car function returns the first element in a list
    if expr[0].data == "car":
        #must be 1 arguement for car function
        if len(expr[1:]) is not 1:
            raise SyntaxError("Expected 1 arguement for function car")
        #arguemnt must be a list
        if not isinstance(expr[1], list):
            #if not a list, check if its a symbol
            if expr[1].is_str:
                #if it is, get the expression associated with the symbol
                #and check if that is a list
                if not isinstance(eval(expr[1], env), list):
                    raise SyntaxError("Expected arguement to be a list for function car")
                #if it is a list, continue with function
                expr[1] = eval(expr[1], env)
            else:
                raise SyntaxError("Expected arguement to be a list for function car")
        return eval(expr[1][0], env)

    #cdr functions returns a list of all but the first element in a list
    if expr[0].data == "cdr":
        #must be 1 arguement for cdr function
        if len(expr[1:]) is not 1:
            raise SyntaxError("Expected 1 arguement for function cdr")
        #arguemnt must be a list
        if not isinstance(expr[1], list):
            #if not a list, check if its a symbol
            if expr[1].is_str:
                #if it is, get the expression associated with the symbol
                #and check if that is a list
                if not isinstance(eval(expr[1], env), list):
                    raise SyntaxError("Expected arguement to be a list for function cdr")
                #if it is a list, continue with function
                expr[1] = eval(expr[1], env)
            else:
                raise SyntaxError("Expected arguement to be a list for function cdr")
        return eval(expr[1], env)[1:]

    #atom? function returns true if the arguement is an atom
    if expr[0].data == "atom?":
        #must be 1 arguement for atom? function
        if len(expr[1:]) is not 1:
            raise SyntaxError("Expected 1 arguement for function atom?")
        return isinstance(expr[1], Atom)


    #if nothing else gets run, return the expression
    return expr

def main():
    #repl
    env = Environment()
    while True:
        str = input()
        toke_str = tokenize(str)
        syntax_tree = parse(toke_str)
        #insert_quote(syntax_tree)
        out = eval(syntax_tree, env)
        if out is not None:
            #need to check is return value is is a list
            #if it is, need to recursivley turn the list into a symbol instead of returning a list
            print(eval(syntax_tree, env))

main()
