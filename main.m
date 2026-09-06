clc;
clear;
%% Solver Setting
ops = sdpsettings('verbose',0,'debug',1,'solver','cplex');% enforce solver,'solver','cplex'
% ops.gurobi.TimeLimit = 300; ops.gurobi.TuneTimeLimit = 0;
Mfunc_data = load('Mfunc.mat');Mfunc = Mfunc_data.Mfunc;
Mpara_data = load('Mpara.mat');Mpara = Mpara_data.Mpara;
%% User Input
EpwmUserInput = 3;
SpiUserInput  = 1;
SciUserInput  = 1;
EqepUserInput = 1;
OutxbarUserInput  = 1;
McanUserInput  = 1;
LinUserInput = 1;
I2cUserInput  = 1;
ClboutxbarUserInput  = 1;
%% Paraments
NumEpwm  = 12;  % EPWM Model Number
NumSpi   = 2;   % SPI Model Number
NumSci   = 3;   % SCI Model Number
NumEqep  = 3;   % EQEP Model Number
NumOutxbar = 8; % Output X-bar Number
NumMcan = 2;    % Mcan Number 
NumLin = 1;
NumI2c = 2;
NumClboutxbar = 8;
NumGpio  = 66;   % GPIO Number
NumReuse = 16;   % GPIO Reuse Choice/Option
NumEpwmPin  = NumEpwm*2;% EPWM Peripheral Pin Number
NumSpiPin   = NumSpi*4; % SPI Peripheral Pin Number
NumSciPin   = NumSci*2; % SCI Peripheral Pin Number
NumEqepPin = NumEqep*4;
NumOutxbarPin = NumOutxbar*1;
NumMcanPin = NumMcan*2;
NumLinPin = NumLin*2;
NumI2cPin = NumI2c*2;
NumClboutxbarPin = NumClboutxbar*1;
NumFuncPin  = NumEpwmPin+NumSpiPin+NumSciPin+NumEqepPin+NumOutxbarPin+NumMcanPin+NumLinPin+NumI2cPin+NumClboutxbarPin; % All Peripheral Pin
M = 10000000;
%% Coefficient Matrix
Cepwm = diag(1:NumEpwm);   % EPWM Cost Matrix
Cspi  = diag(1:NumSpi);    % SPI Cost Matrix
Csci  = diag(1:NumSci);    % SCI Cost Matrix
Ceqep = diag(1:NumEqep);   % EQEP Cost Matrix
Coutxbar  = diag(1:NumOutxbar); % OUTPUT XBAR Cost Matrix
Cmcan  = diag(1:NumMcan);       % MCAN Cost Matrix
Clin = diag(1:NumLin);      	% LIN Cost Matrix
Ci2c  = diag(1:NumI2c);         % I2C Cost Matrix
Cclboutxbar  = diag(1:NumClboutxbar);    % CLB_OUTPUT XBAR Cost Matrix
% Fepwm,Fspi,Fsci,Feqep,Foutxbar,Fmcan,Flin,Fi2c,Fclboutxbar are the Weight Transform Matrix,respectively
[Fepwm,Fspi,Fsci,Feqep,Foutxbar,Fmcan,Flin,Fi2c,Fclboutxbar] = FMatrix(NumEpwm,NumSpi,NumSci,NumEqep,...
                                NumOutxbar,NumMcan,NumLin,NumI2c,NumClboutxbar);
% Bepwm,Bspi,Bsci,Beqep,Boutxbar,Bmcan,Blin,Bi2c,Bclboutxbar are Mapping Transform Matrix,respectively
[Bepwm,Bspi,Bsci,Beqep,Boutxbar,Bmcan,Blin,Bi2c,Bclboutxbar] = BMatrix(NumFuncPin,NumEpwmPin,NumSpiPin,...
                                          NumSciPin,NumEqepPin,NumOutxbarPin,NumMcanPin,NumLinPin,NumI2cPin,NumClboutxbarPin);
%% Variables
Xepwm = binvar(NumEpwm,1,'full');
Xspi  = binvar(NumSpi,1,'full');
Xsci  = binvar(NumSci,1,'full');
Xeqep = binvar(NumEqep,1,'full');
Xoutxbar  = binvar(NumOutxbar,1,'full');
Xmcan  = binvar(NumMcan,1,'full');
Xlin = binvar(NumLin,1,'full');
Xi2c  = binvar(NumI2c,1,'full');
Xclboutxbar  = binvar(NumClboutxbar,1,'full');
Xgpio = binvar(NumGpio,NumReuse,'full');
Xfunc = sdpvar(NumFuncPin,1,'full');
Xchange = sdpvar(NumFuncPin,NumReuse,'full');
Zchange = binvar(NumFuncPin,NumReuse,'full');
%% Objective Function
Obj = sum(Cepwm*Xepwm,'all')+sum(Cspi*Xspi,'all')+sum(Csci*Xsci,'all')+...
      sum(Ceqep*Xeqep,'all')+sum(Coutxbar*Xoutxbar,'all')+sum(Cmcan*Xmcan,'all')+...
      sum(Clin*Xlin,'all')+sum(Ci2c*Xi2c,'all')+sum(Cclboutxbar*Xclboutxbar,'all');
% Obj = 0;
%% Constraints
Cons1 = []; % Model Output Result Must equal to the User Input Peripheral Demand
Cons1 = [Cons1,sum(Xepwm,'all')==EpwmUserInput,sum(Xspi,'all')==SpiUserInput,sum(Xsci,'all')==SciUserInput,...
    sum(Xeqep,'all')==EqepUserInput,sum(Xoutxbar,'all')==OutxbarUserInput,sum(Xmcan,'all')==McanUserInput,...
    sum(Xlin,'all')==LinUserInput,sum(Xi2c,'all')==I2cUserInput,sum(Xclboutxbar,'all')==ClboutxbarUserInput];
Cons2 = []; % Every GPIO Only be Used for One Peripheral Function or no Used
Cons2 = [Cons2,sum(Xgpio,'all')==EpwmUserInput*2+SpiUserInput*4+SciUserInput*2+EqepUserInput*4+OutxbarUserInput*1+McanUserInput*2+LinUserInput*2+I2cUserInput*2+ClboutxbarUserInput*1 ,...
         sum(Xgpio,2)<=1];
Cons3 = []; 
Cons3 = [Cons3,Bepwm*Fepwm*Xepwm+Bspi*Fspi*Xspi+Bsci*Fsci*Xsci+Beqep*Feqep*Xeqep+Boutxbar*Foutxbar*Xoutxbar+Bmcan*Fmcan*Xmcan+Blin*Flin*Xlin+Bi2c*Fi2c*Xi2c+Bclboutxbar*Fclboutxbar*Xclboutxbar==Xfunc,...
         Mfunc*(Mpara.*Xgpio)==Xchange,sum(Zchange,2) == 1];
for i = 1:NumReuse
    Cons3 = [Cons3,Xfunc-Xchange(:,i)<= M*(1-Zchange(:,i)),Xfunc-Xchange(:,i)>=-M*(1-Zchange(:,i))];
end
Cons = Cons1 + Cons2 + Cons3;
%% Solve the Optimization Model
flag = optimize(Cons,Obj,ops);
% flag = optimize(Cons,Obj);
if flag.problem ~= 0
    disp('Solution failure');
end
%% Value storage
Xepwm_value = value(Xepwm);
Xspi_value  = value(Xspi);
Xsci_value  = value(Xsci);
Xeqep_value = value(Xeqep);
Xoutxbar_value  = value(Xoutxbar);
Xmcan_value  = value(Xmcan);
Xlin_value = value(Xlin);
Xi2c_value  = value(Xi2c);
Xclboutxbar_value  = value(Xclboutxbar);
Xgpio_value = value(Xgpio);