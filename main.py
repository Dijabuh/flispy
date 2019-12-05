import curses
from Atom import Atom
from Env import Environment
import Eval as ev
import Parser as par

def main():
    #repl
    env = Environment()
    while True:
        str = input()
        if str == "!quit":
            print("Quitting lisp interpreter")
            break

        if len(str) >= 5 and str[0:5] == "!load":
            print("loading file")
            filename = str[6:]
            with open(filename) as f:
                for line in f:
                    ev.eval(par.parse(par.tokenize(line)), env)

        else:
            toke_str = par.tokenize(str)
            syntax_tree = par.parse(toke_str)
            #insert_quote(syntax_tree)
            out = ev.eval(syntax_tree, env)
            if out is not None:
                #need to check is return value is is a list
                #if it is, need to recursivley turn the list into a symbol instead of returning a list
                print(out)

main()
