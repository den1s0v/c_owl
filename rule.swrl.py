#############		 Paste rules to to Protege`s SWRL Tab 			 ##############
############# (*.py extension is just used for syntax highlighting :) ##############

# BeforeActTransitive
c_schema:Act(?b) ^ c_schema:Act(?c) ^ c_schema:Act(?a) ^ c_schema:beforeAct(?a, ?b) ^ c_schema:beforeAct(?b, ?c) -> c_schema:beforeAct(?a, ?c)


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
hasSource(?stmt, ?src) 
hasLocationSuffix(?stmt, ?stlbl) 
swrlb:stringConcat(?msg, "ActBeforeStartOfBlockError: ", ?src, ?stlbl, "#", ?index, " is placed before start of block.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


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
hasSource(?stmt, ?src) 
hasLocationSuffix(?stmt, ?stlbl) 
swrlb:stringConcat(?msg, "ActAfterEndOfBlockError: ", ?src, ?stlbl, "#", ?index, " is placed after end of block.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# ActsPairMisorderError
c_schema:Context(?c) 
# c_schema:Block(?block) 
c_schema:Statement(?stmt_1) 
c_schema:Statement(?stmt_2) 
c_schema:Act(?act1) 
c_schema:Act(?act2) 

c_schema:hasContext(?act1, ?c) 
c_schema:hasContext(?act2, ?c) 
c_schema:hasNext(?stmt_1, ?stmt_2) 
# c_schema:hasOrigin(?c, ?block) 
c_schema:hasOrigin(?act1, ?stmt_1) 
c_schema:hasOrigin(?act2, ?stmt_2) 
c_schema:before(?act2, ?act1)

c_schema:hasIndex(?c, ?index)
hasSource(?stmt_1, ?src1) 
hasSource(?stmt_2, ?src2) 
swrlb:stringConcat(?msg, "ActAfterEndOfBlockError: ", ?src1, " and ", ?src2, " are placed in swapped order.")
 -> c_schema:message(c_schema:ERRORS, ?msg)
