#Owner: Nandan M Hegde
#Program to convert a PDA which accepts by empty stack to CFG

class PDA:
    def readn(self):
        n=int(input("Enter the number of productions: "))
        return n
    
    def readp(self):
        p=[]
        print("Enter the productions in the following format:")
        print("Enter e for epsilon and don't use e anywhere else")
        print("Enter z for Z0 and don't use z anywhere else")
        print("Make sure not to give any unnecessary state as accepting state, it might result in wrong output")
        print("If the production is delta(q,a,z)=(p,B) then enter it as follows:")
        print("q a z p B")
        print("where q is the current state")
        print("a is the current symbol")
        print("z is the top of stack")
        print("p is the next state")
        print("B is the top of stack with currently pushed symbol")

        for i in range (n):
            temp=[num for num in input().split()]
            p.append(temp)
        return p

    #Seperating input states

    def seperate_ip_state(self,n,p):
        states1=[]
        states=[]
        for i in range(n):
            states1.append(p[i][0])
            states1.append(p[i][3])

        states=set(states1)
        states=list(states)
        if states[0]!=states1[0]:
            states.reverse()
        return states
    #Now states is an array(list) containing input states

    #Seperating input alphabets
    def sep_ip_alpha(self,n,p):
        ip_alpha=[]
        for i in range(n):
            if p[i][1]!="e":
                ip_alpha.append(p[i][1])

        ip_alpha=set(ip_alpha)
        #Converting to a set to remove duplicates
        ip_alpha=list(ip_alpha)
        #converting back again to a list for further use
        #Now ip_alpha is an array(list) containing input alphabets
        return ip_alpha

    def sep_st_alpha(self,n,p):
        #Seperating stack alphabets
        st_alpha=[] 
        for i in range(n):
            if p[i][2]!='e':
                st_alpha.append(p[i][2])

        st_alpha=set(st_alpha)
        #Converting to set to remove duplicates
        st_alpha=list(st_alpha)
        #converting back to list for further use
        #Now st_alpha is an array(list) containing stack alphabets including Z
        return st_alpha
    
    def rules_S(self,states):
        #Rules for starting variable S
        s0=states[0]
        S=[]
        for i in range(len(states)):
            temp=['S',s0+'Z'+states[i]]
            S.append(temp)
        #Now S contains set of rules for starting variable
        return S
    
    def rules_pop(self,p):
        #Rules for pop operations
        terminal=[]
        for i in range (0,n):
            if p[i][4]=="e" or p[i][4]=="Z" or p[i][4]=="z":
                temp=[]
                temp.append(p[i][0]+p[i][2]+p[i][3])
                temp.append(p[i][1])
                terminal.append(temp)
        #Now terminal contains set of rules for pop operations
        return terminal

    def rules_push(self,p,states):
        #Rules for push operations
        var=[]
        for i in range(n):
            x=p[i][4]
            x=list(x)
            if len(x)==2:
                for j in states:
                    for k in states:
                        temp=[]
                        temp.append(str(p[i][0])+str(p[i][2])+str(j))
                        temp.append(p[i][1])
                        temp.append(str(p[i][0])+str(x[0])+str(k))
                        temp.append(str(k)+str(x[1])+str(j))
                        var.append(temp)
        #Now var contains rules for push operations
        return var

    def gen_states(self,states,st_alpha):
        all_var=[]
        #To produce all possible variables and productions
        for i in states:
            for j in st_alpha:
                for k in states:
                    all_var.append(i+j+k)
        return all_var

    def gen_alp(self,x,y):
        #To generate A0,A1,A2,..... so that we can assign them to variables later
        alp=[]
        for i in range(x*y*x):
            alp.append('A'+str(i))
        return alp

    def replace_var(self,var,alp,all_var):
        for i in var:
            l=var.index(i)
            var.remove(i)
            for j in i:
                loc=i.index(j)
                if j in all_var:
                    x=all_var.index(j)
                    i.remove(j)
                    i.insert(loc,alp[x])
            var.insert(l,i)        
        return var

    def replace_term(self,terminal,alp,all_var):
        for i in terminal:
            l=terminal.index(i)
            terminal.remove(i)
            for j in i:
                loc=i.index(j)
                if j in all_var:
                    x=all_var.index(j)
                    i.remove(j)
                    i.insert(loc,alp[x])
            terminal.insert(l,i)
        return terminal

    
    def get_T_1(self,terminal):
        #To get all the terminal production variables
        t_1=[]
        for i in terminal:
            t_1.append(i[0])
        return t_1

    def get_V_1(self,var):
        #To get all the variable producing variables
        v_1=[]
        for i in var:
            v_1.append(i[0])
        return v_1

    def remove_var_1(self,v1,t1,var,S):
        #To remove useless productions from variables
        temp=[]
        for i in S:
            x=i[1].lower()
            temp.append(x)
        for i in var:
            if i[0] not in temp:
                var.remove(i)
        for i in var:
            if i[2] not in v1 and i[2] not in t1:
                var.remove(i)
        for j in var:
            if j[3] not in v1 and j[3] not in t1:
                var.remove(j)
        for k in var:
            if k[2]==k[0] and k[3]==k[0]:
                var.remove(k)
        return var
        #Now var contains only feasible productions

    def remove_S(self,S,v1,t1):
        #To remove useless productions from source productions
        for i in S:
            if i[1] not in v1 and i[1] not in t1:
                S.remove(i)
        return S
    #Now S contains feasible productions only

    def op(self,var,terminal,S,alp,all_var):
        for i in S:
            k=i[1].lower()
            #Replaces the source production variables by A0,A1,....
            x=all_var.index(k)
            y=alp[x]
            print("{0}=>{1}".format(str(i[0]),y))
        for i in var:
            print("{0}=>{1} {2} {3}".format(str(i[0]),str(i[1]),str(i[2]),str(i[3])))
        for i in terminal:
            print("{0}=>{1}".format(str(i[0]),str(i[1])))

    def checkp(self,p):
        #to check whether the entered productions are valid
        for i in p:
            if len(i)!=5:
                return 0
        return 1

    def checkempty(self,p):
        #To check whether the PDA accepts by empty stack
        i=p[0]
        if i[2]!='z':
            return 0
        return 1
    


#Main program
N=PDA()

n=N.readn()
#n Contains number of productions

p=N.readp()
#p Contains productions

c=N.checkp(p)
#Checking whether the entered productions are valid or not
if c==0:
    print("Data entered is invalid")
    quit()

c2=N.checkempty(p)
#Checking whether empty stack is given
if c2==0:
    print("You have not entered an empty stack")
    print("Stack symbol must be z in the first productions")
    quit()


states=N.seperate_ip_state(n,p)
#Contains the states of PDA


ip_alpha=N.sep_ip_alpha(n,p)
#contains input alphabets of PDA


st_alpha=N.sep_st_alpha(n,p)
#Contains stack alphabets of PDA


S=N.rules_S(states)
#Source productions


terminal=N.rules_pop(p)
#Variables producing terminals


var=N.rules_push(p,states)
#Variables producing variables

#Now the cfg has been generated
#Now it needs to be simplified

all_var=N.gen_states(states,st_alpha)
#Contains all possible states


alp=N.gen_alp(len(states),len(st_alpha))
#Contains A0,A1,....

#S=N.replace_s(S,alp,all_var)

T1=N.get_T_1(terminal)
#Contains the contents of 1st column of terminals


V1=N.get_V_1(var)
#Contains the content of 1st column of var

S=N.remove_S(S,V1,T1)
#Useless productions are eliminated

var=N.remove_var_1(V1,T1,var,S)
#Useless productions are eliminated

var=N.replace_var(var,alp,all_var)
#Replacing variables by A0,A1,.....

terminal=N.replace_term(terminal,alp,all_var)
# Replacing variables by A0,A1,.....

N.op(var,terminal,S,alp,all_var)
#Printing the productions
