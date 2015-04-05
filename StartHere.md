#A good place to Start...

# Introduction #

This code allow you to encode and scramble data, what this means?, this means that you can split the original file in parts, delete some of the information and still be able to reconstruct the original data. This can be done thanks to reed-solomon alg.
So you can split the data in several files and save it in different locations, you need all the minimal parts indicated to reconstruct the information, if you get less parts, you cant reconstruct the original file, and can't decrypt the data.

This have 2 basic requirements:
  * PyCrypto (NOT included in the download, so install (or easy\_install) it)
  * py\_ecc (included in the download)

Ok, now you can _keep reading here_, or go to see the _TodoList_

# More details #

Well as i say previously, you can split the original data in parts, what's the current process?, is like this:
  * Encrypt the data
  * Split in NUM\_PARTS, calculating the parity for a minimal number of MIN\_PARTS (required for reconstruction) and (if provided) delete: (NUM\_PARTS-RETAIN\_PARTS), if RETAIN\_PARTS is not provided so we delete: (NUM\_PARTS-MIN\_PARTS),
  * So, we get a file input and a minimun of MIN\_PARTS file in the output to redistribute and hide as we like :).

So what's next?, you can keep all the parts all you want, all the file parts if you want, but only needs MIN\_PARTS to reconstruct the information.

Later we can recover the original file using all the parts that we can get (remember always needs a minumun of MIN\_PARTS) and using this script.

For a beter undestanding of see HowThisWork


# Even More details #
_More?_, ok:
You want to know more about this? so i "recommend" this links:
  * Reed-Solomon ECC Code: Part of the magic :D - http://en.wikipedia.org/wiki/Reed-Solomon
  * PY\_ECC: the original page and code - http://www.mit.edu/~emin/source_code/py_ecc/