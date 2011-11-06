/**
 * gcc `xml2-config --cflags --libs` -o simplesmil simplesmil.c
 *
 * section: xmlReader
 * synopsis: Parse an XML file with an xmlReader
 * purpose: Demonstrate the use of xmlReaderForFile() to parse an XML file
 *          and dump the informations about the nodes found in the process.
 *          (Note that the XMLReader functions require libxml2 version later
 *          than 2.6.)
 * usage: reader1 <filename>
 * test: reader1 test2.xml > reader1.tmp ; diff reader1.tmp reader1.res ; rm reader1.tmp
 * author: Daniel Veillard
 * copy: see Copyright for the status of this software.
 */

#include <stdio.h>
#include <libxml/xmlreader.h>

/**
 * processNode:
 * @reader: the xmlReader
 *
 * Dump information about the current node
 */
static void
processNode(xmlTextReaderPtr reader) {
    const xmlChar *name;
    name = xmlTextReaderConstName(reader);
    if (xmlStrncmp(name, "img", 3) == 0 || xmlStrncmp(name, "video", 5) == 0) {
      char cmd[256];
      const xmlChar *src;
      const xmlChar *alt;

/**
 * Read the attributes
 *
 */
      alt = xmlTextReaderGetAttribute(reader, "alt");
      src = xmlTextReaderGetAttribute(reader, "src");

      if (xmlStrncmp(name, "img", 3) == 0) {
	const xmlChar *durs;
        int dur = 0;

/**
 * Read the attributes
 *
 */
        durs = xmlTextReaderGetAttribute(reader, "dur");
 
/**
 * Scan for a integer
 * 
 */
        sscanf(durs, "%d", &dur);

/**
 * Give some debugging information
 *
 */
        printf("Img: %s (%ds)\n,", alt, dur);

/**
 * Produce the command that will load the image
 * 
 */
        snprintf(cmd, 255, "/usr/bin/xloadimage -global -fullscreen -global -onroot %s", src);

/**
 * Execute the command
 *
 */
        system(cmd);

/**
 * Sleep for the amount of time provided to show the image
 *
 */
        sleep(dur);
      }

      if (xmlStrncmp(name, "video", 5) == 0) {
	      printf("Video: %s", alt);
	      snprintf(cmd, 255, "/usr/bin/vlc --no-audio --file-caching 600 -f --vout -filter deinterlace:logo --deinterlace-mode blend --logo-file=/home/tv/logo.png --logo-x=40 --logo-y=48 %s", src);
	      	     
	      system(cmd);
       }
	       

    } 
}

/**
 * streamFile:
 * @filename: the file name to parse
 *
 * Parse and print information about an XML file.
 */
static void
streamFile(const char *filename) {
    xmlTextReaderPtr reader;
    int ret;

    reader = xmlReaderForFile(filename, NULL, 0);
    if (reader != NULL) {
        ret = xmlTextReaderRead(reader);
        while (ret == 1) {
            processNode(reader);
            ret = xmlTextReaderRead(reader);
        }
        xmlFreeTextReader(reader);
        if (ret != 0) {
            fprintf(stderr, "%s : failed to parse\n", filename);
        }
    } else {
        fprintf(stderr, "Unable to open %s\n", filename);
	sleep(10);
    }
}

int main(int argc, char **argv) {
//    if (argc != 2)
//        return(1);

    /*
     * this initialize the library and check potential ABI mismatches
     * between the version it was compiled for and the actual shared
     * library used.
     */
    LIBXML_TEST_VERSION

//    streamFile(argv[1]);
    streamFile("/home/tv/broadcast.smil");

    /*
     * Cleanup function for the XML library.
     */
    xmlCleanupParser();
    /*
     * this is to debug memory for regression tests
     */
    // xmlMemoryDump();
    return(0);
}
