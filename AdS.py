import sympy as sp
#low tensor indices in these defs of x,g,A,F
z,t,x1,x2=x=[sp.Symbol('z',positive=True)]+sp.symbols(['t','x1','x2'])
Lr=sp.Symbol('Lr',positive=True)
g=(Lr/z)**2*sp.diag(*[1,-1,1,1])
ginv=g.inv()


