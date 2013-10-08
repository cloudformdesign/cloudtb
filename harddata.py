#!/usr/bin/python
# -*- coding: utf-8 -*-
#    The MIT License (MIT)
#    
#    Copyright (c) 2013 Garrett Berg cloudformdesign.com
#    An updated version of this file can be found at:
#    https://github.com/cloudformdesign/cloudtb
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#    
#    http://opensource.org/licenses/MIT
"""
This module was created to realize the potential of "hard data", or data
stored on the harddrive, for memory management and speed.

When I talk of speed, I am not talking computation  s per second in a
hypothetical universe. What I'm talking about is the same kind of speed
that python relies on -- the user of your program.

Most data is hardly ever accessed. For the rare instances you actually need
data RIGHT NOW (and lots of it), the best thing you can do is use iterators.
The module iterables.py aims to give that to you.

For other data you would be better off storing it in a file. I don't know
how many times I have written the code.

For local variales inside of functions, this doesn't really apply -- but for
most object variables they should almost ALWAYS be stored in a file instead.

Here's the wonderful thing about file access -- it's slow, and python knows
it's slow. While you're program is busy taking 100 times longer to pull your
large variable from a file, the rest of your computer can be operating that
much faster.


"""
import sys, os
import pdb
import dbe
import cPickle
import time
    
import tempfile

import system
import textools
import re

'''
mkdtemp(sufix = '.hd', prefix = 'pyhdd08234', dir = )
I want to use mkdtemp to create the temporary directory
a special file named 'timeout' will be created in it

f, path = mkstemp(suffix = '.hd', prefix='hd', dir = path)
'''



THREAD_HANDLED = False
THREAD_PERIOD = 30 # How often the therad runs in seconds
DELETE_TMP_AFTER = 60*60    # deletes unupdated temporary files if their
                            # timer file is not updated in an hour

#ga = harddata_base.__getattribute__
#sa = harddata_base.__setattr__
ga = object.__getattribute__
sa = object.__setattr__

# DO NOT MODIFY THESE
TIMER_FILE = 'pytimer.time'     # DO NOT CHANGE
TEMP_DIRECTORY = None
_HARDDATA = []

STR_TEMP_PREFIX = 'pyhdd08234'
STR_TEMP_SUFIX = '.hd'
tmp_regexp = (textools.convert_to_regexp(STR_TEMP_PREFIX) +
                r'(.*?)' +
              textools.convert_to_regexp(STR_TEMP_SUFIX))
tmp_regexp = re.compile(tmp_regexp)

def create_harddata_thread():
    global THREAD_harddata
    from errors import ModuleError
    try:
        THREAD_harddata
    except NameError:
        raise ModuleError

    from threading import Thread
    
    class harddata_thread(Thread):
        def __init__(self, harddata):
            self.harddata = harddata
            self.last_run = time.time()
            Thread.__init__(self)
            
        def run(self):
            while True:
                start_time = time.time()
                last_run = self.last_run()
                for hd in _HARDDATA:
                    hd._check(time.time())
                self.last_run = time.time()
                if self.last_run - start_time > THREAD_PERIOD:
                    # TODO: change this to logging. Here for debug
                    assert(0)
                else:
                    time.sleep(self.last_run - start_time)
                manage_temp_dirs()
        
    THREAD_harddata = harddata_thread(_HARDDATA)

def create_temp_directory():
    global TEMP_DIRECTORY
    tmpdir = tempfile.mkdtemp(sufix = '.hd', prefix = STR_TEMP_PREFIX, 
                              dir = system.get_temp_directory())
    TEMP_DIRECTORY = tmpdir
    manage_temp_dirs()

def check_timer(folder_path):
    timer_path = os.path.join(TEMP_DIRECTORY, TIMER_FILE)
    if time.time() - os.path.getatime(timer_path) > DELETE_TMP_AFTER:
        import shutil
        shutil.rmtree(folder_path, onerror = )
    
def manage_temp_dirs():
    update_timer_file()
    temp_folders = (n for n in os.listdir(system.get_temp_directory()) 
            if tmp_regexp.match(tmpf))
    for tmpf in temp_folders:
        
        
    
    
def update_timer_file():
    '''updates the file timer so that external python processes don't
    delete the temp data'''
    global TEMP_DIRECTORY
    with open(os.path.join(TEMP_DIRECTORY, TIMER_FILE), 'w') as f:
        f.write(time.ctime(time.time()))
    
def _program_this_for_me():
    '''Automatically codes the harddata_base and stores
    it in extra/harddata_base'''
    import __builtin__
    myset = set(['next'])
    for n in dir(__builtin__):
        if n != 'print':
            myset.update(dir(eval(n)))
    
    # writing for both python 2 and 3...
    fset_path = os.path.join('extra', 'std_object_member_functions.txt')
    if os.path.exists(fset_path):
        with open(fset_path) as f:
            fset = set([l.strip() for l in f])
        myset.update(fset)    
    with open(fset_path, 'w') as f:
        f.write('\n'.join(myset))

    custom = set([
              '__init__',
              '__new__',
              '__getattribute__',
              '__doc__',
              '__repr__',
              '__str__',
              '__delete__'
             ])
    
    filtered = []
    for n in myset:
        if '__' in n and n not in custom:
            filtered.append(n)
    
    filtered.sort()
    
    
    txt_format = '''
    def {name}(self, *args, **kwargs):
        print "{name}: ", args, kwargs
        return self._get_harddata().{name}(*args, **kwargs)'''
    code = []
    for n in filtered:
        code.append(txt_format.format(name = n))
    
    code_txt = 'class harddata_base(object):' + '\n'.join(code)
    
    with open(os.path.join('extra', 'harddata_base.py'), 'w') as f:
        f.write(code_txt)
    
    print "Updated hardata_base"
#    print code_txt
        

_program_this_for_me()

hd = harddata(range(100))
print hd[10]
print hd[10]

hda = harddata(10)
hdb = harddata(14)

print 'adding', hda + hdb

if __name__ == '__main__':
    pass
    # Automatically programs the base function
#    
