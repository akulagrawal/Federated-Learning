:-use_module(python_lib).

run_local(D):-
	number_string(D,A),
	writeln(A),
	string_concat('runLocal',A,B),
	python_call(B,'main',D,X),
	writeln(X).

run_global:-
	D is 10,
	python_call('runGlobal','main',D,X),
	writeln(X).