import json
from vexcommon import *

def api_get(api, name):
	f = getattr(api, 'api_'+name, None)
	if f != None:
		return f
	ops = getattr(api, 'ops', None)
	if ops != None:
		f = ops.get(name)
		if f != None:
			return f
	return None

def parse_dat(dat):
	if type(dat) != list:
		raise Exception("Run data is not list")
	return dat

def run(api, dat, args=None):
	stack = []
	retStack = []
	if args!=None:
		for arg in args:
			stack.append(arg)
	dat = parse_dat(dat)
	dat_len = len(dat)
	ip = 0
	while ip < dat_len:
		op = dat[ip]
		ip += 1
		if op[0] == T_CALL:
			if op[1] == "NOP": continue
			elif op[1] == "ret": # Restore IP from stack
				ip = int(tryPop(retStack, 0xFFFFFFFF))
			else: # Functions from api
				f = api_get(api, op[1])
				if f == None:
					raise Exception(f"No such command: '{op[1]}'")
				newIp = f(ip, stack, retStack)
				if type(newIp) is int:
					ip = newIp
		elif op[0] == T_CALL_STATIC: # Push IP to stack and goto
			retStack.append(ip)
			ip = op[1]
		elif op[0] == T_PUSH:
			stack.append(op[1])
		elif op[0] == T_GOTO_STATIC:
			ip = op[1]


if __name__ == "__main__":
	import sys
	args = sys.argv[1:]
	if len(args) < 1:
		print("Arguments: FILE [args...]")
		print("\tFILE   - file to run")
		print("\t[args] - will be added to the stack")
		sys.exit(-1)
	with open(args[0]) as f:
		import vm
		j = json.load(f)
		toAdd = None
		if len(args) > 1:
			toAdd = args[1:]
		run(vm, j, toAdd)
