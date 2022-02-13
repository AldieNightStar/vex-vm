from vexcommon import *

ops={}

def api_print(ip, s):
	if len(s) < 1:
		print("Nothing to pop()")
		return
	print(s.pop())

def api_dump(ip, s):
	print("DUMP:")
	print("\tSTACK 1", s)
	print("\tSTACK 2", SSTACK)

# ====================
# REPEAT LOOP
# ====================
API_REPEAT_STACK = []

# Usage
#   10 repeat
#     # Do something
#   loop
def api_repeat(ip, s):
	count = s.pop()
	API_REPEAT_STACK.append((ip, count))

# Usage
#   10 repeat
#     # Do something
#   loop
def api_loop(ip, s):
	if len(API_REPEAT_STACK) < 1:
		return
	rep = API_REPEAT_STACK.pop()
	rep = (rep[0], rep[1]-1)
	if rep[1] < 1:
		return
	API_REPEAT_STACK.append(rep)
	return rep[0]

# Usage
#   10 repeat
#     # Prints iteration count
#     iter print
#   loop
def api_iter(ip, s):
	if len(API_REPEAT_STACK) < 1:
		s.append(0)
		return
	rep = API_REPEAT_STACK[-1]
	s.append(rep[1])

# ====================
# Stack Ops
# ====================
def api_dup(ip, s):
	v = s.pop()
	s.append(v)
	s.append(v)

def api_drop(ip, s):
	s.pop()

def api_swap(ip, s):
	a = s.pop()
	b = s.pop()
	s.append(a)
	s.append(b)


# ====================
# Logical
# ====================

def api_then(ip, s):
	label = int(s.pop())
	res = int(s.pop())
	if res == 1:
		return label

def api_not(ip, s):
	res = int(s.pop())
	if res == 1:
		s.append(0)
	else:
		s.append(1)

def __logical(f):
	def log(ip, s):
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

# Usage:
#   10 "a" set
def api_set(ip, s):
	name = s.pop()
	val  = s.pop()
	MEM[name] = val

# Usage:
#   "a" get
def api_get(ip, s):
	s.append(MEM.get(s.pop()))


# ====================
# Call
# ====================

# Usage:
#   @someLabel here call
def api_call(ip, s):
	herePos = int(s.pop())
	labelPos = int(s.pop())
	s.append(herePos+1)
	return labelPos


# ====================
# Math
# ====================

def __mathematical(f):
	def proc(ip, s):
		a = s.pop()
		b = s.pop()
		s.append(f(b,a))
	return proc

ops["+"] = __mathematical(lambda a,b: a+b)
ops["-"] = __mathematical(lambda a,b: a-b)
ops["*"] = __mathematical(lambda a,b: a*b)
ops["/"] = __mathematical(lambda a,b: a/b)
ops["%"] = __mathematical(lambda a,b: a%b)

# ====================
# Second stack
# ====================

SSTACK = []

def api_save(ip, s):
	SSTACK.append(s.pop())

def api_restore(ip, s):
	s.append(SSTACK.pop())
