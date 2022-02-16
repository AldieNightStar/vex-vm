from vexcommon import *

ops={}

# ====================
# Debugging
# ====================

def api_print(ip, s, retStack):
	if len(s) < 1:
		print("Nothing to pop()")
		return
	print(s.pop())

def api_dump(ip, s, retStack):
	print("DUMP:")
	print("\tSTACK 1", s)
	print("\tSTACK 2", SSTACK)

def api_pause(ip, s, retStack):
	api_dump(ip, s)
	input(f"pos:{ip} || PAUSED!!!")

# ====================
# REPEAT LOOP
# ====================
API_REPEAT_STACK = []

# Usage
#   10 repeat
#     # Do something
#   loop
def api_repeat(ip, s, retStack):
	count = s.pop()
	API_REPEAT_STACK.append((ip, count))

# Usage
#   10 repeat
#     # Do something
#   loop
def api_loop(ip, s, retStack):
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
def api_iter(ip, s, retStack):
	if len(API_REPEAT_STACK) < 1:
		s.append(0)
		return
	rep = API_REPEAT_STACK[-1]
	s.append(rep[1])

# ====================
# Stack Ops
# ====================
def api_dup(ip, s, retStack):
	v = s.pop()
	s.append(v)
	s.append(v)

def api_drop(ip, s, retStack):
	s.pop()

def api_swap(ip, s, retStack):
	a = s.pop()
	b = s.pop()
	s.append(a)
	s.append(b)

def api_slen(ip, s, retStack):
	s.append(len(s))


# ====================
# Logical
# ====================

# 1 @main then
def api_then(ip, s, retStack):
	label = int(s.pop())
	res = int(s.pop())
	if res == 1:
		retStack.append(ip)
		return label

def api_not(ip, s, retStack):
	res = int(s.pop())
	if res == 1:
		s.append(0)
	else:
		s.append(1)

def api_is_none(ip, s, retStack):
	res = s.pop()
	if res == None:
		s.append(1)
	else:
		s.append(0)

def api_none(ip, s):
	s.append(None)

def __logical(f):
	def log(ip, s):
		b = s.pop()
		a = s.pop()
		if f(a,b):
			s.append(1)
		else:
			s.append(0)
	return log

ops["eq"]  = __logical(lambda a, b: a == b)
ops["neq"]  = __logical(lambda a, b: a != b)
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
def api_set(ip, s, retStack):
	name = s.pop()
	val  = s.pop()
	MEM[name] = val

# Usage:
#   "a" get
def api_get(ip, s, retStack):
	s.append(MEM.get(s.pop()))

# ====================
# Local Memory
# ====================

# Stack based mem
LMEM = []

def api_local(ip, s, retStack):
	# Add new element to the mem stack
	LMEM.append({})

def api_endlocal(ip, s, retStack):
	# Just remove last element
	LMEM.pop()

# Usage:
#   "a" lget
def api_lget(ip, s, retStack):
	name = s.pop()
	if len(LMEM) < 1:
		api_local(ip, s)
	s.append(LMEM[-1].get(name))

# Usage:
#   123 "a" lset
def api_lset(ip, s, retStack):
	name = s.pop()
	val  = s.pop()
	if len(LMEM) < 1:
		api_local(ip, s)
	LMEM[-1][name] = val


# ====================
# Call
# ====================

# Usage:
#   @someLabel here call
def api_call(ip, s, retStack):
	herePos = int(s.pop())
	labelPos = int(s.pop())
	retStack.append(herePos+1)
	return labelPos


# ====================
# Math
# ====================

def __mathematical(f):
	def proc(ip, s, retStack):
		a = float(s.pop())
		b = float(s.pop())
		s.append(f(b,a))
	return proc

ops["+"] = __mathematical(lambda a,b: a+b)
ops["-"] = __mathematical(lambda a,b: a-b)
ops["*"] = __mathematical(lambda a,b: a*b)
ops["/"] = __mathematical(lambda a,b: a/b)
ops["%"] = __mathematical(lambda a,b: a%b)

def api_goto(ip, s, retStack):
	return int(s.pop())

def _inc(ip, s, retStack):
	s.append(s.pop() + 1)

def _dec(ip, s, retStack):
	s.append(s.pop() - 1)

ops["--"] = _dec
ops["++"] = _inc

# ====================
# Second stack
# ====================

SSTACK = []

def api_save(ip, s, retStack):
	SSTACK.append(s.pop())

def api_restore(ip, s, retStack):
	s.append(SSTACK.pop())

# ====================
# Arrays
# ====================

def api_array(ip, s, retStack):
	arr = []
	while True:
		el = tryPop(s)
		if el == None:
			break
		arr.insert(0, el)
	s.append(arr)

# $array @label foreach
def api_foreach(ip, s, retStack):
	lab = tryPop(s)
	arr = tryPop(s)
	if not type(arr) is list:
		return
	s.append(ip)
	for i in range(len(arr)):
		el = arr[i]
		if i!=0:
			s.append(lab)
		s.append(el)
	return lab
