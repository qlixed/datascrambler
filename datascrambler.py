'''
=== ds.py ===
DataScrambler!
@author: QliXed [aka QliX=D!, EHB]
@contact: qlixed_at_gmail_dot_com
'''
from optparse import OptionParser, OptionGroup
from crypt import Crypter, CryptoBlock
from scrambler import Scrambler
import sys
from os.path import isfile
from tempfile import NamedTemporaryFile
from os import getpid, rename, unlink


def get_cmdline_parser():
    '''
        get_cmdline_parser:
        Create and Setup the OptionParser for parse the cmdline.
        @return OptionParser Instance
    '''
    usage_msg = """
    Scrambling data?, so:
    \t%prog --key the_key --scramble -p 10 -m 4 -k 6 filename
    Unscrambling data?, so:
    \t%prog --key the_key --unscramble --output-file out_filename filename1 [filename2 ... filenameN]
    More information?, try:
    \t%prog --help
    """
    the_parser = OptionParser(usage=usage_msg)
    the_parser.add_option("-k", "--key", dest="key",
        help="KEY is the encryption/decryption key to use.", metavar="KEY")
    
    the_parser.add_option("-u", "--unscramble", action="store_false",
        dest="scramble", help="action: unscramble and decrypt.")
    unscramble_params = OptionGroup(the_parser, "=== Unscramble Options ==",
        "This options need to be specified only on --unscramble action is done.")
    unscramble_params.add_option("-o", "--output-file", dest="output",
        help="OUT_FILENAME Indicate the output filename.", metavar="OUT_FILENAME")
    
    the_parser.add_option("-s", "--scramble", action="store_true", dest="scramble",
        help="action encrypt and scramble a file")
    scramble_params = OptionGroup(the_parser, "=== Scramble Options ===",
        "This options need to be specified only on --scramble action is done."
        "Remember that the relation between the numbers are:"
        "\tNUM_PARTS>RETAIN_PARTS>=MIN_PARTS")
    scramble_params.add_option("-p", "--parts", dest="parts", type='int',
          help="NUM_PARTS is the number of parts that we going to split the file,", metavar="NUM_PARTS")
    scramble_params.add_option("-m", "--minparts", dest="minparts", type='int',
          help="MIN_PARTS indicate the numbers of parts that we going to need to recover the original file.", metavar="MIN_PARTS")
    scramble_params.add_option("-r", "--retainparts", dest="retainparts", type='int',
          help="RETAIN_PARTS indicate the numbers of parts that we retain of the original split. If not specified, so we keep only MIN_PARTS.", metavar="RETAIN_PARTS")
    
    the_parser.add_option_group(scramble_params)
    the_parser.add_option_group(unscramble_params)
    return the_parser


if __name__ == '__main__':
    cmdline_parser = get_cmdline_parser()
    (cmdops, args) = cmdline_parser.parse_args()
    # Validating parameters:
    #   It's Large, it's boring, but needs to be done.
    if cmdops.scramble is None:
        cmdline_parser.error("You need to indicate the action, you're trying to scramble or unscramble things?")
        cmdline_parser.print_help()
        sys.exit(-1)
    if cmdops.key is None:
        cmdline_parser.error("You need to specify the key")
        cmdline_parser.print_help()
        sys.exit(-1)
    if cmdops.scramble: #Need to check the parts, retain and min parts
        if cmdops.parts is None:
            cmdline_parser.error("You need to specify the number of parts that we going to split the data.")
            cmdline_parser.print_help()
            sys.exit(-1)
        if cmdops.minparts is None:
            cmdline_parser.error("You need to specify the minimun number of parts that we going to keep.")
            cmdline_parser.print_help()
            sys.exit(-1)
        if cmdops.retainparts is not None:
            if cmdops.retainparts < cmdops.minparts:
                cmdline_parser.error("Remember that KEEPEDPARTS need to be equal or higher than MINPARTS")
                cmdline_parser.print_help()
                sys.exit(-1)
        if len(args) == 0:
            cmdline_parser.error("You need to specify a filename to scramble!")
            cmdline_parser.print_help()
            sys.exit(-1)
        if len(args) > 1:
            cmdline_parser.error("You need to specify only one filename to scramble!")
            cmdline_parser.print_help()
            sys.exit(-1)
    else:
        if cmdops.output is None:
            cmdline_parser.error("You need to specify the output filename!")
            cmdline_parser.print_help()
            sys.exit(-1)
        if len(args) == 0 or len(args) < 2:
            cmdline_parser.error("You need to specify two or more filenames to unscramble!")
            cmdline_parser.print_help()
            sys.exit(-1)
    # Done Params checks, now go on with the real thing
    crpt = Crypter(key=cmdops.key)
    scrmblr = Scrambler()
    if cmdops.scramble:
        #Scramble!
        if not isfile(args[0]):
            cmdline_parser.error("{0} is not a file!".format(args[0]))
            cmdline_parser.print_help()
            sys.exit(-1)
        fd_source = open(args[0], 'rb')
        fc = fd_source.read()
        fd_source.close()
        crpt.encrypt_data(fc)
        crpt_blocks = crpt.get_encrypted_blocks()
        fd_temp = NamedTemporaryFile('wb', prefix=str(getpid()) + "crpt", dir="./", delete=False)
        tmp_filename = fd_temp.name
        for block in crpt_blocks:
            fd_temp.file.write("@block:" + ",".join([str(block.block_id), block.hash]) + '\n')
            fd_temp.file.write(block.encrypted)
            fd_temp.flush()
        fd_temp.close()
        scrambled_files = None
        if cmdops.retainparts is None:
            scrambled_files = scrmblr.scramble_it(tmp_filename, parts=cmdops.parts, minparts=cmdops.minparts, deleteparts=(cmdops.parts - cmdops.minparts))
        else:
            scrambled_files = scrmblr.scramble_it(tmp_filename, parts=cmdops.parts, minparts=cmdops.minparts, deleteparts=(cmdops.parts - cmdops.retainparts))
        unlink(tmp_filename)
        i = 1
        print "Done!"
        print "Files:"
        for source_file in scrambled_files:
            dest_file = "_".join([str(args[0]), str(i)])
            rename(source_file, dest_file)
            print "{0} - {1}".format(str(i), dest_file)
            i += 1
    else:
        #Unscramble! 
        input_files = args
        for infile in input_files:
            if not isfile(infile):
                cmdline_parser.error("{0} is not a file".format(infile))
                cmdline_parser.print_help()
                sys.exit(-1)
        # Ugly:
        # Just need the filename for use in the param...
        fd_temp = NamedTemporaryFile('wb', prefix=str(getpid()) + "nscmbld", dir="./")
        ft_name = fd_temp.name
        fd_temp.close()
        scrmblr.unscramble_it(input_files, ft_name)
        if not isfile(ft_name):
            print "Error when unscrambling! - Sorry :("
            sys.exit(-1)
        fd_source = open(ft_name, 'rb')
        fc = ""
        fc = fd_source.read()
        fd_source.close()
        unlink(ft_name)
        if not fc.startswith('@block:'):
            print "Error reading cryptoblocks!"
            sys.exit(-1)
        source_blocks = fc.split("@block:")
        crpt_blocks = list()
        for block in source_blocks:
            lines = block.split('\n', 1)
            metadata = lines[0].split(',')
            data = "".join(lines[1:])
        crpt_blocks.append(CryptoBlock(metadata[0], data, metadata[1]))
        crpt.decrypt_cryptoblocks(crpt_blocks)
        data_blocks = crpt.get_decrypted_blocks()
        fd_dest = open(cmdops.output, 'wb')
        fd_dest.write(''.join(data_blocks))
        fd_dest.flush()
        print "Done!"
        print "File:", fd_dest.name
        fd_dest.close()
    sys.exit(0)
        
    
    
    
     
