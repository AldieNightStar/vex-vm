from vexcommon import *

ops={}

def api_print(s):
	print(s.pop())

def api_dump(s):
	print("DUMP", s)

# ====================
# REPEAT LOOP
# ====================
API_REPEAT_STACK = []

def api_repeat(s):
	count = s.pop()
	start = s.pop()+2
	API_REPEAT_STACK.append((start, count))

def api_loop(s):
	if len(API_REPEAT_STACK) < 1:
		return
	rep = API_REPEAT_STACK.pop()
	rep = (rep[0], rep[1]-1)
	if rep[1] < 1:
		return
	API_REPEAT_STACK.append(rep)
	return rep[0]

def api_iter(s):
	if len(API_REPEAT_STACK) < 1:
		s.append(0)
		return
	rep = API_REPEAT_STACK[-1]
	s.append(rep[1])

# ====================
# Stack Ops
# ====================
def api_dup(s):
	v = s.pop()
	s.append(v)
	s.append(v)

def api_drop(s):
	s.pop()

def api_swap(s):
	a = s.pop()
	b = s.pop()
	s.append(a)
	s.append(b)


# ====================
# Logical
# ====================

def api_then(s):
	label = int(s.pop())
	res = int(s.pop())
	if res == 1:
		return label

def api_not(s):
	res = int(s.pop())
	if res == 1:
		s.append(0)
	else:
		s.append(1)

def __logical(f):
	def log(s):
		b = s.pop()
		a = s.pop()
		if f(a,b):
			s.append(1)
		else:
			s.append(0)
	return log

ops["=="]  = __logical(lambda a, b: a == b)
ops["!="]  = __logical(lambda a, b: a != b)
ops[">"]   = __logical(lambda a, b: a >  b)
ops["<"]   = __logical(lambda a, b: a <  b)
ops[">="]  = __logical(lambda a, b: a >= b)
ops["<="]  = __logical(lambda a, b: a <= b)



# ====================
# Memory
# ====================
MEM = {}

def api_set(s):
	s.append(MEM[s.pop()])

def api_get(s):
	MEM[s.pop()] = s.pop()