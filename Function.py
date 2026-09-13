import numpy as np

def FMatrix(NumEpwm,NumSpi,NumSci,NumEqep,NumOutxbar,NumMcan,NumLin,NumI2c,NumClboutxbar):
    # EPWM SubModel Weight Matrix
    Fepwm = np.zeros((NumEpwm*2, NumEpwm))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumEpwm + 1):
        Fepwm[Nrow, Ncol] = 1 + 0.01 * i + 0.001 * 1
        Fepwm[Nrow + 1, Ncol] = 1 + 0.01 * i + 0.001 * 2
        Ncol += 1
        Nrow += 2

    # SPI SubModel Weight Matrix
    Fspi = np.zeros((NumSpi * 4, NumSpi))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumSpi + 1):
        Fspi[Nrow, Ncol] = 2 + 0.1 * i + 0.01 * 1
        Fspi[Nrow + 1, Ncol] = 2 + 0.1 * i + 0.01 * 2
        Fspi[Nrow + 2, Ncol] = 2 + 0.1 * i + 0.01 * 4
        Fspi[Nrow + 3, Ncol] = 2 + 0.1 * i + 0.01 * 8
        Ncol += 1
        Nrow += 4

    # SCI SubModel Weight Matrix
    Fsci = np.zeros((NumSci * 2, NumSci))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumSci + 1):
        Fsci[Nrow, Ncol] =  4 + 0.1 * (2 ** (i - 1)) + 0.01 * 1
        Fsci[Nrow + 1, Ncol] = 4 + 0.1 * (2 ** (i - 1)) + 0.01 * 2
        Ncol += 1
        Nrow += 2

    # EQEP SubModel Weight Matrix
    Feqep = np.zeros((NumEqep * 4, NumEqep))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumEqep + 1):
        Feqep[Nrow, Ncol] = 8 + 0.1 * (2 ** (i - 1)) + 0.01 * 1
        Feqep[Nrow + 1, Ncol] = 8 + 0.1 * (2 ** (i - 1)) + 0.01 * 2
        Feqep[Nrow + 2, Ncol] = 8 + 0.1 * (2 ** (i - 1)) + 0.01 * 4
        Feqep[Nrow + 3, Ncol] = 8 + 0.1 * (2 ** (i - 1)) + 0.01 * 8
        Ncol += 1
        Nrow += 4

    # OutputXBAR SubModel Weight Matrix
    Foutxbar = np.zeros((NumOutxbar * 1, NumOutxbar))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumOutxbar + 1):
        Foutxbar[Nrow, Ncol] =  16 + 0.1 * i
        Ncol += 1
        Nrow += 1

    # MCAN SubModel Weight Matrix
    Fmcan = np.zeros((NumMcan * 2, NumMcan))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumMcan + 1):
        Fmcan[Nrow, Ncol] = 32 + 0.1 * i + 0.01 * 1
        Fmcan[Nrow + 1, Ncol] = 32 + 0.1 * i + 0.01 * 2
        Ncol += 1
        Nrow += 2

    # LIN SubModel Weight Matrix
    Flin = np.zeros((NumLin * 2, NumLin))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumLin + 1):
        Flin[Nrow, Ncol] = 64 + 0.1 * i + 0.01 * 1
        Flin[Nrow + 1, Ncol] = 64 + 0.1 * i + 0.01 * 2
        Ncol += 1
        Nrow += 2

    Fi2c = np.zeros((NumI2c * 2, NumI2c))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumI2c + 1):
        Fi2c[Nrow, Ncol] = 128 + 0.1 * i + 0.01 * 1
        Fi2c[Nrow + 1, Ncol] = 128 + 0.1 * i + 0.01 * 2
        Ncol += 1
        Nrow += 2

    # CLB_OUTPUT XBAR SubModel Weight Matrix
    Fclboutxbar = np.zeros((NumClboutxbar * 1, NumClboutxbar))
    Ncol = 0
    Nrow = 0
    for i in range(1, NumClboutxbar + 1):
        Fclboutxbar[Nrow, Ncol] = 256 + 0.1 * i
        Ncol += 1
        Nrow += 1

    return (Fepwm,Fspi,Fsci,Feqep,Foutxbar,Fmcan,Flin,Fi2c,Fclboutxbar)


def BMatrix(NumFuncPin,NumEpwmPin,NumSpiPin,NumSciPin,NumEqepPin,NumOutxbarPin,NumMcanPin,NumLinPin,NumI2cPin,NumClboutxbarPin):

    # Initialize Matrix
    Bepwm = np.zeros((NumFuncPin, NumEpwmPin))
    Bspi = np.zeros((NumFuncPin, NumSpiPin))
    Bsci = np.zeros((NumFuncPin, NumSciPin))
    Beqep = np.zeros((NumFuncPin, NumEqepPin))
    Boutxbar = np.zeros((NumFuncPin, NumOutxbarPin))
    Bmcan = np.zeros((NumFuncPin, NumMcanPin))
    Blin = np.zeros((NumFuncPin, NumLinPin))
    Bi2c = np.zeros((NumFuncPin, NumI2cPin))
    Bclboutxbar = np.zeros((NumFuncPin, NumClboutxbarPin))

    # Calculate Row Index
    row1 = NumEpwmPin
    row2 = row1 + NumSpiPin
    row3 = row2 + NumSciPin
    row4 = row3 + NumEqepPin
    row5 = row4 + NumOutxbarPin
    row6 = row5 + NumMcanPin
    row7 = row6 + NumLinPin
    row8 = row7 + NumI2cPin
    row9 = row8 + NumClboutxbarPin

    # Check Function Pin Number
    if row9 == NumFuncPin:
        print("BMatrix Mode Number Correct")
    else:
        print("Warning: BMatrix Mode Number Incorrect!")

    # Construct EPWM Matrix
    Bepwm[0:row1, :] = np.eye(NumEpwmPin)
    # Construct SPI Matrix
    Bspi[row1:row2, :] = np.eye(NumSpiPin)
    # Construct SCI Matrix
    Bsci[row2:row3, :] = np.eye(NumSciPin)
    # Construct EQEP Matrix
    Beqep[row3:row4, :] = np.eye(NumEqepPin)
    # Construct OUTPUT XBAR Matrix
    Boutxbar[row4:row5, :] = np.eye(NumOutxbarPin)
    # Construct MCAN Matrix
    Bmcan[row5:row6, :] = np.eye(NumMcanPin)
    # Construct LIN Matrix
    Blin[row6:row7, :] = np.eye(NumLinPin)
    # Construct I2C Matrix
    Bi2c[row7:row8, :] = np.eye(NumI2cPin)
    # Construct CLB OUTPUT XBAR Matrix
    Bclboutxbar[row8:row9, :] = np.eye(NumClboutxbarPin)

    # Return Matrix
    return (Bepwm,Bspi,Bsci,Beqep,Boutxbar,Bmcan,Blin,Bi2c,Bclboutxbar)