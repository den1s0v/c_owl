% make some input data for DEC
% run with DEC.lp


% Set length of timeline
#const maxstep={MAXSTEP}.


% Declare fluents and events causing fluents to change

{FLUENTS_DECLARATION}

{EVENTS_DECLARATION}


% Plug events to dependent fluents

{FLUENTS_DEPENDENCIES}


	% Expand binary to trenary for each moment event happens
	initiates (E, F, T) :- initiates (E, F), happens(E, T).
	terminates(E, F, T) :- terminates(E, F), happens(E, T).



% Initial state of fluents

{FLUENTS_INITIAL_STATE}


% Moments when events occur

{EVENTS_HAPPEN}


#show holdsAt/2.
