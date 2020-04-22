:- initialization go.

go :-
        current_prolog_flag(argv, Arguments),
        writeln(Arguments),
        go(Arguments).

go(Args) :-
	consult('platform.pl'),
	consult('handler.pl'),
	nth0(0,Args,X),
	nth0(1,Args,Agent),
	writeln(X),
	atom_number(X,Y),
    	D is 0,
    	python_call('runLocal', 'getIP', D, IP),
    	start_tartarus(IP,Y,10),
    	create_mobile_agent(Agent,(IP,Y),handler1,[10,20]),
    	execute_agent(Agent,(IP,Y),handler1).


%:- module(loop, [upto/4, downto/4]).
%
%upto(Low,High,_Step,Low) :- Low =< High.
%upto(Low,High,Step,Var) :-
	%number_string(Low, X),
    %string_concat('agent', X, Y),
    %Port is 8000+Low,
    %writeln(Port),
    %writeln(Y),
    %start_tartarus(localhost,Port,Low),
    %writeln("hi"),
    %create_mobile_agent(Y,(localhost,Port),handler1,[Low]),
    %create_mobile_agent(Y,(localhost,Port),handler1,[Low]),
    %close_tartarus,
    %close_tartarus,
    %Inc is Low+Step,
    %Inc =< High,
    %upto(Inc, High, Step, Var).
%
%downto(Low,High,_Step,High) :- Low =< High.
%downto(Low,High,Step,Var) :-
    %Dec is High-Step,
    %Dec >= Low,
    %downto(Low, Dec, Step, Var).
