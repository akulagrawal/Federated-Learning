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
  ((exists_file('.last')) -> post ; writeln('Over')),
  writeln('Back'),
  open('.prolNext', read, Str),
  read_file(Str,Lines),
  close(Str),
  nth0(0,Lines,IP),
  nth0(1,Lines,Port),
  writeln('IP ':IP),
  writeln('Port ':Port),
  atom_number(Port, P),
  move_agent(agent1,(IP,P)),
  writeln('agent sent').

post:-
  writeln('post'),
  open('.post_info', read, Str),
  read_file(Str,Lines),
  close(Str),
  writeln(Lines),
  X is 0,
  Y is 20,
  postAll(X,Y,Lines),
  D is 0,
  python_call('agentUtil','delLast',D,Z),
  writeln('Done').

postAll(X,Y,Lines):-
  ((X<Y) -> (postUtil(X,Y,Lines), Z is X+1, postAll(Z,Y,Lines)) ; writeln('Done')).

postUtil(X,Y,Lines):-
  writeln('postUtil'),
  Idx1 is X*3,
  Idx2 is Idx1+1,
  Idx3 is Idx1+2,
  nth0(Idx1,Lines,IP),
  nth0(Idx2,Lines,Port),
  nth0(Idx3,Lines,Client),
  atom_number(Port, B),
  post_agent(platform,(IP,B),[receive,Receiving,(localhost,50),Client]),
  writeln('Posted ':X).

read_file(Stream,[]) :-
    at_end_of_stream(Stream).

read_file(Stream,[Z|L]) :-
    \+ at_end_of_stream(Stream),
    read(Stream,Z),
    read_file(Stream,L).
