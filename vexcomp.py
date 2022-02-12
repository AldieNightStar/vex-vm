from lex import lex as llex, T_STR, T_SPC, T_NUM
import os.path
import json
from vexcommon import *

TEST=True

def lex(src):
	return llex(src)

def first_compile(arr):
	pos=0
	res=[]
	labelStack = []
	while pos<len(arr):
		token=arr[pos]
		pos += 1
		lebalStack = []
		if token.type == T_SPC:
			if token.value.startswith(":") and len(token.value) > 1:
				lname = token.value[1:]
				res.append((T_LABEL, lname))
				labelStack.append(lname)
			elif token.value == ":":
				lname = tryPop(labelStack)
				res.append((T_LABEL_END, lname))
			else:
				res.append((T_CALL, token.value))
		elif token.type in (T_STR, T_NUM):
			res.append((T_PUSH, token.value))
	return res

# Here we will replace label names with numbers.
# Also label declarations will replaced with NOP's
def process_labels(arr):
	pos = 0
	labs = {}
	# Find labels, replace declarations with NOP's
	while pos < len(arr):
		token = arr[pos] # token: (TYPE, val)
		if token[0] == T_LABEL:
			labs[token[1]] = pos
			arr[pos] = NOP
		elif token[0] == T_LABEL_END:
			arr[pos] = RET
		pos+=1
	# Find calls which the same as label name. Replace it with static call (which points to code position itself)
	pos = 0
	while pos < len(arr):
		token = arr[pos]
		if token[0]==T_CALL and token[1] in builtin: # Ignore built in commands
			pos+=1
			continue
		elif token[0]==T_CALL:
			if token[1] in labs:
				arr[pos] = (T_CALL_STATIC, labs[token[1]])
		pos+=1
	return arr

def compile(src):
	arr = lex(src)
	arr = first_compile(arr)
	arr = process_labels(arr)
	return arr

def compile_to_json(src, filename):
	arr = compile(src)
	with open(filename, 'w') as f:
		f.write(json.dumps(arr, indent=4))
	return arr

if __name__ == "__main__":
	import sys
	args = sys.argv[1:]
	if len(args) < 2:
		print("Usage: FILE OUTPUT_FILE.json")
		print("\tFILE - File to compile")
		print("\tOUTPUT_FILE - Output file after compilation")
		sys.exit(-1)
	with open(args[0]) as f:
		compile_to_json(f.read(), args[1])