from  automata.fa.dfa import DFA
import numpy as np

#We implement the machine learning of regular sets for languages of binary only

def aux_question2(k): #This is a auxiliar funtion for the question 2
    if k==1:
        return ['','0','1']
    elif k==0:
        return ['']
    else:
        init=['','0','1']
        k=k-1
        maxim=None
        for i in range(2**(k-1)):
            maxim=len(max(init))
            for j in init:
                if len(j)==maxim:
                    init.append(j+'0')
                    init.append(j+'1')
    return init
            
def question1(dfa, input_symbols):#O(n) time
    #This is the first question of the teacher ¿Is a str w membership of unkown automata? (Use this with the unkown automata)
    #Can use for read a input o a dfa
    if dfa.accepts_input(input_symbols):
        return True
    else:
        return False

def question2(dfa1, dfa2):#
    #This is the second question of the teacher ¿Is a conjecture automata equal to the unkown automata?
    C = dfa1.symmetric_difference(dfa2,minify=True)#
    n_states=len(C._compute_reachable_states())
    aux=None
    if C.isempty()==True:
        return True #Return True because the 2 dfa are equivalent
    else:
        #From the "Tarea 4" we have the next lema(if you want the demostration read the document) 
        #Sea C un aut ́omata finito determinista con p estados, tal que L(C) ̸= φ. Entonces L(C) acepta al menos una cadena w de longitud menor o
        #igual a p −1.
       aux=aux_question2(n_states+1)
       for i in aux:
           if question1(C,i)==True:
               return i #Return the counterexample
           
#def prefixed_closed(S):
    #rows=['']#Elements of (S U S concatenate A)
    #columns=['']#Elementos of E
    #aux=[]
    #for i in S:
        #aux.append()
        
def mapping_funtion(dfa,u):
    result=question1(dfa,u)
    if result==True:
        return 1
    if result==False:
        return 0

def search_key(value,dic):
    for i in dic:
        if dic[i]==value:
            return i
    return False

def aux_closed(matrix,rows,columns,S_concatenate_A,S,dicrows,s,a):
    candidate=matrix[search_key(s+a,dicrows)].tolist()
    row_i=None
    for i in S:
         row_i=matrix[search_key(i,dicrows)].tolist()
         if row_i==candidate:
             return False
    return True
       
def closed(matrix,rows,columns,S_concatenate_A,S,dicrows):
    validate=[]
    t=None
    s=None
    row_t=None
    row_s=None
    candidate=None
    new_S=None
    for i in range(len(S_concatenate_A)):
        for j in range(len(S)):
            t=S_concatenate_A[i]
            s=S[j]
            row_t=matrix[search_key(t,dicrows)].tolist()
            row_s=matrix[search_key(s,dicrows)].tolist()
            if row_t==row_s and row_t!=False and search_key(t,dicrows)!=False and search_key(t,dicrows)!=False :
                validate.append(True) 
    if len(validate)==len(S_concatenate_A):
        return None
    else:
        for i in S:
            for k in ['0','1']:
                if aux_closed(matrix,rows,columns,S_concatenate_A,S,dicrows,i,k)==True:
                    return i+k
                    
def consisted(matrix,S,dicrows,E,dfa):
    row_i=None
    row_j=None
    news_E=None
    for i in S:
        for j in S:
            row_i=matrix[search_key(i,dicrows)].tolist()
            row_j=matrix[search_key(j,dicrows)].tolist()
            if row_i==row_j and search_key(i,dicrows)!=False and search_key(j,dicrows)!=False:
                for k in ["0","1"]:
                    row_i=matrix[search_key(i+k,dicrows)].tolist()
                    row_j=matrix[search_key(j+k,dicrows)].tolist()
                    if row_i!=row_j:
                        for m in ["0","1"]:
                            for n in E:
                                for w in S:
                                    for x in S:
                                        if mapping_funtion(dfa,str(w)+str(m)+str(n))!=mapping_funtion(dfa,str(x)+str(m)+str(n)):
                                            news_E=m+n
                        return news_E
    return news_E
                
def aux_observation_table(S,A):
    S_concatenate_A=[]
    for i in S:
        for j in A:
            S_concatenate_A.append(i+j)
    S_union_S_concatenateA=S_concatenate_A+S
    return S_union_S_concatenateA,S_concatenate_A

def final_states(matrix,S,dicrows):
    aux1=[]
    aux2=None
    for i in S:
        if mapping_funtion(dfa,i)==1:
            if search_key(i,dicrows)!= False:
                aux2=matrix[search_key(i,dicrows)].tolist()
                aux1.append(str(aux2))
    return set(aux1)
            
def transition_funtion(matrix,S,rowsdic):
    transitions={}
    aux1={}
    aux2={}
    aux3=None
    for i in S:
        aux1=matrix[search_key(i,rowsdic)].tolist()#row s
        if search_key(i+"0",rowsdic)!= False:
            aux2["0"]=str(matrix[search_key(i+"0",rowsdic)].tolist())#first
        elif search_key(i+"0",rowsdic)==False:
            aux2['0']='qrec'
        if search_key(i+"1",rowsdic) != False:
            aux2["1"]=str(matrix[search_key(i+"1",rowsdic)].tolist())#second
        elif search_key(i+"1",rowsdic)==False:
            aux2['0']='qrec'   
        transitions[str(aux1)]=aux2
        
    aux2={'0':'qrec','1':'qrec'}
    transitions['qrec']=aux2
    return transitions

def states(matrix,S,rowsdic):
    states=[]
    epsilon=None
    for i in S:
        if i=='':
            if search_key(i,rowsdic)!= False:
                epsilon=str(matrix[search_key(i,rowsdic)].tolist())
        if search_key(i,rowsdic)!= False:
            states.append(str(matrix[search_key(i,rowsdic)].tolist()))
    return set(states+['qrec']),epsilon
        
def dfa_of_a_table(matrix,S,rowsdic):
    dfa = DFA(
    states=states(matrix,S,rowsdic)[0],
    input_symbols={"0", "1"},
    transitions=transition_funtion(matrix,S,rowsdic),
    initial_state=states(matrix,S,rowsdic)[1],
    final_states=final_states(matrix,S,rowsdic),
)
    return dfa
def prefix_counterexample(i):
    prefix=['']
    for j in range(len(i)):
        prefix.append(i[0:j])
    return prefix
    
def learning(dfa):
    S=['']#We initialize S
    E=['']#We initialize E
    stop=False
    newE=None
    newS=None
    newrow=None
    newcolumn=None
    S_union_S_concatenateA,S_concatenate_A=aux_observation_table(S,['0','1'])
    rows=S_union_S_concatenateA#Elements of (S U S concatenate A)
    dicrows=dict(enumerate(rows))
    columns=E#Elements of E
    diccolumns=dict(enumerate(columns))
    matrix=np.zeros((len(rows),len(columns)))#Initial observation table
    hypotesis=None
    prefix=None
    count=0
    for i in range(len(rows)):
        for j in range(len(columns)):
                dicrows[i]=rows[i]
                matrix[i][j]=mapping_funtion(dfa,rows[i]+columns[j])#mapping funtion evaluate 
    while stop==False:
        if  closed(matrix,rows,columns,S_concatenate_A,S,dicrows)!=None:
            newS=closed(matrix,rows,columns,S_concatenate_A,S,dicrows)
            S.append(newS)
            S_union_S_concatenateA,S_concatenate_A=aux_observation_table(S,['0','1'])
            dicrows[len(dicrows)]=newS
            newrow=np.zeros(((1,np.shape(matrix)[1])))
            for i in range(len(columns)):
                newrow[0][i]=mapping_funtion(dfa,str(newS)+columns[i])
            matrix=np.concatenate((matrix,newrow))
        if consisted(matrix,S,dicrows,E,dfa)!=None:
            newE=consisted(matrix,S,dicrows,E,dfa)
            E.append(newE)
            diccolumns[len(diccolumns)]=newE
            newcolumn=np.zeros((np.shape(matrix)[0],1))
            for i in range(len(rows)):
                newcolumn[i][0]=mapping_funtion(dfa,rows[i]+str(newE))
            matrix=np.concatenate((matrix,newcolumn),axis=1)
        else:
            hypotesis=dfa_of_a_table(matrix,S,dicrows)
            if question2(dfa,hypotesis)==True:
                return hypotesis
            else: 
                prefix=question2(dfa,hypotesis)
                newS=prefix_counterexample(prefix)
                for i in newS:
                    if i not in S:
                        S.append(i)
                for i in newS:
                    if i not in dicrows.values():
                        dicrows[len(dicrows)]=i
                newrow=np.zeros(((len(newS),np.shape(matrix)[1])))
                for i in range(len(columns)):
                    for j in range(len(newS)):
                        newrow[j][i]=mapping_funtion(dfa,newS[j]+columns[i])
                matrix=np.concatenate((matrix,newrow))
        count+=1
        if count==10:
            return dfa.show_diagram(path='./dfa1.png')
    return None

def cicle_table(dfa):
    pass


dfa = DFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5"},
    input_symbols={"0", "1"},
    transitions={
        "q0": {"0": "q2", "1": "q1"},
        "q1": {"0": "q2", "1": "q1"},
        "q2": {"0": "q4", "1": "q3"},
        "q3": {"0": "q4", "1": "q3"},
        "q4": {"0": "q5", "1": "q4"},
        "q5": {"0": "q5", "1": "q5"},
    },
    initial_state="q0",
    final_states={"q5"},
)

print(learning(dfa))

                