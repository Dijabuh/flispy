import copy

#class to represent a lisp environment
class Environment():
    def __init__(self, upper_env = None):
        self.env = dict()
        self.upper_env = upper_env
        #if an environemnt was passed in, copy its environment to the new one
        #used for procedure calls
        if upper_env is not None:
            self.env = copy.deepcopy(upper_env.env)

    #binds a symbol to an expression
    def add_symbol(self, symbol, expr):
        self.env[symbol] = expr

    #retreives the expression from a given symbol
    def get_expr(self, symbol):
        if symbol in self.env:
            return self.env[symbol]
        elif self.upper_env is not None:
            return self.upper_env.get_expr(symbol)
        else:
            raise SyntaxError("Symbol not defined")
