%% invalid network: branch references undefined bus 99

mpc.bus = [
	1	3	0	0	0	0	1	1.00	0	0	1	1.06	0.94;
	2	1	0	0	0	0	1	1.00	0	0	1	1.06	0.94;
];

mpc.gen = [
	1	0	0	10	-10	1.00	100	1	10	0	0	0	0	0	0	0	0	0	0	0	0;
];

mpc.branch = [
	1	99	0.1	0.2	0	0	0	0	0	0	1	-360	360;
];
