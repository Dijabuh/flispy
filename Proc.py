from Atom import Atom
from Env import Environment
import Eval

#class to represent user defined procedures
class Procedure():
    #procedures are created with an environment, body of the procedurem and arguements
    def __init__(self, env, body, args):
        #the procedures environment has an upper_env of the passed environment
        self.env = env
        self.body = body
        self.args = args
        self.num_args = len(args)

    #evals procedure
    def eval_proc(self, args):
        if len(args) is not self.num_args:
            raise SyntaxError("Wrong number of arguements for procedure call")
        env = Environment(self.env)
        #add arguements to environment
        for i in range(self.num_args):
            val = Eval.eval(args[i], env)
            env.add_symbol(self.args[i].data, val)

        return Eval.eval(self.body, env)

