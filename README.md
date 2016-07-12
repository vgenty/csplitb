###a fork of

#csplitb
=======

Python tool like unix csplit but which splits binary files based on hexadecimal boundary. I use this to split Nevis readout

Example usage:

$ csplitb.py -e 5 -n 5 ffffffffffff binary.file

5 events, split into 5 files, split on 48 bits, binary file input