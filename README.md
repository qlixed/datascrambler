# datascrambler
Datascrambler a command line application to encrypt and scramble (or ofuscate?) information!. It Uses AES (pycrypto) and Reed-Solomon (py_ecc) to Scramble the data. Is written in Python and is cross-platform. See the Home https://github.com/qlixed/datascrambler/wiki/Home on Wiki to more information... Or maybe you need to know How it works: https://github.com/qlixed/datascrambler/wiki/HowThisWork :) 

##A good place to Start...
###Introduction

This code allow you to encode and scramble data, what this means?, this means that you can split the original file in parts, delete some of the information and still be able to reconstruct the original data. This can be done thanks to reed-solomon alg. So you can split the data in several files and save it in different locations, you need all the minimal parts indicated to reconstruct the information, if you get less parts, you cant reconstruct the original file, and can't decrypt the data.

This have 2 basic requirements:

    PyCrypto? (NOT included in the download, so install (or easy_install) it)
    py_ecc (included in the download) 

Ok, now you can keep reading here, or go to see the TodoList
More details

Well as i say previously, you can split the original data in parts, what's the current process?, is like this:

    Encrypt the data
    Split in NUM_PARTS, calculating the parity for a minimal number of MIN_PARTS (required for reconstruction) and (if provided) delete: (NUM_PARTS-RETAIN_PARTS), if RETAIN_PARTS is not provided so we delete: (NUM_PARTS-MIN_PARTS),
    So, we get a file input and a minimun of MIN_PARTS file in the output to redistribute and hide as we like :). 

So what's next?, you can keep all the parts all you want, all the file parts if you want, but only needs MIN_PARTS to reconstruct the information.

Later we can recover the original file using all the parts that we can get (remember always needs a minumun of MIN_PARTS) and using this script.

For a beter undestanding of see https://github.com/qlixed/datascrambler/wiki/HowThisWork Even More details

More?, ok: You want to know more about this? so i "recommend" this links:

    Reed-Solomon ECC Code: Part of the magic :D - http://en.wikipedia.org/wiki/Reed-Solomon
    PY_ECC: the original page and code - http://www.mit.edu/~emin/source_code/py_ecc/ 
