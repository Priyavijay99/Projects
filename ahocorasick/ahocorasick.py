from collections import defaultdict
import pdb
from visual_automata.fa.dfa import VisualDFA
from automata.fa.dfa import DFA
from enum import Enum

# Enum is a type object to store consequent numerical values for the static values like a,t,g,c
class Input(Enum):
    a = 0
    t = 1
    g = 2
    c = 3
    n = 4

# AhoCorasick class implementation to build trie tree using BFS algorithm
class AhoCorasick:
    # Constructor method to initialize the variables needed while creating the object
    def __init__(self, words):
        '''
        input               - words (list of words by which the turing machine will be generated)
        self.max_states     - to store maximum number of states which is sum of lenghts of all input words
        self.max_characters - number of all possible inputs as text(a,t,g,c,n here)
        self.out            - to find end state and its corresponding word
        self.fail           - to find fail state of all the available states
        self.goto           - defines the structure of automata, a flow of all states for all inputs
        self.states         - set of all states in BFS(Breadth First Search) order
        self.input_symbols  - list of all possible inputs as text(a,t,g,c,n here)
        self.final_states   - set of states where complete word has been formed
        self.current_state  - current position/state of automata at any point of time(even at end)
        self.outputfn       - dict to store which word ends at which end state
        self.words          - input list of words
        self.states_count   - create automata and store total number of states and not maximum
        '''
        self.max_states = sum([len(word) for word in words])
        self.max_characters = 5
        self.out = [0]*(self.max_states+1)
        self.fail = [-1]*(self.max_states+1)
        self.goto = {x:[-1]*self.max_characters for x in range(self.max_states+1)}
        self.states = set()
        self.input_symbols = {'a','t','g','c', 'n'}
        self.initial_state = 0
        self.final_states = set()
        self.current_state = 0
        self.outputfn = {}
        for i in range(len(words)):
            words[i] = words[i].lower()
        self.words = words
        # pdb.set_trace()
        self.states_count = self.__build_matching_machine()

    def __build_matching_machine(self):
        '''
        method to build automata
        '''
        k = len(self.words)
        states = 1
        # states - number of states
        # states is 1 as current_state is 0 initially
        for i in range(k):
            # loop through the list of words..
            word = self.words[i]
            current_state = 0
            # for all the words, current_state starts with 0
            for character in word:
                # loop through all chars in a word
                ch = Input[character].value
                # ch - corresponding numeric value of character, from enum
                # creating a state and increment the state count only if it doesn't exists
                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1
                # updating current state 
                current_state = self.goto[current_state][ch]
            # updating out function to find endstate and its word
            self.out[current_state] |= (1<<i)
            # adding final states for the purpose of visualisation
            self.final_states.add(current_state)
        #updating self loop from 0th state to 0th state if it has -1
        for ch in Input:
            if self.goto[0][ch.value] == -1:
                self.goto[0][ch.value] = 0
        # Initializing queue - FIFO
        queue = []
        # Updating failstates for all elements 0th state to 0
        for ch in Input:
            ch = ch.value
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                # appending next state values from 0 to queue (BFS)
                queue.append(self.goto[0][ch])
        #initial state 0 added for visualisation purpose
        self.states.add(0)

        #loop to find fail states of all elements in BFS fashion
        while queue:
            # stating state from queue's first state and removing the state from queue
            state = queue.pop(0)
            #loop through all character for the taken particular state
            for ch in range(self.max_characters):
                if self.goto[state][ch] != -1:
                    # find fail over only if goto for the taken particular state is not -1
                    failure = self.fail[state]
                    # fail over of goto state will be same as fail over of cureent state
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]
                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure
                    # updating failure state also for out function for current take state
                    self.out[self.goto[state][ch]] |= self.out[failure]
                    # appending the child states of all current state as its failover is found(BFS way)
                    queue.append(self.goto[state][ch])
            # adding states for visualisation purpose
            self.states.add(state)
        return states

    def __find_next_state(self, current_state, next_input):
        # based on currentState and nextInput, finding nextState available in goto
        # if goto not available, return failover state
        answer = current_state
        ch = Input[next_input].value
        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]
  
        return self.goto[answer][ch]

    def search_words(self, text):
        # text - input text to find the occurrences
        text = text.lower()
        # initial state is 0
        self.current_state = 0
        # empty list of dict initialization
        result = defaultdict(list)

        for i in range(len(text)):
            # loop through text to find the matches/occurrences
            self.current_state = self.__find_next_state(self.current_state, text[i])

            # goto next loop if currentState is not an endState. ie. if out[state]==0
            if self.out[self.current_state] == 0: continue
            
            #if current state is endState, then loop through list of words to find the ending word in current state
            for j in range(len(self.words)):
                if (self.out[self.current_state] & (1<<j)) > 0:
                    word = self.words[j]
                    # initializing output function just for print purpose
                    if self.current_state in self.outputfn.keys() and word not in self.outputfn[self.current_state]:
                        self.outputfn[self.current_state].append(word)
                    else:
                        self.outputfn[self.current_state] = [word]
                    # adding word and its start occurrence to result object
                    result[word].append(i-len(word)+1)
  
        return result

    def createTransitions(self):
        '''
        creating transitions just for visualization purpose.
        '''
        self.transitions = {}
        for state in self.states:
            self.transitions[str(state)] = {}
            for input in self.input_symbols:
                # skipping n input as it always lead to failover state
                if input == 'n':
                    continue
                self.transitions[str(state)][str(input)] = str(self.__find_next_state(state, input))

if __name__ == "__main__":
    #input list of words to process automata
    words = ["at", "gc", "tata", "cat"]
    #creating object of class
    aho_chorasick = AhoCorasick(words)
    #reading file for input text
    with open('g1.fasta', 'r+') as f:
        text = f.readline()
    #search_words to find matches of all words & store it in result
    result = aho_chorasick.search_words(text)
  
    # Print the result
    print(f"Current state: {aho_chorasick.current_state}")
    allPos = {y:x for x in result for y in result[x]}
    for pos in sorted(allPos):
        print(f'{pos+1},["{allPos[pos]}"]', end=';')
    # cnt = {}
    # for word in result:
    #     if len(result[word]) not in cnt.keys():
    #         cnt[len(result[word])] = []
    #     cnt[len(result[word])].append(word)
    # print("\n\n cnt:", cnt)

    print(f"Output function:\n{aho_chorasick.outputfn}")
    pdb.set_trace()
    transitions = aho_chorasick.createTransitions()
    # pdb.set_trace()
    str_states = {str(x) for x in aho_chorasick.states}
    # str_inputs = {str(x) for x in aho_chorasick.input_symbols}
    str_final = {str(x) for x in aho_chorasick.final_states}
    
    dfa = VisualDFA(
    states=str_states,
    input_symbols=aho_chorasick.input_symbols-{'n'},
    transitions=aho_chorasick.transitions,
    initial_state=str(aho_chorasick.initial_state),
    final_states=str_final,
    )
    
    # dia = dfa.show_diagram()
    # minimal_dfa = VisualDFA.minify(dfa)
    dia = dfa.show_diagram()
    print(dia)
    dia.view()
    