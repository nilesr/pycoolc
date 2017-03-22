import random
epsilon_literal = 'ε'
class field():
    def __init__(self):
        self.nodes = set()
        self.start = False
class nfa():
    def __init__(self):
        self.terminal = False
        self.moves = {'ε': set()}
        self.id = random.randrange(1000)

def build_from_char(c):
    base = nfa()
    end = nfa()
    end.terminal = True
    base.moves[c] = end
    f = field()
    f.start = base
    f.nodes = set([base, end])
    return f
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
    for node in union(a.nodes, b.nodes):
        if node.terminal:
            node.terminal = False
            node.moves['ε'].add(new_end)
    f.start = new_start
    f.nodes.add(new_start)
    f.nodes.add(new_end)
    return f
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

def union(a, b):
    r = set()
    for e in a:
        r.add(e)
    for e in b:
        r.add(e)
    return r

# def add_epsilon_moves(s): # needs to be redone from scratch
    # # new_s = set(s)
    # new_s = set()
    # for state in s:
        # new_s.add(state)
        # for possible_move in state.moves['ε']:
            # #new_s.add(possible_move)
            # #new_s = union(new_s, add_epsilon_moves(set([possible_move])))
            # for m in add_epsilon_moves(set([possible_move])):
                # new_s.add(m)
    # return new_s
def add_epsilon_moves(s, ignore=set()): # needs to be redone from scratch
    new_s = set(s)
    if len(ignore) == 0: ignore = new_s
    for state in s:
        # if state in ignore:
            # continue
        for possible_move in state.moves['ε']:
            if possible_move in ignore:
                continue
            for m in add_epsilon_moves(set([possible_move]), union([possible_move], ignore)):
                new_s.add(m)
    return new_s

def compute(f, inp):
    states = set([f.start])
    idx = 0
    while idx < len(inp):
        # print(states)
        states = add_epsilon_moves(states)
        # print(states)
        # print()
        new_states = set()
        c = inp[idx]
        for state in states:
            for key, move in state.moves.items():
                if key == c:
                    new_states.add(move)
        states = new_states;
        idx += 1
    for state in states:
        if state.terminal:
            return True
    return False

full = concatenate(build_from_char('a'), build_from_char('b'))
full2 = concatenate(iterate(build_from_char('a')), build_from_char('b'))


# strings = ["aa", "ab", "ba", "bb", "aba", "aab", "aaab", "aaba", "b"]
# for s in strings:
    # print("String " + s + " " + ("matches" if compute(full, s) else "does not match") + " pattern " + "ab")
# print()
# for s in strings:
    # print("String " + s + " " + ("matches" if compute(full2, s) else "does not match") + " pattern " + "a*b")

#print(compute(full2, "aab"))
def addr(node):
    #return str(node).split()[3].replace(">", "").replace("0x", "_")
    return str(node.id)
def pmap(f):
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
#pmap(full2)
#pmap(iterate(a))

def list_to_field(l):
    if len(l) == 0:
        f = field()
        n = nfa()
        n.terminal = True
        f.start = n
        f.nodes = set([n])
        return f
    final = l[0]
    for k in l[1:]:
        final = concatenate(final, k)
    return final
def build_from_regex(regex):
    to_concat = []

    inparens = False
    for i in range(len(regex)):
        if inparens:
            if regex[i] == ")":
                if inparens == 1:
                    to_concat.append(build_from_regex(subregex)) # FIX
                    inparens = False
                else:
                    inparens -= 1
            if regex[i] == "(":
                inparens += 1
            subregex += regex[i]
        elif regex[i] == "(":
            inparens = 1
            subregex = ""
            continue
        elif regex[i] == "*":
            to_concat[-1] = iterate(to_concat[-1])
        elif regex[i] == "+":
            return either(list_to_field(to_concat), build_from_regex(regex[i+1:])) # kind of a hack and gives + the highest possible operator precedence
        else:
            to_concat.append(build_from_char(regex[i]))
    return list_to_field(to_concat)
#pmap(build_from_regex("ab(c1+2d(e*f)d)*e"))
#pmap(either(build_from_char('a'), build_from_char('b')))
# x = build_from_regex("(1+0)*1")
# #pmap(x)
# for s in ["101", "111110", "11001", "1", "0"]:
    # print(compute(x, s))
x = build_from_regex("a+b+c")
pmap(x)
