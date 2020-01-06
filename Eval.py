from Env import Environment
from Atom import Atom
import Proc

#tuple represtinig all the primitives in this lisp
Primitives = ("+", "-", "*", "/",
              "eq?", "quote", "cons",
              "car", "cdr", "atom?",
              "define", "lambda", "cond")

#evaluates a syntax tree
def eval(expr, env):
    #if the expression is a number atom, return the number
    if isinstance(expr, Atom) and expr.is_num:
        return expr
    #if the expression is not a number but still an atom,
    #return the expression defined by the symbol
    elif isinstance(expr, Atom):
        return env.get_expr(expr.data)
    
    if isinstance(expr, list) and len(expr) is 0:
        return expr

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
    elif expr[0].data is "-":
        #must be 2 arguements for the - function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function -")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) - eval(expr[2], env))

    #multiply
    elif expr[0].data is "*":
        #must be 2 arguements for the * function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function *")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) * eval(expr[2], env))

    #divide
    elif expr[0].data is "/":
        #must be 2 arguements for the / function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function /")
        #return the sum of the 2 arguements
        return Atom(eval(expr[1], env) // eval(expr[2], env))

    #define binds a symbol to an expression
    elif expr[0].data == "define":
        if expr[1].data in Primitives:
            raise SyntaxError("Cant define a primitive")
        #must be 2 arguements for the define function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function define")
        env.add_symbol(expr[1].data, eval(expr[2], env))

        return None

    #eq? checks if 2 things are equal
    elif expr[0].data == "eq?":
        #must be 2 arugements for eq? function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function eq?")
        return eval(expr[1], env) == eval(expr[2], env)
    
    #quote returns the symbols passed in instead of evaluating them
    elif expr[0].data == "quote":
        #must be 1 arguement for quote function
        if len(expr[1:]) is not 1:
            raise SyntaxError("Expected 1 arguements for function quote")
        return expr[1]

    #cons returns a list containing the 2 arguements
    elif expr[0].data == "cons":
        #must be 2 arguements for cons function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function cons")
        l = list()
        l.append(eval(expr[1], env))
        l.append(eval(expr[2], env))
        return l
    
    #car function returns the first element in a list
    elif expr[0].data == "car":
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
    elif expr[0].data == "cdr":
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
    elif expr[0].data == "atom?":
        #must be 1 arguement for atom? function
        if len(expr[1:]) is not 1:
            raise SyntaxError("Expected 1 arguement for function atom?")
        return isinstance(expr[1], Atom)

    #lambda function creates a user defined function
    elif expr[0].data == "lambda":
        #must be 2 arguements for lambda function
        if len(expr[1:]) is not 2:
            raise SyntaxError("Expected 2 arguements for function lambda")

        #both arguements must be lists
        if not isinstance(expr[1], list):
            raise SyntaxError("Expected arguements for lambda definition to be a list")
        if not isinstance(expr[2], list):
            raise SyntaxError("Expected body for lambda definition to be a list")

        proc = Proc.Procedure(env, expr[2], expr[1])
        return proc

    #cond function is a block of if/then/else statements
    elif expr[0].data == "cond":
        for l in expr[1:]:
            if not isinstance(l, list):
                raise SyntaxError("All arguements of cond must be lists")
            if len(l) is not 2:
                raise SyntaxError("Each cond block must have 2 arguements")
            if not isinstance(l[0], list) and l[0].data == "else":
                #if it is else, eval the second part of l then finish going through cond loop
                return eval(l[1], env)
            else:
                ##if it isnt, check if the eval arguement 1 is true
                #if it is, run the eval arguement 2 then break
                if eval(l[0], env) is True:
                    return eval(l[1], env)
        return None

    #perform function call if none of the primitives were called
    elif expr[0].data in env.env and isinstance(eval(expr[0], env), Proc.Procedure):
        return eval(expr[0], env).eval_proc(expr[1:])

    #if nothing else gets run, return the expression
    return expr

