#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

int main(int argc, char** argv);

extern char **environ;

int main(int argc, char** argv) {
	while (1) {
		int ret = system("./wrapme");

/*		if (ret == -1) {
			printf("Wrapme unavailable!\n");
			sleep(10);
		}*/

		if (WIFSIGNALED(ret) &&
			(WTERMSIG(ret) == SIGINT))
				break;
	}
}
