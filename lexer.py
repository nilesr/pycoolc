import sys
sys.path.append(".")
import nfa, string
digit = '+'.join("0123456789")
letter = '+'.join(string.ascii_letters) + "+_"
upper = '+'.join(string.ascii_uppercase)
lower = '+'.join(string.ascii_lowercase)
whitespace = " +\n+\f+\r+\t+\v"
any_char = digit + "+" + letter + "+" + whitespace
any_string = "("+any_char+")*"

integer = nfa.compile("(" + digit + ")*") # may not be negative because my "-?" at the beginning broke everything
integer.type = "integer"
identifier = nfa.compile("(" + letter + ")(" + letter + "+" + digit + ")*") # letter followed by any number of letters or digits
identifier.type = "identifier"
string = nfa.compile("(\"(" + any_string + ")\")+('("+any_string+")')")
string.type = "string"
# comment = nfa.compile("--(" + any_char + ")*\n") # BROKEN AF
# comment.type = "comment"
keyword = nfa.compile("+".join(["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", "then", "while", "case", "esac", "new", "of", "not", "true"]))
keyword.type = "keyword"
assign = nfa.compile("<-")
assign.type = "assign"
relop = nfa.compile("+".join(["<", "<=", ">", ">=", "=", "<>"]))
relop.type = "relop"
semicolon = nfa.compile(";")
semicolon.type = "semicolon"
whitespace_nfa = nfa.compile(whitespace)
whitespace_nfa.type = "whitespace_nfa"
parens = nfa.either(nfa.build_from_char("("), nfa.build_from_char(")"))
parens.type = "parens"


test_data = """
if x = y then
    x <- 10;
else
    x <- 20; -- comment
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

def lex(data):
    import subprocess
    process = subprocess.Popen(["gpp", "+c", "--", "\\n"], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    data = process.communicate(input=data.encode("utf-8"))[0].decode("utf-8")
    priority_order = [whitespace_nfa, parens, semicolon, keyword, assign, relop, integer, string, identifier]
    done = []
    data_ptr = 0
    while data_ptr < len(data):
        one_matched = False
        for regex in priority_order:
            data_end = len(data)
            while data_end - data_ptr > 0:
                considering = data[data_ptr:data_end]
                #print("Considering " + considering.replace("\n", "\\n"))
                #print("matching '" + considering + "' against regex '" + regex.orig + "'")
                if nfa.match(regex, considering):
                    #print("Matched " + considering)
                    data_ptr += len(considering)
                    t = token()
                    t.matched_string = considering
                    t.type = regex.type
                    done.append(t)
                    this_regex_matched = True
                    one_matched = True
                    break
                data_end -= 1
        if not one_matched:
            print("Nothing matched '" + considering + "', bailing out")
            return []
    return done
for tkn in lex(test_data):
    if tkn.type != "whitespace_nfa": print("token was '" + tkn.matched_string + "' of type " + tkn.type)
