# Thompson's contstruction
# Johnathan Joyce


def shunt(infix):
    """The Shunting yard algorithm - infix to postfix"""
    
    
    # special characters precedence
    specials = { '*': 50, '.':40, '|':30}
    
    pofix = ""
    
    # operator stack
    stack = ""
    
    for c in infix:
        if c == '(':
            stack = stack + c
            # if open bracket push to stack, if closing pop and push output until open bracket
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        # if operator, push to sstack after popping lower or equal precedence
        # operators from top of stack into output
        elif c in specials:
            while stack and specials.get(c,0) <= specials.get(stack[-1], 0):
                 pofix, stack = pofix + stack [-1], stack[:-1]
            stack = stack + c
                    
        # regular characters are push immediately to the output
        else: pofix = pofix + c
    
    # pop all remaining operators from stack to output
    while stack: 
        pofix, stack = pofix + stack[-1], stack[:-1]
        
    
     # return postfix regex
    return pofix 
        
        
    
        

class state:
    label = None
    edge1 = None
    edge2 = None


class nfa:
    initial = None
    accept = None

   
    
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    nfastack = []

    for c in pofix:
        if c == '.':
            # pop two nfa's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # connect first nfa's accept state to the second's initial
            nfa1.accept.edge1 = nfa2.initial
            # push nfa to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)  
        elif c == '|':
            # pop two nfa's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            initial = state()
            # create a new initial state, connect it to initial state
            # of the two nfa's popped from the stack
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # create a new accept state, connecting the accept states
            # of the two nfa's popped from the stack to the new state.
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        elif c == '*':
            # pop a single nfa from the stack.
            nfa1 = nfastack.pop()
            # create new initial and accept states
            initial = state()
            accept = state()
            # Join the new inital state to nfa1's inital state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to the new accept state and nfa1's intial state.
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        else:
            # create new initial and accept states
            accept = state()
            initial = state()
            # Join the inital state and the accept state using an arrow labelled c.
            initial.label = c
            initial.edge1 = accept
            # push new nfa to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
            
    return nfastack.pop()

print(compile("ab.cd.|"))
print(compile("aa.*"))

def followes(state):
    
     #create a new set, with state as its only member
     states = set()
     states.add(state)
     
     
     # check if the state has arrows labelled
     if state.label is None:
         # check if edge 1 is a state
         if state.edge1 is not None:           
             # if there's an edge1, follow it
             states |= followes(state.edge1)
         if state.edge2 is not None:
         # if theres an edge2, follow it.
             states |= followes(state.edge2)
     return states

         

def match(infix, string):
    
    # matches string to infix regex
    
    # shunt and compile the regular expression.
    postfix = shunt(infix)
    nfa = compile(postfix)
    
    
    # the current set of states and the next set of states
    current = set()
    next = set()
    
    # add the initial state to the current set.
    current |= followes(nfa.initial)
    
    for s in string:
        # loop through the current set of states.
        for c in current:
            # check if state is labelled s
            if c.label == s:
                # add edge1 state to next set
                next |= followes(c.edge1)
                
        # set current to next, and clear out next
        current = next
        next = set()
        # commented test for nfa.accept returning correct values
        #print (nfa.accept in current)
    return (nfa.accept in current)
            
        
    
    
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print (match(i, s), i, s)
