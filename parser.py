import sys
sys.path.append(".")
import lexer

# I know I really shouldn't be using a class for this but tokens and tokens_ptr were global variables and I didn't feel like rewriting the whole thing to not use global variables, so now they're technically instance variables

class parser():
    def __init__(self, grammar):
        self.grammar = grammar
    def parse(self, inp):
        print("Parsing input " + inp)
        self.tokens = lexer.lex(inp)
        self.tokens = [t for t in self.tokens if not t.type == "whitespace_nfa"]
        self.tokens_ptr = 0
        return self.match_nterm(self.grammar["start"])

    def term(self, t_type, literal = False):
        this_token = self.tokens[self.tokens_ptr]
        self.tokens_ptr += 1
        #print("attempting to match '" + str(literal) + "' ("+t_type+") to " + this_token.matched_string + " at position " + str(self.tokens_ptr - 1))
        if t_type != this_token.type:
            return False
        if not literal:
            return True
        return literal == this_token.matched_string

    def match_syms(self, syms):
        # return term(a) and term(b) and term(c)
        for sym in syms:
            if not self.match_sym(sym):
                return False
        return True

    def match_sym(self, sym):
        if sym[0] == "terminal":
            return self.term(*(sym[1]))
        return self.match_nterm(sym[1])

    def match_nterm(self, nterm):
        save = self.tokens_ptr
        for f in grammar[nterm]:
            self.tokens_ptr = save
            if self.match_syms(f):
                print("Matched term " + str([k[1] for k in f]))
                return True
        return False

# Our productions for this context-free grammar
# E -> T + E
#    | T
# T -> int * T
#    | int
#    | ( E )
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
        "start": "e",
}

p = parser(grammar)
print(p.parse("(10 + (99 * 44))*3 + 1231"))


import sys
sys.exit(0)



grammar = {
        "program": [
           [["nonterminal", "class"], ["terminal", ["semicolon"]], ["nonterminal", "program"]],
           [["nonterminal", "class"]],
        ],
        "class": [
            [
                ["terminal", ["keyword", "class"]],
                ["terminal", ["identifier"]],
                ["terminal", ["keyword", "inherits"]],
                ["terminal", ["identifier"]],
                ["terminal", ["braces", "{"]],
                ["nonterminal", "feature;+"],
                ["terminal", ["braces", "}"]]
            ],
            [
                ["terminal", ["keyword", "class"]],
                ["terminal", ["identifier"]],
                ["terminal", ["braces", "{"]],
                ["nonterminal", "feature;+"],
                ["terminal", ["braces", "}"]]
            ]
        ],
        "feature;+": [
            [
                ["terminal", ["semicolon"]]
            ],
            [
                ["nonterminal", "feature"],
                ["terminal", ["semicolon"]],
                ["nonterminal", ["feature;+"]]
            ]
        ],
        "feature": [
            [
                ["terminal", ["identifier"]],
                ["terminal", ["parens", "("]],
                ["terminal", ["parens", ")"]],
                ["terminal", ["colon"]],
                ["terminal", ["identifier"]],
                ["terminal", ["braces", "{"]],
                ["nonterminal", "expr"],
                ["terminal", ["braces", "}"]]
            ],
            [
                ["terminal", ["identifier"]],
                ["terminal", ["parens", "("]],
                ["nonterminal", "formal,+"],
                ["terminal", ["parens", ")"]],
                ["terminal", ["colon"]],
                ["terminal", ["identifier"]],
                ["terminal", ["braces", "{"]],
                ["nonterminal", "expr"],
                ["terminal", ["braces", "}"]]
            ],
            [
                ["terminal", ["identifier"]],
                ["terminal", ["colon"]],
                ["terminal", ["identifier"]],
                ["terminal", ["assign"]],
                ["nonterminal", "expr"],
            ],
            [
                ["terminal", ["identifier"]],
                ["terminal", ["colon"]],
                ["terminal", ["identifier"]],
            ]
        ],
        "formal": [
            [
                ["terminal", ["identifier"]],
                ["terminal", ["colon"]],
                ["terminal", ["identifier"]],
            ]
        ],
        "formal,+": [
            [
                ["nonterminal", "formal"],
                ["terminal", ["comma"]],
                ["nonterminal", "formal,+"]
            ],
            [
                ["nonterminal", "formal"]
            ]
        ]
}
