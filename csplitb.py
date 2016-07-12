#!/usr/bin/python

import argparse,sys

#The binascii module contains a number of methods to convert between binary and various ASCII-encoded binary representations.
import binascii

#Memory-mapped file objects behave like both strings and like file objects. Unlike normal string objects, however, these are mutable. You can use mmap objects in most places where strings are expected; for example, you can use the re module to search through a memory-mapped file. 
import mmap


class CSplitB(object):

    def __init__(self, spliton, infile, number, prefix, suffix):
        #Return the binary data represented by the hexadecimal string hexstr. This function is the inverse of b2a_hex(). hexstr must contain an even number of hexadecimal digits (which can be upper or lower case), otherwise a TypeError is raised.
        self.spliton_str = binascii.unhexlify(spliton)

        if not prefix:
            prefix = "xx"
        if not suffix:
            suffix = ".dat"

        self.infile = infile
        self.number = number
        self.prefix = prefix
        self.suffix = suffix
        self.number_fmt = "%%0%dd" % self.number
        print "Self.number is {}".format(self.number_fmt)
        self.last_idx = -1
        self.count = 0

    def run(self):
        with open(self.infile, "r+b") as f:
            self.mm = mmap.mmap(f.fileno(), 0)
            while True:
                idx = self.mm.find(self.spliton_str, self.last_idx + 1)
                print "idx is ",idx," self.last_idx is ",self.last_idx
                if idx == -1:
                    self.finish()
                    break
                else:
                    self.rotate(idx)

    def rotate(self, idx):
        if self.last_idx != -1:
            self.write(self.mm[self.last_idx:idx])
        self.last_idx = idx


    def finish(self):
        self.write(self.mm[self.last_idx:])

    def write(self, data):
        outfile = self.prefix + (self.number_fmt % self.count) + self.suffix
        with open(outfile, "w+b") as f:
            f.write(data)
        self.count += 1


def main(argv = sys.argv):
    parser = argparse.ArgumentParser(description="csplitb - Context splitter on binary data.")
    parser.add_argument("spliton", help="Hexadecimal representation of data to split on.")
    parser.add_argument("infile", help="Input file.")
    parser.add_argument("-n", "--number", type=int, help="Number of zeroes to pad filename. No default")
    parser.add_argument("-f", "--prefix", help="Output file prefix. Default is xx")
    parser.add_argument("-s", "--suffix", help="Output file suffix. Default is .dat")
    args = parser.parse_args(argv[1:])

    csplitb = CSplitB(args.spliton, args.infile, args.number, args.prefix, args.suffix)
    return csplitb.run()

if __name__ == '__main__':
    main()
