'''
=== scrambler.py ===

@author: QliXed [aka QliX=D!, EHB]
@contact: qlixed_at_gmail_dot_com
'''
from py_ecc import DecodeFiles, EncodeFile
from random import randrange
from os import remove 
from mmap import mmap


class Scrambler(object):
    '''
    Scramble Data files using Red-Solomon (AKA raid5 parity algorithm)
    to split the files and reconstruct. 
    It uses the py_ecc library (Copyright Emin Martinian 2002.)
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass #Nothing to do.

    def scramble_it(self, filename, parts=10, minparts=4, deleteparts=4):
        '''
            Do an apparently mess with the data. :)
        '''
        filenames = EncodeFile(filename, filename + '_scrambled', parts, minparts)
        kill_list = list()
        k = 0
        #print 'choosing kill blocks:'
        while(len(kill_list) <= deleteparts - 1):
            k = randrange(0, parts - 1, 1)
            if filenames[k] not in kill_list:
                kill_list.append(filenames[k])
                #print filenames[k]
        for file2del in kill_list:           
            remove(file2del)
            filenames.remove(file2del)
        return filenames
    
    def unscramble_it(self, filenames, newfilename):
        '''
            UnDo an apparently mess with the data. :)
        '''
        return DecodeFiles(filenames, newfilename)


