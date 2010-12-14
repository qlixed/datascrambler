'''
=== scrambler.py ===

@author: QliXed [aka QliX=D!, EHB]
@contact: qlixed_at_gmail_dot_com
'''
from scrambler import Scrambler
from os.path import getsize
import os

def process_size(deleteparts, parts, minparts):
    scrblr = Scrambler()
    file = 'C:\Documents and Settings\eb020653\My Documents\workspace\datascrambler\scrambler\\100bytes.txt'
    data = scrblr.scramble_it(file, deleteparts=deleteparts, parts=parts, minparts=minparts, securedelete=False)
    result = scrblr.unscramble_it(filenames=data, newfilename="rec_100bytes.txt")
    #print result
    sizes = list()
    scrambled_size = 0
    for filepart in data:
        filepart_size = getsize(filepart)
        scrambled_size += filepart_size
        sizes.append(filepart_size)
    original_size = getsize(file)
    return """{0};{1};{2};{3};""".format(original_size, str(sizes[0]), scrambled_size, ((scrambled_size - original_size) / float(original_size)) * 100)
    #print """
    #Original size={0} bytes
    #Parts sizes={1} bytes
    #Scrambled size={2} bytes
    #Ratio= {3} % extra 
    #Ratio is : ((Scrambled size-Original size)/Original size)*100)
    #""".format(original_size, str(sizes), scrambled_size, ((scrambled_size-original_size)/float(original_size))*100)

def process_timeit(deleteparts, parts, minparts):
    scrblr = Scrambler()
    files = list()
    files.append('C:\Documents and Settings\eb020653\My Documents\workspace\datascrambler\scrambler\scrambler.py')
    files.append('C:\Documents and Settings\eb020653\My Documents\My ISOs\ubuntu-10.04-server-i386.iso')
    files.append('C:\Documents and Settings\eb020653\My Documents\lib\Core Python Programming (2006).pdf')
    files.append('C:\Downloads\Video\sintel-2048-surround.mp4')
    files.append('C:\Downloads\Software\steelstorm-ep1-v10001723.exe')
    for file in files:
        data = scrblr.scramble_it(file, deleteparts=deleteparts, parts=parts, minparts=minparts, securedelete=False)
        result = scrblr.unscramble_it(filenames=data, newfilename="pyscrambler.py")
    #print result

if __name__ == '__main__':
    """
    max=10
    for i in xrange(max-1):
        for k in xrange(max-1-i):
            #print "------------------------------------------------"
            #print "Going with ", i
            #process(deleteparts=k+1, parts=max, minparts=i+1)
            #print "------------------------------------------------"
            print str(i+1)+";"+str(k+1)+";"+process_size(deleteparts=k+1, parts=max, minparts=i+1)
    """
    import sys
    from timeit import Timer
    import os
    from hotshot import Profile
    #sys.exit(0)
    timer_info = list()
    timer_result = None
    setupbase = """
from scrambler import Scrambler 
scrblr=Scrambler()
file='@replaceme@'
"""
    statm = """
data = scrblr.scramble_it(file,deleteparts=6, parts=10, minparts=4, securedelete=False)
"""
    file = 'C:\Documents and Settings\eb020653\My Documents\workspace\datascrambler\scrambler\scrambler.py'
    print 'Starting with ', file
    t = Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    print file + ':'
    file = os.path.normpath('C:\Documents and Settings\eb020653\Desktop\doxygen_manual-1.6.1.pdf')
    timer_result = t.repeat(repeat=10, number=1)
    timer_info.append([('scramble', os.path.basename(file), tr) for tr in timer_result])
    print timer_result
    print 'Starting with ', file
    t = Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    timer_result = t.repeat(repeat=10, number=1)
    timer_info.append([('scramble', os.path.basename(file), tr) for tr in timer_result])
    print timer_result
    print '------------------------------'
    print 'Hotshooting:'
    print setupbase.replace('@replaceme@', file) + statm
    p = Profile(logfn='scramble_doxygen.log')
    p.run(setupbase.replace('@replaceme@', file) + statm)
    p.close()
    file = 'C:\Documents and Settings\eb020653\My Documents\lib\Core Python Programming (2006).pdf'
    print 'Starting with ', file
    t = Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    print file + ':'
    print t.repeat(repeat=1, number=1)
    '''
    file='C:\Downloads\Software\steelstorm-ep1-v10001723.exe'
    print 'Starting with ', file
    t=Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    print file+':'
    print t.repeat(repeat=3, number=3)
    file='C:\Downloads\Video\sintel-2048-surround.mp4'
    print 'Starting with ', file
    t=Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    print file+':'
    print t.repeat(repeat=3, number=3)
    file='C:\Documents and Settings\eb020653\My Documents\My ISOs\ubuntu-10.04-server-i386.iso'
    print 'Starting with ', file
    t=Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    print file+':'
    print t.repeat(repeat=3, number=3)
    '''
    setupbase = """
from scrambler import Scrambler 
scrblr=Scrambler()
files=list()
files.append('doxygen_manual-1.6.1.pdf_scrambled.p_0')
files.append('doxygen_manual-1.6.1.pdf_scrambled.p_1')
files.append('doxygen_manual-1.6.1.pdf_scrambled.p_3')
files.append('doxygen_manual-1.6.1.pdf_scrambled.p_9')
"""
    statm = """
scrblr.unscramble_it(files,'doxygen_manual-1.6.1.pdf')
"""
    print 'Recovering data times:'
    t = Timer(stmt=statm, setup=setupbase.replace('@replaceme@', file))
    timer_result = t.repeat(repeat=10, number=1)
    timer_info.append([('unscramble', os.path.basename(file), tr) for tr in timer_result])
    print timer_result
    print '------------------------------'
    print 'Hotshooting:'
    p = Profile(logfn='unscramble_doxygen.log')
    p.run(setupbase + statm)
    p.close()
    print timer_info
    print "\r\n".join([";".join(tr) for tr in timer_info])
    
    #result = scrblr.unscramble_it(filenames=data, newfilename="pyscrambler.py")
