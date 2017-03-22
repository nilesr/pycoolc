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

integer = nfa.compile("-?(" + digit + ")*") # may or may not be negative
identifier = nfa.compile("(" + letter + ")(" + letter + "+" + digit + ")*") # letter followed by any number of letters or digits
string = nfa.compile("(\"(" + any_string + ")\")+('("+any_string+")')")
comment = nfa.compile("--(" + any_char + ")*")
keyword = nfa.compile("+".join(["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", "then", "while", "case", "esac", "new", "of", "not", "true"]))
assign = nfa.compile("<-")
relop = nfa.compile("+".join(["<", "<=", ">", ">=", "=", "<>"]))

# print("Integer's regex was " + integer.orig)
# print("string's regex was " + string.orig)
#nfa.pmap(identifier)
