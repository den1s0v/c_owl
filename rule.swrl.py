#############		 Paste rules to to Protege`s SWRL Tab 			  #############
############# (*.py extension is just used for syntax highlighting :) #############
### Rule format structure: blocks separated by blank line:
### - variables (`?x`, `?my_var`) type declaration.
### - conditions & restrictions; last line is exact rule trigger.
### - strings assignment; last line is concatenation of result message.
### > line starting with `->` is a rule body - saves message as new data property assigned to LOG (global individual). 



# BeforeActTransitive
c_schema:Act(?b) ^ c_schema:Act(?c) ^ c_schema:Act(?a) ^ c_schema:beforeAct(?a, ?b) ^ c_schema:beforeAct(?b, ?c) -> c_schema:beforeAct(?a, ?c)


# 1
# ActBeforeStartOfBlockError
c_schema:Context(?c) 
c_schema:Block(?block) 
c_schema:Statement(?stmt1) 
c_schema:Act(?act1) 
c_schema:Act(?act) 

c_schema:hasContext(?act1, ?c) 
c_schema:hasContext(?act,  ?c) 
c_schema:hasFirst(?block, ?stmt1) 
c_schema:hasOrigin(?c, ?block) 
c_schema:hasOrigin(?act1, ?stmt1) 
c_schema:before(?act, ?act1)

c_schema:hasIndex(?c, ?index)
c_schema:hasOrigin(?act, ?stmt) 
c_schema:hasSource(?stmt, ?src) 
c_schema:hasLocationSuffix(?stmt, ?stlbl) 
swrlb:stringConcat(?msg, "ActBeforeStartOfBlockError: act `", ?src, "` (", ?stlbl, "#", ?index, ") is placed before start of block.")
 -> c_schema:message(c_schema:ERRORS, ?msg)

# 2
# ActAfterEndOfBlockError
c_schema:Context(?c) 
c_schema:Block(?block) 
c_schema:Statement(?stmt_end) 
c_schema:Act(?end) 
c_schema:Act(?act) 

c_schema:hasContext(?end, ?c) 
c_schema:hasContext(?act,  ?c) 
c_schema:hasLast(?block, ?stmt_end) 
c_schema:hasOrigin(?c, ?block) 
c_schema:hasOrigin(?end, ?stmt_end) 
c_schema:before(?end, ?act)

c_schema:hasIndex(?c, ?index)
c_schema:hasOrigin(?act, ?stmt) 
c_schema:hasSource(?stmt, ?src) 
c_schema:hasLocationSuffix(?stmt, ?stlbl) 
swrlb:stringConcat(?msg, "ActAfterEndOfBlockError: act `", ?src, "` (", ?stlbl, "#", ?index, ") is placed after end of block.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# 3
# ActsPairMisorderError
c_schema:Context(?c)
c_schema:Statement(?stmt_1)
c_schema:Statement(?stmt_2)
c_schema:Act(?act1)
c_schema:Act(?act2)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act2, ?c)
c_schema:hasNext(?stmt_1, ?stmt_2)
c_schema:hasOrigin(?act1, ?stmt_1)
c_schema:hasOrigin(?act2, ?stmt_2)
c_schema:before(?act2, ?act1)

c_schema:hasIndex(?c, ?index)
c_schema:hasSource(?stmt_1, ?src1) 
c_schema:hasSource(?stmt_2, ?src2) 
swrlb:stringConcat(?msg, "ActsPairMisorderError: acts `", ?src2, "` and `", ?src1, "` are placed in reversed order.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# 4
# ActCannotFollowActError
c_schema:Context(?c)
c_schema:Statement(?stmt_act1)
c_schema:Statement(?stmt_act2)
c_schema:Act(?act1)
c_schema:Act(?act2)
c_schema:Statement(?stmt_2)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act2, ?c)
c_schema:hasNext(?act1, ?act2)
c_schema:hasNext(?stmt_act1, ?stmt_2)
c_schema:hasOrigin(?act1, ?stmt_act1)
c_schema:hasOrigin(?act2, ?stmt_act2)

differentFrom(?stmt_act2, ?stmt_2)

c_schema:hasSource(?stmt_act1, ?src_a1) 
c_schema:hasSource(?stmt_act2, ?src_a2) 
c_schema:hasSource(?stmt_2, ?src2) 
swrlb:stringConcat(?msg, "ActCannotFollowActError: `", ?src_a1, "` must be followed by `", ?src2, "` , not `", ?src_a2, "`.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# 5
# ActCannotPrecedeActError
c_schema:Context(?c)
c_schema:Statement(?stmt_act1)
c_schema:Statement(?stmt_act2)
c_schema:Act(?act1)
c_schema:Act(?act2)
c_schema:Statement(?stmt_1)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act2, ?c)
c_schema:hasNext(?act1, ?act2)
c_schema:hasNext(?stmt_1, ?stmt_act2)
c_schema:hasOrigin(?act1, ?stmt_act1)
c_schema:hasOrigin(?act2, ?stmt_act2)

differentFrom(?stmt_act1, ?stmt_1)

c_schema:hasSource(?stmt_act1, ?src_a1)
c_schema:hasSource(?stmt_act2, ?src_a2)
c_schema:hasSource(?stmt_1, ?src1)
swrlb:stringConcat(?msg, "ActCannotPrecedeActError: `", ?src_a2, "` must be preceeded by `", ?src1, "` , not `", ?src_a1, "`.")
 -> c_schema:message(c_schema:ERRORS, ?msg)

