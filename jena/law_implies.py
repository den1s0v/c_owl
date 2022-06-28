# law_implies.py

correct_by_mistake = [
	# [(cm[0].split(","), cm[1]) for cm in list(L.strip().split("\t")) ]
	L.strip()
	 for L in """SequenceNext,SequenceBegin	TooEarlyInSequence
SequenceNext	TooLateInSequence
SequenceNext,SequenceBegin	SequenceFinishedTooEarly
SequenceEnd	SequenceFinishedNotInOrder
SequenceNext, SequenceEnd	DuplicateOfAct
AltBegin	NoFirstCondition
AltBegin,AltBranchBegin,NextAltCondition	BranchNotNextToCondition
AltBranchBegin,NextAltCondition	ElseBranchNotNextToLastCondition
AltBranchBegin	ElseBranchAfterTrueCondition
AltBranchBegin,NextAltCondition	CondtionNotNextToPrevCondition
AltBranchBegin,NextAltCondition	ConditionTooEarly
AltBranchBegin,NextAltCondition	ConditionTooLate
AltEndAfterBranch	ConditionAfterBranch
AltBranchBegin,NextAltCondition	DuplicateOfCondition
NextAltCondition	NoNextCondition
NextAltCondition,AltEndAllFalse,AltElseBranchBegin	BranchOfFalseCondition
AltEndAfterBranch	AnotherExtraBranch
AltBegin,NextAltCondition	BranchWithoutCondition
AltBranchBegin	NoBranchWhenConditionIsTrue
AltEndAllFalse	LastFalseNoEnd
AltBranchBegin	AlternativeEndAfterTrueCondition
AltEndAfterBranch	NoAlternativeEndAfterBranch
AltElseBranchBegin	LastConditionIsFalseButNoElse
IterationBeginOnTrueCond	NoIterationAfterSuccessfulCondition
IterationBeginOnTrueCond	LoopEndAfterSuccessfulCondition
LoopEndOnFalseCond	NoLoopEndAfterFailedCondition
PreCondLoopBegin,PostCondLoopBegin,LoopCondBeginAfterIteration	LoopEndsWithoutCondition
PreCondLoopBegin	LoopStartIsNotCondition
PostCondLoopBegin	LoopStartIsNotIteration
LoopEndOnFalseCond	LoopContinuedAfterFailedCondition
LoopEndOnFalseCond	IterationAfterFailedCondition
LoopCondBeginAfterIteration,LoopEndOnFalseCond	NoConditionAfterIteration
LoopCondBeginAfterIteration,LoopEndOnFalseCond	NoConditionBetweenIterations""".split("\n")]


# print(correct_by_mistake)

c2m = {}

for L in correct_by_mistake:
	cs, m = L.split("\t")
	for c in cs.split(","):
		c2m[c] = c2m.get(c, []) + [m]
		
# print(c2m)

java_code = ''

for c, ms in c2m.items():
	java_code += f'case("{c}"):\n'
	for m in ms:
	    java_code += f'	mistakeNames.add("{m}");\n'
	java_code += '	break;\n'


print(java_code)
