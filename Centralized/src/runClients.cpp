#include <iostream>
using namespace std;

// A dummy function 
void createPlatform(int idx) 
{ 
    string s = "python \"federated_main_local.py\" --model=cnn --dataset=mnist --epochs=10 --iid=0 --client=" + to_string(idx);
    system(s.c_str());
} 

int main() {
	int n = 100;

	for(int i=0;i<n;i++) {
		createPlatform(i);
	}

	return 0;
}