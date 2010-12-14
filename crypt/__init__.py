'''
=== __init__.py ===

@author: QliXed [aka QliX=D!, EHB]
@contact: qlixed_at_gmail_dot_com
'''

from crypter import Crypter, CryptoBlock
from optparse import OptionParser  
import sys
from Crypto.Hash import SHA256

def get_cmdline_parser():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                  help="FILE to Work with", metavar="FILE")
    parser.add_option("-k", "--key", dest="key",
                  help="KEY is the encryption key to use", metavar="KEY")
    parser.add_option("-b", "--block_size", dest="block_size", type='int',
                  help="BLOCK_SIZE is the size of the every block", metavar="BLOCK_SIZE")
    return parser

if __name__ == '__main__':
    cmdopts = get_cmdline_parser()
    (opts, args) = cmdopts.parse_args()
    bs = None
    if opts.file is None:
        cmdopts.error("ERROR: You need to specify the file to encrypt")
        cmdopts.print_help()
        sys.exit(0)
    if opts.key is None:
        cmdopts.error("ERROR: You need to specify the key for the encryption")
        cmdopts.print_help()
        sys.exit(0)
    if opts.block_size is not None:
        if opts.block_size <= 1024:
            cmdopts.error("ERROR: You need to specify the block_size greater than 1024")
            cmdopts.print_help()
            sys.exit(0)
        bs = opts.block_size
    sys.stdout.write("Initializing Crypter...")
    if opts.block_size is None:
        crp = Crypter(key=opts.key)
    else:
        crp = Crypter(key=opts.key, blocklimit=opts.block_size)
    print ('OK!')
    sys.stdout.write("Open and reading the file...")
    source_file = open(opts.file, 'rb')
    fc = source_file.read()
    print ('OK!')
    sys.stdout.write("Encrypting...")
    crp.encrypt_data(fc)
    blocks = crp.get_encrypted_blocks()
    print ('OK!')
    print "---------------------------------------"
    print "Original Data: (show first 50 Chars)"
    print fc[:50]
    source_hash = SHA256.new(fc).hexdigest()
    print "Original Data hexdigest:", source_hash
    print "---------------------------------------"
    print "Encrypted Data: (show first 50 Chars)"
    print blocks[0].encrypted[:50]
    sys.stdout.write("Decrypting...")
    crp.decrypt_cryptoblocks(blocks)
    print ('OK!')
    unencrypted_blocks = crp.get_decrypted_blocks()
    print "---------------------------------------"
    print "Numblocks=", len(unencrypted_blocks)
    print "Decrypted Data: (show first 50 Chars)"
    print unencrypted_blocks[0][:50]
    unencrypted_hash = SHA256.new("".join(unencrypted_blocks)).hexdigest()
    print "Decrypted Data hexdigest:", unencrypted_hash
    print "Hash Match?:{0}".format(source_hash == unencrypted_hash)
    
