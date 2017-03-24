import sys
sys.path.append(".")
import nfa, string
digit = '+'.join("0123456789")
letter = '+'.join(string.ascii_letters) + "+_"
upper = '+'.join(string.ascii_uppercase)
lower = '+'.join(string.ascii_lowercase)
whitespace_no_newline = " +\f+\r+\t+\v"
whitespace = whitespace_no_newline + "+\n"
any_char = digit + "+" + letter + "+" + whitespace
any_string = "("+any_char+")*"

integer = nfa.compile("-?(" + digit + ")(" + digit + ")*")
integer.type = "integer"
identifier = nfa.compile("(" + letter + ")(" + letter + "+" + digit + ")*") # letter followed by any number of letters or digits
identifier.type = "identifier"
string = nfa.compile("(\"(" + any_string + ")\")+('("+any_string+")')")
string.type = "string"
comment = nfa.compile("--(" + digit + "+" + letter + "+" + whitespace_no_newline + ")*\n") # Untested
comment.type = "comment"
keyword = nfa.compile("+".join(["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", "then", "while", "case", "esac", "new", "of", "not", "true"]))
keyword.type = "keyword"
assign = nfa.compile("<-")
assign.type = "assign"
relop = nfa.compile("+".join(["<", "<=", ">", ">=", "=", "<>", "!="]))
relop.type = "relop"
semicolon = nfa.compile(";")
semicolon.type = "semicolon"
whitespace_nfa = nfa.compile(whitespace)
whitespace_nfa.type = "whitespace_nfa"
parens = nfa.either(nfa.build_from_char("("), nfa.build_from_char(")"))
parens.type = "parens"
mathbinop = nfa.either(nfa.either(nfa.compile("-+/+%+^+|+&"), nfa.build_from_char("+")), nfa.build_from_char("*"))
mathbinop.type = "mathbinop"
mathunop = nfa.compile("~")
mathunop.type = "mathunop"
brace = nfa.compile("{+}")
brace.type = "brace"
bracket = nfa.compile("[+]")
bracket.type = "bracket"
unop = nfa.compile("!")
unop.type = "unop"


test_data = """
if x = y then
    x <- 10;
else
    x <- x - (y * -1); -- comment test
    print("string literal test");
fi
"""

#print(nfa.match(keyword, "if"))
#print(nfa.match(nfa.compile("if+and"), "if"))
#print(nfa.match(integer, "10"))
#nfa.pmap(nfa.compile("if+and"))
#sys.exit(0)

class token():
    def __init__(self):
        self.matched_string = ""
        self.type = False

# returns a list of tokens in the order they appeared in the input string
def lex(data):
    # import subprocess
    # process = subprocess.Popen(["gpp", "+c", "--", "\\n"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    # data = process.communicate(input=data.encode("utf-8"))[0].decode("utf-8")
    # whichever of these is the first to match a substring of the text is used to create the token
    priority_order = [whitespace_nfa, comment, integer, parens, bracket, brace, mathbinop, mathunop, unop, semicolon, keyword, assign, relop, string, identifier]
    done = []
    data_ptr = 0
    while data_ptr < len(data): # loop until we've read the whole input string
        one_matched = False
        # start by trying to match the whole rest of the input string, and chop one character off the end until there are no characters left. If none of those substrings matched, move on to the next regex in the priority order
        for regex in priority_order: # starting with the highest priority regex
            data_end = len(data) # MAXIMUM MUNCH - literally the largest lookahead possible
            this_regex_matched = False
            while data_end - data_ptr > 0:
                considering = data[data_ptr:data_end]
                if nfa.match(regex, considering): # If this regex matched the substring
                    data_ptr += len(considering) # add the length of what it matched to where we'll start reading the next token from
                    t = token() # construct a token and add it to the result list
                    t.matched_string = considering
                    t.type = regex.type
                    done.append(t)
                    one_matched = True # don't die
                    this_regex_matched = True
                    break
                data_end -= 1
            if this_regex_matched:
                break
        if not one_matched:
            print("Nothing matched '" + considering + "', bailing out") # if we encounter something that we can't parse, just die
            return []
    return done
# debug
for tkn in lex(test_data):
    if tkn.type != "whitespace_nfa": print("token was '" + tkn.matched_string.replace("\n", "\\n") + "' of type " + tkn.type)
