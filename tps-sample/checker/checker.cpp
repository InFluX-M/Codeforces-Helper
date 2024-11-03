/*
	THIS IS NOT QUERA CHECKER
	you can use it too generator test but for quera you should read tutorials.
*/

#include "testlib.h"

using namespace std;

int main(int argc, char * argv[])
{
	registerChecker("test-name", argc, argv);
	compareRemainingLines(1);
}

