%% 3-bus sample for GS with Slack/PV/PQ handling

%% bus data
% bus_i type Pd Qd Gs Bs area Vm Va baseKV zone Vmax Vmin
mpc.bus = [
	1	3	0.0	0.0	0	0	1	1.00	0	0	1	1.06	0.94;
	2	2	0.0	0.0	0	0	1	1.02	0	0	1	1.06	0.94;
	3	1	30.0	10.0	0	0	1	1.00	0	0	1	1.06	0.94;
];

%% generator data
% bus Pg Qg Qmax Qmin Vg mBase status Pmax Pmin Pc1 Pc2 Qc1min Qc1max Qc2min Qc2max ramp_agc ramp_10 ramp_30 ramp_q apf
mpc.gen = [
	1	20.0	0.0	100	-100	1.00	100	1	100	0	0	0	0	0	0	0	0	0	0	0	0;
	2	20.0	0.0	100	-100	1.02	100	1	100	0	0	0	0	0	0	0	0	0	0	0	0;
];

%% branch data
% fbus tbus r x b rateA rateB rateC ratio angle status angmin angmax
mpc.branch = [
	1	2	0.05	0.20	0.02	0	0	0	0	0	1	-360	360;
	1	3	0.05	0.25	0.03	0	0	0	0	0	1	-360	360;
	2	3	0.05	0.20	0.02	0	0	0	0	0	1	-360	360;
];
