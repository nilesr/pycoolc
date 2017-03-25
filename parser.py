import sys
sys.path.append(".")
import lexer
grammar = {
        "e": [
            #[["nonterminal", "t"], ["terminal", ["mathbinop", "+"]], ["nonterminal", "e"]],
            [["nonterminal", "t"]],
        ],
        "t": [
            #[["terminal", ["integer"]], ["terminal", ["mathbinop", "*"]], ["nonterminal", "t"]],
            [["terminal", ["integer"]]],
            #[["terminal", ["parens", "("]], ["nonterminal", "e"], ["terminal", ["parens", ")"]]],
        ],
        "order": ["e", "t"]
}

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

compiled = {}
def build_test(): # I don't know how, I don't know why, and I don't know where, but this code has a race condition in it. It's late and I'll fix it later
    for x, y in grammar.items():
        if x == "order": continue
        built_outer = []
        for l in y:
            # l is line 6, 7, 10, 11, 12
            built = []
            for sym in l:
                if sym[0] == "terminal":
                    built.append(lambda: term(*sym[1]))
                else:
                    built.append(lambda: compiled[sym[1]]())
            def temp_inner(built):
                for f in built:
                    if not f():
                        return False
                return True
            built_outer.append(lambda: temp_inner(built))
        def temp():
            global tokens_ptr
            save = tokens_ptr
            for f in built_outer:
                tokens_ptr = save
                if not f():
                    return False
            return True
        compiled[x] = temp

tokens = lexer.lex("10")
tokens_ptr = 0
build_test()
print(compiled["e"]())
print(tokens_ptr)
"""
tokens = lexer.lex("(10+1)*3")
tokens_ptr = 0
def e1():
    return t() and term("mathbinop","+") and e()
def e2():
    return t()
def e():
    global tokens_ptr
    save = tokens_ptr
    for f in [e1, e2]:
        tokens_ptr = save
        if f():
            return True
    return False
def t1():
    return term("integer") and term("mathbinop", "*") and t()
def t2():
    return term("integer")
def t3():
    return term("parens", "(") and e() and term("parens", ")")
def t():
    global tokens_ptr
    save = tokens_ptr
    for f in [t1, t2, t3]:
        tokens_ptr = save
        if f():
            return True
    return False
print(e())
print(tokens_ptr)
"""
