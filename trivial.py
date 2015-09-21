from multiprocessing import Pool
p = Pool(3)
def f(x):
	return x*x

p.map(f,[1,2,3])
#print 'null'
