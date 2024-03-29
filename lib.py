

def getAbsPath(path):
	splitted_path = path.split('/')
	new_path = ""
	skips = 0
	for name in splitted_path[::-1]:
		if name == ".":
			continue
		
		if name == "..":
			skips += 1
			continue

		if skips > 0:
			skips -= 1
			continue
		
		new_path = name + "/" + new_path
	
	return new_path[:-1]