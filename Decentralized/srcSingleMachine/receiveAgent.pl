:-use_module(python_lib).

%handler
receive(Receiving,(localhost,50),W):-
	writeln('Handler for post agent'),
	writeln('Client ':W),
	python_call('runLocal','main',W,X),
	writeln(X).