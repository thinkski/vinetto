vinetto
=======

Forensic tool for examining Thumbs.db files

Forked from vinetto-0.07beta on http://sourceforge.net/projects/vinetto

------------------------------------------------------------------------------

                                  Vinetto

                       http://vinetto.sourceforge.net

                     Michel Roukine <rukin@users.sf.net>



Version beta 0.07 (June 14 2007)
------------------

Introduction
------------

Vinetto is a forensics tool to examine Thumbs.db files.
It is a command line python script that works on Linux, Mac OS X and
Cygwin(win32).


License
-------

This program is distributed under the GNU General Public License - see the
accompanying COPYING file for more details.


Thanks
------
Many thanks to Christophe Monniez (d-fence.be) for the idea of this tool and
for his encouragements.

The vinetto code was written with grateful thanks to Martin Schwartz, author of
Laola and its Hacking guide to the binary structure of Ole / Compound Documents.


Project overview
----------------
1 - Context : The Windows systems (98, ME, 2000 and XP) can store thumbnails
and metadata of the picture files contained in the directories of its FAT32 or
NTFS filesystems. 
Thumbnails and associated metadata are stored in Thumbs.db files. 
Thumbs.db files are undocumented OLE structured files.

Once a picture file has been deleted from the filesystem, the related thumbnail
and associated metada remain stored in the Thumbs.db file. So, the data
contained in those thumbs.db files are an helpful source of information for the
forensics investigator.

2 - What the software is intended to do : Vinetto extracts thumbnails and
associated metadata from the Thumbs.db files.

Moreover [when vinetto will be 0.98 beta] it will function according to three
modes:
  -> elementary mode : in this mode vinetto will only extract thumbnails and
     metadata from chosen Thumbs.db file.
  -> directory mode : in this mode vinetto will check for consistency between
     directory content and related Thumbs.db file i.e. it will report
     thumbnails that have a missing associated file into the directory.
  -> filesystem mode : in this mode vinetto will process whole FAT or NTFS
     partition. 

3 - What purpose it will serve : Vinetto will help *nix-based forensics
investigators to : 
  -> easily preview thumbnails of deleted pictures on Windows systems, 
  -> obtain informations (dates, path, ...) about those deleted images. 

4 - Misc. : Vinetto is intended to be integrated into forensics liveCD like
FCCU GNU/Linux Forensic Boot CD.


Requirements
------------

Python-2.3 or later.

PIL (Python Imaging Library) 1.1.5 or later. PIL is used to attempt correct
reconstitution the Type 1 thumbnails. 


Current known limitations
-------------------------

AFAIK Windows(R)(TM) uses two format types to store thumbnails in its Thumbs.db
files.
I called these formats Type 1 and Type 2.
Type 2 is compliant to jpeg format. But Type 1 seems to be a family of
jpeg-alike formats with special headers, huffman and quantization tables. 

*** Currently, vinetto does not manage to reconstitute correctly some Type 1
thumbnails. ***


Usage
-----

usage: vinetto [OPTIONS] [-s] [-U] [-o DIR] file

options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -o DIR      write thumbnails to DIR
  -H          write html report to DIR
  -U          use utf8 encodings
  -s          create symlink of the image realname to the numbered name in
              DIR/.thumbs


	Metadata list will be written on standard output.

--------------
June 14 2007
Michel Roukine
