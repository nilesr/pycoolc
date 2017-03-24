import random # only used for nfa id, which is only used by pmap
epsilon_literal = 'ε'
class field(): # a "field" has a list of nodes and a starting node, that's it
    def __init__(self):
        self.nodes = set()
        self.start = False
        self.orig = "not compiled"
# a node is either terminal (accepting) or not, and it has a list of possible moves. 
# the moves are usually indexed by a character, so my_nfa.moves['a'] will return another nfa
# ε is special because there can be more than one ε moves, and they don't consume a character of input
# so my_nfa.moves['ε'] will actually return a set of nodes
class nfa():
    def __init__(self):
        self.terminal = False
        self.moves = {'ε': set()}
        self.id = random.randrange(1000)
# makes a super simple field with a start node and a terminal node. The start node will move to the end node but only if it's fed the character we were passed.
# it puts them in a field and sets the start node of the field to the start node
def build_from_char(c):
    base = nfa()
    end = nfa()
    end.terminal = True
    base.moves[c] = end
    f = field()
    f.start = base
    f.nodes = set([base, end])
    return f
# this takes a field and allows that field to be repeated zero or more times.
#                _______________ε_______________
#               /                               \ 
#              /                                 v
# start -> (node) --ε--> (passed field) --ε--> (node) <- that one is terminal
#              ^             /
#               \_____ε_____/
# 
# 
def iterate(f):
    new_f = field()
    outer_start = nfa()
    outer_end = nfa()
    for node in f.nodes:
        if node.terminal:
            node.moves['ε'].add(outer_end)
            node.moves['ε'].add(outer_start)
            node.terminal = False
    for k in f.nodes:
        new_f.nodes.add(k)
    new_f.nodes.add(outer_start)
    new_f.nodes.add(outer_end)
    outer_end.terminal = True
    outer_start.moves['ε'] = set([f.start, outer_end])
    new_f.start = outer_start
    return new_f
# This allows either token in the language
#                .--ε--> (a) --ε--.
#               /                  \
# start -> (node)                 (end) <- that one is terminal
#               \                  /
#                `--ε--> (b) --ε--`
#  
def either(a, b):
    f = field()
    f.nodes = a.nodes
    for k in b.nodes:
        f.nodes.add(k)
    new_start = nfa()
    new_start.moves['ε'].add(a.start)
    new_start.moves['ε'].add(b.start)
    new_end = nfa()
    new_end.terminal = True
    for node in (a.nodes | b.nodes):
        if node.terminal:
            node.terminal = False
            node.moves['ε'].add(new_end)
    f.start = new_start
    f.nodes.add(new_start)
    f.nodes.add(new_end)
    return f
# returns a field with a then b
# start -> (a) --ε--> (b) <-- that one has terminal nodes
def concatenate(a, b):
    f = field()
    f.start = a.start
    for node in a.nodes:
        f.nodes.add(node)
        if node.terminal:
            node.terminal = False
            node.moves['ε'].add(b.start)
    for node in b.nodes:
        f.nodes.add(node)
    return f
# takes a set of nodes, returns a set of those nodes and all nodes connected to those nodes by epsilon moves
# uses an ignore list for its recursive calls so it won't loop infinitely
def epsilon_closure(s, ignore=False):
    new_s = set(s) # we can't modify the set we're iterating over or the program will explode, so we return a new set instead of modifying s
    if not ignore:
        ignore = new_s
    for state in s:
        for possible_move in state.moves['ε']: # for all possible ε moves in all the moves we're expanding over, recurse
            if possible_move in ignore:
                continue
            for m in epsilon_closure(set([possible_move]),(set([possible_move]) | ignore)):
                new_s.add(m)
    return new_s

# determines if a compiled regular expression matches a string
def match(f, inp):
    states = set([f.start])
    idx = 0
    while idx < len(inp):
        states = epsilon_closure(states) # expand into epsilon connected states
        new_states = set() # the states we will be in after we consume the input
        c = inp[idx] # the character we're taking in right now
        for state in states:
            for key, move in state.moves.items():
                if key == c:
                    new_states.add(move) # add this move to new_states if we could get there from one of our old states by consuming that exact character
        states = new_states; # prepare to do it all over again
        idx += 1
        if len(states) == 0: # if there are no states, we can't possibly end up at a terminal state so just stop reading
            return False
    # now we've consumed all the input. If any of the states we are in are accepting states, it matched, otherwise return false
    states = epsilon_closure(states) # expand into epsilon connected states
    for state in states:
        if state.terminal:
            return True
    return False


def list_to_field(l):
    if len(l) == 0: # this base case shouldn't be hit unless you have an empty regex or start your regex with a + or something
        # all it does is make a field with one terminal node in it
        f = field()
        n = nfa()
        n.terminal = True
        f.start = n
        f.nodes = set([n])
        return f
    # just maps concatenate over all the things in the list and returns the giant field at the end
    final = l[0]
    for k in l[1:]:
        final = concatenate(final, k)
    return final
def zero_or_one(f):
    f2 = field()
    f2.nodes = f.nodes
    f2.start = f.start
    n = nfa()
    n.terminal = True
    for k in f.nodes:
        if k.terminal:
            k.terminal = False
            k.moves['ε'].add(n)
    f2.nodes.add(n)
    f2.start.moves['ε'].add(n)
    return f2
def compile(regex):
    to_concat = [] # empty list of things to concatenate
    inparens = False # parenthesis parsing stuff
    for i in range(len(regex)):
        if inparens: # if we're in parenthesis
            if regex[i] == ")": # and we find a close parenthesis
                if inparens == 1: # and we're now at the same level we started at
                    to_concat.append(compile(subregex)) # compile the stuff that was in parenthesis and add it to the list
                    inparens = False # and we're no longer in parenthesis
                else:
                    inparens -= 1 # otherwise decrease parens level
            if regex[i] == "(": # increase parens level if we find a (
                inparens += 1
            subregex += regex[i] # add the character to the string we will compile when we reach the end of the highest set of parenthesis
        elif regex[i] == "(": # if we weren't in parens and we find a "(", enter parenthesis
            inparens = 1
            subregex = ""
            continue
        elif regex[i] == "*": # if we find a *, iterate the last thing on the stack, which might have been a subregex (and that's ok)
            to_concat[-1] = iterate(to_concat[-1])
        elif regex[i] == "+": # kind of a hack and gives + the highest possible operator precedence
            ret = either(list_to_field(to_concat), compile(regex[i+1:]))
            ret.orig = regex
            return ret
        elif regex[i] == "?": # COMPLETELY UNTESTED
            to_concat[-1] = zero_or_one(to_concat[-1])
        else: # if we just found a regular character, add it to the stuff to concatenate
            to_concat.append(build_from_char(regex[i]))
    ret = list_to_field(to_concat)
    ret.orig = regex
    return ret

def addr(node): # this used to be a hack that would print the memory address of the node starting with a _ so graphviz didn't split it at the end of the number
    return str(node.id)
def pmap(f): # prints out the passed field in a way that dot can compile to an svg
    print("digraph test {")
    for node in f.nodes:
        for char, move in node.moves.items():
            if char == 'ε':
                for m in move:
                    print(addr(node) + " -> " + addr(m) + " [label=epsilon]")
            else:
                print(addr(node) + " -> " + addr(move) + " [label="+char+"]")
        if node.terminal:
            print(addr(node) + " -> " + addr(node) + " [label=terminal]")
    print(addr(f.start) + " -> " + addr(f.start) + " [label=start]")
    print("}")


# DEBUG

# BAD CODE - WILL BREAK EVERYTHING
# a = build_from_char('a')
# b = build_from_char('b')
# full = concatenate(a, b)
# full2 = concatenate(iterate(a), b)
# The reason you can't do this is because concatenate is a destructive operation (unsets terminal and adds moves to previously terminal nodes on a)
# so iterate(a) in the definition of full2 will set all terminal nodes of a to the new terminal node of iterate, but there are no terminal nodes of a so you get a mess. It will actually continue being connected to b as part of full
# End bad code

# this works
# full = concatenate(build_from_char('a'), build_from_char('b'))
# full2 = concatenate(iterate(build_from_char('a')), build_from_char('b'))

# strings = ["aa", "ab", "ba", "bb", "aba", "aab", "aaab", "aaba", "b"]
# for s in strings:
    # print("String " + s + " " + ("matches" if match(full, s) else "does not match") + " pattern " + "ab")
# print()
# for s in strings:
    # print("String " + s + " " + ("matches" if match(full2, s) else "does not match") + " pattern " + "a*b")

#print(match(full2, "aab"))
#pmap(full2)
#pmap(zero_or_one(build_from_char("a")))

#pmap(compile("ab(c1+2d(e*f)d)*e"))
#pmap(either(build_from_char('a'), build_from_char('b')))
# x = compile("(1+0)*1")
# pmap(x)
# for s in ["101", "111110", "11001", "1", "0"]:
    # print(match(x, s))
# x = compile("a+b+c")
# pmap(x)
