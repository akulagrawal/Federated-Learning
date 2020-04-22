:-use_module(python_lib).
:- initialization go.

go :-
        current_prolog_flag(argv, Arguments),
        writeln(Arguments),
        go(Arguments).

go(Args) :-
	consult('platform.pl'),
	consult('handler.pl'),
	nth0(0,Args,X),
	writeln(X),
	atom_number(X,Y),
	D is 0,
	python_call('runLocal', 'getIP', D, IP),
    	start_tartarus(IP,Y,10).
