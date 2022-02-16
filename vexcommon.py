DEBUG_MODE=True


T_CALL         = "CALL"
T_CALL_STATIC  = "CALL_STATIC"
T_GOTO_STATIC  = "GOTO_STATIC"
T_PUSH         = "PUSH"
T_PUSHLABELPOS = "PUSHLABELPOS"
T_LABEL        = "LABEL"
T_LABEL_END    = "LABEL_END"

NOP = (T_CALL, "NOP")
RET = (T_CALL, "ret")

builtin = ("NOP", "ret")

def tryPop(arr,default=None):
	try:
		return arr.pop()
	except:
		return default