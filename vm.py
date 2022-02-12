def api_print(s):
	print(s.pop())

def api_dump(s):
	print("DUMP", s)

API_FOR = [0, 0]
def api_repeat(s):
	count = s.pop()
	start = s.pop()+2
	API_FOR[0] = count
	API_FOR[1] = start

def api_loop(s):
	API_FOR[0] -= 1
	if API_FOR[0] < 1:
		return None
	return int(API_FOR[1])