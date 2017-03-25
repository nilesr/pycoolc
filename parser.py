import sys
sys.path.append(".")
import lexer
def term(t_type, literal = False):
    global tokens_ptr, tokens
    this_token = tokens[tokens_ptr]
    tokens_ptr += 1
    print("attempting to match '" + str(literal) + "' ("+t_type+") to " + this_token.matched_string + " at position " + str(tokens_ptr - 1))
    if t_type != this_token.type:
        return False
    if not literal:
        return True
    return literal == this_token.matched_string

grammar = {
        "e": [
            [["nonterminal", "t"], ["terminal", ["mathbinop", "+"]], ["nonterminal", "e"]],
            [["nonterminal", "t"]],
        ],
        "t": [
            [["terminal", ["integer"]], ["terminal", ["mathbinop", "*"]], ["nonterminal", "t"]],
            [["terminal", ["integer"]]],
            [["terminal", ["parens", "("]], ["nonterminal", "e"], ["terminal", ["parens", ")"]]],
        ],
        "order": ["e", "t"]
}

def match_syms(syms):
    # return term(a) and term(b) and term(c)
    for sym in syms:
        if not match_sym(sym):
            return False
    return True

def match_sym(sym):
    if sym[0] == "terminal":
        return term(*(sym[1]))
    return match_nterm(sym[1])

def match_nterm(nterm):
    global tokens_ptr
    save = tokens_ptr
    for f in grammar[nterm]:
        tokens_ptr = save
        if match_syms(f):
            return True
    return False

tokens = lexer.lex("(10+1)*3")
tokens_ptr = 0
print(match_nterm("e"))
print(tokens_ptr)
