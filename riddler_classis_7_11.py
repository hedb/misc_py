from sympy import *

p = symbols('p')

t = solve(p-0.5)
print (t)


t = solve(  [p**2-0.5, p>0] )
print (t)


t = solve((1-p)**2-0.5 )
print (t)

t = solve( [(1-p)*p-0.5, p>0] )
print (t)