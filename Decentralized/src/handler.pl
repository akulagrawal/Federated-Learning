:-dynamic handler1/3.
:-use_module(python_lib).
/* guid: keyword name of agent
   (A,B): constants IP and port
   main: keyword
 */

handler1(guid,(A,B),main):-
  writeln('agent arrived'),
  writeln(guid:A:B),
  D is 0,
  python_call('agentUtil','main',D,X),
  atom_string(X,Y),
  %open('.next', read, Str),
  %read_file(Str,Lines),
  %close(Str),
  %nth0(0,Lines,Y),
  move_agent(agent1,(X,8000)),
  writeln('agent sent at ':Y).






read_file(Stream,[]) :-
    at_end_of_stream(Stream).

read_file(Stream,[Z|L]) :-
    \+ at_end_of_stream(Stream),
    read(Stream,Z),
    writeln(Z),
    read_file(Stream,L).
