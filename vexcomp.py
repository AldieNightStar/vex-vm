from lex import lex as lex, T_STR, T_SPC, T_NUM
import os.path
import json
from vexcommon import *

TEST=True

def check_token_multiplier(s): # Returns token, count
	if "*" in s and len(s) > 1:
		arr = s.split("*", 1)
		return arr[0], int(arr[1])
	return s, 0

def find_label_end(arr, pos, name):
	while pos < len(arr):
		token = arr[pos]
		if token[0]==T_LABEL_END and token[1] == name:
			return pos
		pos += 1
	return None

def append_times(arr, el, times=1):
	if times < 1:
		times = 1
	for i in range(times):
		arr.append(el)

def first_compile(arr):
	pos=0
	res=[]
	globalVars = False
	labelStack = []
	while pos<len(arr):
		token=arr[pos]
		pos += 1
		if token.type == T_SPC:
			# SPC token types
			#   =name - variable setter with "name"
			#   $name - variable getter with "name"
			#   @name - converts label address to int and pushes to stack
			#   :name - defines new label (Need to be closed with ":") 
			#   :     - ends up current label
			#   name  - simple call
			# Get token multiplier (*123 after token name)
			tokVal, tokMul = check_token_multiplier(token.value)
			# =name will be replaced with "name" lset
			if tokVal == "global":
				globalVars = True
			elif tokVal == "endglobal":
				globalVars = False
			elif tokVal.startswith("=") and len(tokVal) > 1:
				res.append((T_PUSH, tokVal[1:]))
				if globalVars:
					res.append((T_CALL, "set"))
				else:
					res.append((T_CALL, "lset"))
			# $name will be replaced with "name" lget
			elif tokVal.startswith("$") and len(tokVal) > 1:
				res.append((T_PUSH, tokVal[1:]))
				if globalVars:
					res.append((T_CALL, "get"))
				else:
					res.append((T_CALL, "lget"))
			# :name - means label declaration	
			elif tokVal.startswith(":") and len(tokVal) > 1:
				lname = tokVal[1:]
				res.append((T_LABEL, lname))
				labelStack.append(lname)
			# : - means label declaration end
			elif tokVal == ":":
				lname = tryPop(labelStack)
				res.append((T_LABEL_END, lname))
			# @ - points to label and will be replaced in future to it's number
			elif tokVal.startswith("@") and len(tokVal) > 1:
				append_times(res, (T_PUSHLABELPOS, tokVal[1:]), tokMul)
			else:
				# Another op is as a call
				append_times(res, (T_CALL, tokVal), tokMul)
		elif token.type in (T_STR, T_NUM):
			res.append((T_PUSH, token.value))
	return res

def process_skips(arr):
	pos = 0
	willSkip = False
	while pos < len(arr):
		token = arr[pos]
		# If token is skip command
		if token[0]==T_CALL and token[1]=="skip":
			arr[pos]=NOP
			# FIND next token
			nextTok = arr[pos+1]
			# IF token is label, find it's end
			if nextTok[0] == T_LABEL:
				# Nake (CALL_STATIC, label_end_pos)
				endPos = find_label_end(arr, pos, nextTok[1])
				if endPos != None:
					arr[pos] = (T_GOTO_STATIC, endPos+1)
		pos += 1
	return arr

def process_nops(arr):
	res = []
	for a in arr:
		if a[0]==T_CALL and a[1]=="NOP":
			continue
		else:
			res.append(a)
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
		elif token[0]==T_PUSHLABELPOS:
			if token[1] in labs:
				arr[pos] = (T_PUSH, labs[token[1]])
		pos+=1
	return arr

def compile(src, debug=False):
	arr = lex(src)
	arr = first_compile(arr)
	arr = process_nops(arr)
	arr = process_skips(arr)
	arr = process_labels(arr) # Latest compilation as labels already defined
	if debug:
		for i in range(len(arr)):
			print(i, arr[i])
		print("------")
	return arr

def compile_to_json(src, filename, debug=False):
	arr = compile(src, debug)
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
		# Last param - debug: True|False
		compile_to_json(f.read(), args[1], True)