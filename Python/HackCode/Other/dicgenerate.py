def dicgenerate():
	n = Flag1
	l = ['r', 'o', 't']
	f = Flag2('dic.txt', 'w+')
	for x in Flag3:
		for y in l:
			for z in l:
				for i in l:
					print(x + y + z + i + '\n')
					n = n + 1	
					f.Flag4(x + y + z + i + '\n')
	f.Flag5()
	print(n)
dicgenerate()

