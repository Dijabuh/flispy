from Atom import Atom

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
