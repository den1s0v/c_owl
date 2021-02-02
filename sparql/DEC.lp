%Discrete Event Calculus for ASP 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Discete Event Calculus. 
time(0..maxstep).


% DEC 5
% Fluent remains for the next moment if not terminated now
holdsAt(F,T+1) :- holdsAt(F,T);
                  not _new_pred_1(T,F);
                  time(T);
                  fluent(F);
                  T<maxstep.

% DEC 6
% Fluent does not exist for the next moment, too if not initiated now
 :- {not holdsAt(F,T+1)}0;
    not holdsAt(F,T);
    not _new_pred_2(T,F);
    fluent(F);
    time(T);
    T<maxstep.

% DEC 9
% Fluent appears at the next moment if is initiated now
holdsAt(F,T+1) :- happens(E,T),initiates(E,F,T),event(E),fluent(F),time(T),T<maxstep.

% DEC 10
% Fluent must not exist at the next moment if is terminated now
 :- {not holdsAt(F,T+1)}0;
     happens(E,T);
     event(E);
     fluent(F);
     terminates(E,F,T);
     time(T);
     T<maxstep.


_new_pred_1(T,F) :- happens(E,T);
                    terminates(E,F,T);
                    event(E);
                    fluent(F).


_new_pred_2(T,F) :- happens(E,T);
                    initiates(E,F,T);
                    event(E);
                    fluent(F).




% A fluent can appear somewhere in time (redundant?)
{holdsAt(F,T)}:-fluent(F);
 time(T).
