:-use_module(python_lib).

run_local(D):-
	python_call('agentUtil','main',D,X),
	writeln(X).