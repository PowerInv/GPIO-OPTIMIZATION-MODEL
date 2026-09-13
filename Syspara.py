import numpy as np
from Function import FMatrix,BMatrix

## User Input
EpwmUserInput = 3
SpiUserInput  = 1
SciUserInput  = 1
EqepUserInput = 1
OutxbarUserInput  = 1
McanUserInput  = 1
LinUserInput = 1
I2cUserInput  = 1
ClboutxbarUserInput  = 1

 # # Paraments
NumEpwm  = 12     # EPWM Model Number
NumSpi   = 2      # SPI Model Number
NumSci   = 3      # SCI Model Number
NumEqep  = 3      # EQEP Model Number
NumOutxbar = 8    # Output X-bar Number
NumMcan = 2       # Mcan Number 
NumLin = 1  
NumI2c = 2  
NumClboutxbar = 8  
NumGpio  = 66      # GPIO Number
NumReuse = 16      # GPIO Reuse Choice/Option
NumEpwmPin  = NumEpwm*2   # EPWM Peripheral Pin Number
NumSpiPin   = NumSpi*4    # SPI Peripheral Pin Number
NumSciPin   = NumSci*2    # SCI Peripheral Pin Number
NumEqepPin = NumEqep*4  
NumOutxbarPin = NumOutxbar*1  
NumMcanPin = NumMcan*2  
NumLinPin = NumLin*2  
NumI2cPin = NumI2c*2  
NumClboutxbarPin = NumClboutxbar*1  
NumFuncPin  = NumEpwmPin+NumSpiPin+NumSciPin+NumEqepPin+NumOutxbarPin+NumMcanPin+NumLinPin+NumI2cPin+NumClboutxbarPin    # All Peripheral Pin
M = 10000000  

## Parament Matrix
Cepwm = np.diag(np.arange(1, NumEpwm + 1))            # EPWM Cost Matrix
Cspi = np.diag(np.arange(1, NumSpi + 1))              # SPI Cost Matrix
Csci = np.diag(np.arange(1, NumSci + 1))              # SCI Cost Matrix
Ceqep = np.diag(np.arange(1, NumEqep + 1))            # EQEP Cost Matrix
Coutxbar = np.diag(np.arange(1, NumOutxbar + 1))      # OUTPUT XBAR Cost Matrix
Cmcan = np.diag(np.arange(1, NumMcan + 1))            # MCAN Cost Matrix
Clin = np.diag(np.arange(1, NumLin + 1))              # LIN Cost Matrix
Ci2c = np.diag(np.arange(1, NumI2c + 1))              # I2C Cost Matrix
Cclboutxbar = np.diag(np.arange(1, NumClboutxbar + 1)) # CLB_OUTPUT XBAR Cost Matrix
TotalFuncPin = (EpwmUserInput*2+SpiUserInput*4+SciUserInput*2+EqepUserInput*4+OutxbarUserInput+McanUserInput*2+LinUserInput*2+I2cUserInput*2+ClboutxbarUserInput)
(Fepwm,Fspi,Fsci,Feqep,Foutxbar,Fmcan,Flin,Fi2c,Fclboutxbar) = FMatrix(NumEpwm,NumSpi,NumSci,NumEqep,NumOutxbar,NumMcan,NumLin,NumI2c,NumClboutxbar)
(Bepwm,Bspi,Bsci,Beqep,Boutxbar,Bmcan,Blin,Bi2c,Bclboutxbar) = BMatrix(NumFuncPin,NumEpwmPin,NumSpiPin,NumSciPin,NumEqepPin,NumOutxbarPin,NumMcanPin,NumLinPin,NumI2cPin,NumClboutxbarPin)