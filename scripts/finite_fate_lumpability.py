from fractions import Fraction as Q
import json

def analyze(P,groups,loss,horizon=5):
    n=len(P)
    if n<2 or len(groups)!=n or not loss or any(i not in range(n) for i in loss):
        raise ValueError("invalid state or loss")
    M=[[Q(str(v)) for v in row] for row in P]
    if any(len(row)!=n or min(row)<0 or sum(row)!=1 for row in M):
        raise ValueError("nonstochastic matrix")
    blocks={k:[i for i,g in enumerate(groups) if g==k] for k in dict.fromkeys(groups)}
    if any(set(b)&set(loss) and not set(b)<=set(loss) for b in blocks.values()):
        raise ValueError("loss not measurable")
    witness=None
    for ids in blocks.values():
        for i in ids[1:]:
            for target,js in blocks.items():
                a=sum(M[ids[0]][j] for j in js)
                b=sum(M[i][j] for j in js)
                if a!=b and witness is None:
                    witness=[ids[0],i,str(target),str(a),str(b)]
    T=[row[:] for row in M]
    for i in loss:T[i]=[Q(int(i==j)) for j in range(n)]
    risk=[Q(int(i in loss)) for i in range(n)]
    trajectory=[]
    for t in range(1,horizon+1):
        risk=[sum(T[i][j]*risk[j] for j in range(n)) for i in range(n)]
        gap=max(max(risk[i] for i in ids)-min(risk[i] for i in ids) for ids in blocks.values())
        trajectory.append({"t":t,"risk":[str(v) for v in risk],"max_block_gap":str(gap)})
    return {"strong_lumpability":witness is None,"witness":witness,"first_hit":trajectory,"empirical_claim":False}

def example():
    P=[[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,1,0],[0,0,0,0,1]]
    return analyze(P,["A","A","B","B","LOSS"],{4})

if __name__=="__main__":
    print(json.dumps(example(),indent=2))
