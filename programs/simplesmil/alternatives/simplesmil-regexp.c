#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <regex.h>

int main(int argc, char** argv);

int main(int argc, char** argv) {
        FILE * fp;
        char * line = NULL;
        size_t len = 0;
        ssize_t read;
	regex_t preg;
	regmatch_t match;
	
        fp = fopen("broadcast.smil", "r");
        if (fp == NULL)
                exit(EXIT_FAILURE);

	int err = regcomp(&preg, "(img|video) src=\"(.*)\" alt=\"(.*)\" dur=\"(.*)\"", REG_EXTENDED);

	while ((read = getline(&line, &len, fp)) != -1) {
//              printf("Retrieved line of length %zu :\n", read);
//    
                printf("%s", line);
		regexc(&preg, line, 1, 0, match, 0);
        }
        if (line)
                free(line);

	regfree(&preg);

        return EXIT_SUCCESS;
}
