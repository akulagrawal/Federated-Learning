#include <iostream>
using namespace std;

void createClient(int idx) 
{ 
    string s = "python \"federated_main_local_ini.py\" --model=cnn --dataset=mnist --epochs=10 --iid=0 --client=" + to_string(idx);
    system(s.c_str());
}

void runClient(int idx) 
{ 
    string s = "python \"federated_main_local.py\" --model=cnn --dataset=mnist --epochs=10 --iid=0 --client=" + to_string(idx);
    system(s.c_str());
}

void runGlobal() 
{ 
    string s = "python \"federated_main_global.py\" --model=cnn --dataset=mnist --epochs=10 --iid=0";
    system(s.c_str());
}

int main() {
	int n = 10;

	for(int i=0;i<n;i++) {
		createClient(i);
	}
	int n_iter = 10;
	for(int i=0;i<n_iter;i++) {
		runGlobal();
		for(int j=0;j<n;j++)
			runClient(j);
	}

	return 0;
}
