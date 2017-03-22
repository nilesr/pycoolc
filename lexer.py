import sys
sys.path.append(".")
import nfa, string
digit = '+'.join("0123456789")
letter = '+'.join(string.ascii_letters) + "+_"
upper = '+'.join(string.ascii_uppercase)
lower = '+'.join(string.ascii_lowercase)
any_char = digit + "+" + letter
whitespace = " +\n+\f+\r+\t+\v"

integer = nfa.compile("(" + digit + ")*")
identifier = nfa.compile("(" + letter + ")(" + any_char + ")*") # letter followed by any number of letters or digits
string = nfa.compile("(\"(" + any_char + ")*\")" + "('("+any_char+")*')")
comment = nfa.compile("--(" + any_char + ")*")
keyword = nfa.compile("+".join(["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", "then", "while", "case", "esac", "new", "of", "not", "true"]))
