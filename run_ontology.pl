% run_ontology

:- current_prolog_flag(argv, [FileIn | [FileOut | _Rest]]),

format("IN:  ~s\nOUT: ~s", [FileIn, FileOut]),
% writeln(FileIn), writeln(FileOut), writeln(Rest),

[init_ontology],
run_onto(FileIn, FileOut),

halt;  % exit normally
writeln("Prolog finished with an error."),
halt.