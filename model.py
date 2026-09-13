import cvxpy as cp
import numpy as np
from Syspara import *
from DataDeal import ParaMatrix,FuncMatrix,Datafile_init
Mfunc = FuncMatrix
Mpara = ParaMatrix
solver = cp.xxx  # Use your useful solver

# Variables
Xepwm = cp.Variable((NumEpwm, 1), boolean=True)
Xspi = cp.Variable((NumSpi, 1), boolean=True)
Xsci = cp.Variable((NumSci, 1), boolean=True)
Xeqep = cp.Variable((NumEqep, 1), boolean=True)
Xoutxbar = cp.Variable((NumOutxbar, 1),boolean=True)
Xmcan = cp.Variable((NumMcan, 1),boolean=True)
Xlin = cp.Variable((NumLin, 1),boolean=True)
Xi2c = cp.Variable((NumI2c, 1),boolean=True)
Xclboutxbar = cp.Variable((NumClboutxbar, 1),boolean=True)
Xgpio = cp.Variable((NumGpio, NumReuse),boolean=True)
Xfunc = cp.Variable((NumFuncPin, 1))
Xchange = cp.Variable((NumFuncPin, NumReuse))
Zchange = cp.Variable((NumFuncPin, NumReuse),boolean=True)

# Constraint
Cons1 = [cp.sum(Xepwm)==EpwmUserInput,cp.sum(Xspi)==SpiUserInput,cp.sum(Xsci)==SciUserInput,cp.sum(Xeqep)==EqepUserInput,cp.sum(Xoutxbar)==OutxbarUserInput,
         cp.sum(Xmcan)==McanUserInput,cp.sum(Xlin)==LinUserInput,cp.sum(Xi2c)==I2cUserInput,cp.sum(Xclboutxbar)==ClboutxbarUserInput]
Cons2 = [cp.sum(Xgpio)==TotalFuncPin,cp.sum(Xgpio,axis=1)<= 1]
Cons3 = [(Bepwm@Fepwm@Xepwm+Bspi@Fspi@Xspi+Bsci@Fsci@Xsci+Beqep@Feqep@Xeqep+Boutxbar@Foutxbar@Xoutxbar+Bmcan@Fmcan@Xmcan+Blin@Flin@Xlin+Bi2c@Fi2c@Xi2c+Bclboutxbar@Fclboutxbar@Xclboutxbar==Xfunc),
        (Mfunc@ cp.multiply(Mpara,Xgpio)== Xchange),cp.sum(Zchange,axis=1) == 1]
for i in range(NumReuse):
    Cons3 += [Xfunc-Xchange[:, i:i+1]<=M*(1-Zchange[:, i:i+1]),Xfunc-Xchange[:, i:i+1]>=-M*(1- Zchange[:, i:i+1])]
Cons = Cons1 + Cons2 + Cons3 # All Constraints


# Objective Function
Obj = (cp.sum(Cepwm@Xepwm)+cp.sum(Cspi@Xspi)+cp.sum(Csci@Xsci)+cp.sum(Ceqep@Xeqep)+cp.sum(Coutxbar@Xoutxbar)+cp.sum(Cmcan@Xmcan)+cp.sum(Clin@Xlin)+ cp.sum(Ci2c@Xi2c)+cp.sum(Cclboutxbar@Xclboutxbar))
# Minization Optimization Problem
problem = cp.Problem(cp.Minimize(Obj),Cons)
# Solver
result = problem.solve(solver,verbose=False)
if problem.status not in [cp.OPTIMAL,cp.OPTIMAL_INACCURATE]:
    print("Solution failure")
    print("Status:",problem.status)
else:
    print("Solution success")
    print("Optimal value:",problem.value)

# Value
GPIO_value = (Xgpio.value>0.99).astype(int)
epwm_value = (Xepwm.value>0.99).astype(int)
spi_value = (Xspi.value>0.99).astype(int)
sci_value = (Xsci.value>0.99).astype(int)
eqep_value = (Xeqep.value>0.99).astype(int)
outxbar_value = (Xoutxbar.value>0.99).astype(int)
mcan_value = (Xmcan.value>0.99).astype(int)
lin_value = (Xlin.value>0.99).astype(int)
i2c_value = (Xi2c.value>0.99).astype(int)
clboutxbar_value = (Xclboutxbar.value>0.99).astype(int)

# Output
rows, cols = np.where(GPIO_value == 1)
for i in range(len(rows)):
    bin_num = format(cols[i], '04b') 
    print(f'GPIO{rows[i]} muxed {Datafile_init.iloc[rows[i],cols[i]]},GPAGMUX={int(bin_num[0:2],2)},GPAMUX={int(bin_num[2:4],2)}')
