#Hindi
print(f"HINDI:")
baseline = 56.44
res='''37.03
32.38
33.24
41.47
28.4'''
theta = '''0.32
0.39
0.31
0.31
0.43'''

res = [float(x) for x in res.split('\n')]
theta = [float(x) for x in theta.split('\n')]
drop_in_performance = [(baseline - x)/baseline for x in res]
res_theta = zip(theta, drop_in_performance)


res_theta = sorted(res_theta, key=lambda x: x[0])
print(*res_theta, sep='\n')
print("\n\n\n")

#GERMAN
print(f"GERMAN:")
baseline = 41.25
res='''16.37
4.11
16.7'''
theta = '''0.91
0.96
0.96'''

res = [float(x) for x in res.split('\n')]
theta = [float(x) for x in theta.split('\n')]
drop_in_performance = [(baseline - x)/baseline for x in res]
res_theta = zip(theta, drop_in_performance)


res_theta = sorted(res_theta, key=lambda x: x[0])
print(*res_theta, sep='\n')

#ARABIC
print(f"ARABIC:")
baseline = 55.32
res='''24.17
46.76
43.55
38.25
44.41
48.36
50.16
33.05'''
theta = '''0.09
0.06
0.2
0.21
0.21
0.02
0.32
0.19'''

res = [float(x) for x in res.split('\n')]
theta = [float(x) for x in theta.split('\n')]
drop_in_performance = [(baseline - x)/baseline for x in res]
res_theta = zip(theta, drop_in_performance)


res_theta = sorted(res_theta, key=lambda x: x[0])
print(*res_theta, sep='\n')
print("\n\n\n")

