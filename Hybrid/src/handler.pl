:-dynamic handler1/3.
:-use_module(python_lib).
/* guid: keyword name of agent
   (A,B): constants IP and port
   main: keyword
 */

handler1(guid,(A,B),main):-
  writeln('agent arrived'),
  writeln(guid:A:B),
  atom_concat('._client_', guid, Cfile),
  ((exists_file(Cfile)) -> (open(Cfile, read, Cstr), read_file(Cstr,Myline), close(Cstr), nth0(0,Myline,D), atom_concat(D, '.', Temp1), atom_concat(Temp1, guid, I), python_call('agentUtil','main',I,X)) ; (atom_concat('.', guid, D), python_call('agentUtil','main',D,X))),
  writeln('Back'),
  atom_concat('._prolNext_', guid, Nextfile),
  open(Nextfile, read, Str),
  read_file(Str,Lines),
  close(Str),
  nth0(0,Lines,IP),
  nth0(1,Lines,Port),
  writeln('IP ':IP),
  writeln('Port ':Port),
  atom_number(Port, P),
  move_agent(guid,(IP,P)),
  write('agent '),
  write(guid),
  writeln(' sent').

read_file(Stream,[]) :-
    at_end_of_stream(Stream).

read_file(Stream,[Z|L]) :-
    \+ at_end_of_stream(Stream),
    read(Stream,Z),
    read_file(Stream,L).
