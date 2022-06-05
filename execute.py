from dfa import DFA
from dfa import symmetric_difference
from learner import Teacher, learn

def menu():
    transitions_dic={}
    transition_dic={}
    print(100*'-')
    print('Welcome(The states are numbers)')
    print('')
    Q=input('Please put the states(separate by comas) of the dfa that recognizes the unkown lenguajes: ').split(',')
    q0=input('Please put the initial states: ')
    F=input('Please put the final states(separate by comas): ')
    print('Please first put the state and the transition funtion asociated, when finished put Break(in the states and')
    print('for break the loop)')
    state=None
    transition_funtion_0=None
    transition_funtion_1=None
    while state!='Break': 
        state=input('Please put the state: ')
        if state in Q:
            transition_funtion_0=input('Please put the state to which the state already entered passes when reading 0:')
            transition_funtion_1=input('Please put the state to which the state already entered passes when reading 1:')
            transition_dic['0']=transition_funtion_0
            transition_dic['1']=transition_funtion_1
            transitions_dic[state]=transition_dic
            transition_dic={}
        if state not in Q and state!='Break':
            print('Error, you enter a a non existent state, retry')
    dfa=DFA(Q,q0,F,transitions_dic)
    teacher = Teacher(dfa)
    result=learn(teacher)
    if symmetric_difference(result,dfa)==None:
        print('The machine found and learn the next regular lenguajes ',result.__dict__,symmetric_difference(result,dfa))
        print('Thanks')
        menu()
        return ''
menu()
