import pandas as pd
import numpy as np
import re

## Read the Data File
Datafile_init = pd.DataFrame(pd.read_excel(r'file_root\GPIO0-GPIO68_Pins.xlsx'))
GpioList  = list(Datafile_init.iloc[:,0])
Datafile_init = Datafile_init.iloc[:, 1:] #Remove the first column
Datafile_init = Datafile_init.fillna(0)

## Parament
NumGPIO = 66
NumReuse = 16
NumFunc = 76

## Deal and weight each peripheral pin
EpwmPattern = re.compile(r'EPWM(\d+)_(A|B)')
SpiPattern  = re.compile(r'SPI([AB])_(CLK|PTE|POCI|PICO)$')
SciPattern  = re.compile(r'SCI([ABC])_(RX|TX)$')
EqepPattern = re.compile(r'EQEP(\d+)_(A|B|INDEX|STROBE)$')
OutputxbarPattern = re.compile(r'OUTPUTXBAR(\d+)')
McanPattern = re.compile(r'MCAN([AB])_(RX|TX)$')
LinPattern = re.compile(r'LIN([AB])_(RX|TX)$')
I2cPattern = re.compile(r'I2C([AB])_(SDA|SCL)$')
CLBOutputxbarPattern = re.compile(r'CLB_OUTPUTXBAR(\d+)')
def EpwmValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1) # Extract the Number
    alpha = int(num)
    letter = match.group(2)    # Extract the letter
    beta = 1 if letter == 'A' else 2 # A:alpha=1;B:alpha=2
    Goal = 1 + 0.01*alpha + 0.001*beta
    return Goal
def SpiValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)  # Extract the Number
    alpha = 1 if num =='A' else 2
    letter = match.group(2)    # Extract the letter
    if letter == 'CLK':
        beta = 1
    elif letter == 'PTE':
        beta = 2
    elif letter == 'POCI':
        beta = 4
    elif letter == 'PICO':
        beta = 8
    Goal = 2 + 0.1*alpha + 0.01*beta
    return Goal
def SciValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    if num == 'A':
        alpha = 1
    elif num == 'B':
        alpha = 2
    elif num == 'C':
        alpha = 4
    letter = match.group(2)
    beta = 1 if letter == 'RX' else 2
    Goal = 4 + 0.1*alpha + 0.01*beta
    return Goal
def EqepValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    alpha = int(num)
    letter = match.group(2)
    if letter == 'A':
        beta = 1
    elif letter == 'B':
        beta = 2
    elif letter == 'INDEX':
        beta = 4
    elif letter == 'STROBE':
        beta = 8
    Goal = 8 + 0.1*(2**(alpha-1)) + 0.01*beta
    return Goal
def OutxbarValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    alpha = int(num)
    Goal = 16 + 0.1*alpha
    return Goal
def McanValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    alpha = 1 if num == 'A' else 2
    letter = match.group(2)
    beta = 1 if letter == 'RX' else 2
    Goal = 32 + 0.1*alpha + 0.01*beta
    return Goal
def LinValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    alpha = 1 if num == 'A' else 2
    letter = match.group(2)
    beta = 1 if letter == 'RX' else 2
    Goal = 64 + 0.1*alpha + 0.01*beta
    return Goal
def I2cValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    alpha = 1 if num == 'A' else 2
    letter = match.group(2)
    beta = 1 if letter == 'SDA' else 2
    Goal = 128 + 0.1*alpha + 0.01*beta
    return Goal
def CLBOutxbarValue(element,pattern):
    match = pattern.search(element)
    num = match.group(1)
    alpha = int(num)
    Goal = 256 + 0.1*alpha
    return Goal

# All Function 
FuncList = []
# EPWM: 1-12, A/B
for num in range(1, 13):
    for letter in ['A', 'B']:
        FuncList.append(f'EPWM{num}_{letter}')
# SPI: A/B, CLK/PTE/POCI/PICO
for spi in ['A', 'B']:
    for signal in ['CLK', 'PTE', 'POCI', 'PICO']:
        FuncList.append(f'SPI{spi}_{signal}')
# SCI: A/B/C, RX/TX
for sci in ['A', 'B', 'C']:
    for signal in ['RX', 'TX']:
        FuncList.append(f'SCI{sci}_{signal}')
# EQEP: 1-3, A/B/INDEX/STROBE
for num in range(1, 4):
    for signal in ['A', 'B', 'INDEX', 'STROBE']:
        FuncList.append(f'EQEP{num}_{signal}')
# OUTPUTXBAR: 1-8
for num in range(1, 9):
    FuncList.append(f'OUTPUTXBAR{num}')
# MCAN: A/B, RX/TX
for mcan in ['A', 'B']:
    for signal in ['RX', 'TX']:
        FuncList.append(f'MCAN{mcan}_{signal}')
# LIN: A, RX/TX
for lin in ['A']:
    for signal in ['RX', 'TX']:
        FuncList.append(f'LIN{lin}_{signal}')
# I2C: A/B, SDA/SCL
for i2c in ['A', 'B']:
    for signal in ['SDA', 'SCL']:
        FuncList.append(f'I2C{i2c}_{signal}')
# CLBOUTPUTXBAR: 1-8
for num in range(1, 9):
    FuncList.append(f'CLB_OUTPUTXBAR{num}')

FuncUseList = ['EPWM','SPI','SCI','EQEP','OUTPUTXBAR','MCAN','LIN','I2C','CLB_OUTPUTXBAR']
## GPIO Peripher Weigth
ParaMatrix = np.zeros((NumGPIO,NumReuse))
for i,row in Datafile_init.iterrows():
    for j, element in enumerate(row):
        if isinstance(element, str):
            if 'EPWM' in element:
                ParaMatrix[i,j] = EpwmValue(element,EpwmPattern)
            elif 'SPI' in element:
                ParaMatrix[i,j] = SpiValue(element,SpiPattern)
            elif 'SCI' in element:
                ParaMatrix[i,j] = SciValue(element,SciPattern)
            elif 'EQEP' in element:
                ParaMatrix[i,j] = EqepValue(element,EqepPattern)
            elif 'OUTPUTXBAR' in element and 'CLB' not in element:
                ParaMatrix[i,j] = OutxbarValue(element,OutputxbarPattern)
            elif 'MCAN' in element:
                ParaMatrix[i,j] = McanValue(element,McanPattern)     
            elif 'LIN' in element:
                ParaMatrix[i,j] = LinValue(element,LinPattern) 
            elif 'I2C' in element:
                ParaMatrix[i,j] = I2cValue(element,I2cPattern)
            elif 'CLB_OUTPUTXBAR' in element:
                ParaMatrix[i,j] = CLBOutxbarValue(element,CLBOutputxbarPattern)
        else:
            ParaMatrix[i,j] = 0
## GPIO Function Transmit Matrix
FuncMatrix = np.zeros((NumFunc,NumGPIO))
for i,row in Datafile_init.iterrows():
    for j, element in enumerate(row):
        if isinstance(element, str):
            if any(prefix in element for prefix in FuncUseList):
                position = FuncList.index(element)
                FuncMatrix[position,i] = 1

df_ParaMatrix = pd.DataFrame(ParaMatrix)
df_ParaMatrix.to_csv(r'Storage_file_root\ParaMatrix.csv', index=False, header=False)
df_FuncMatrix= pd.DataFrame(FuncMatrix)
df_FuncMatrix.to_csv(r'Storage_file_root\FuncMatrix.csv', index=False, header=False)
