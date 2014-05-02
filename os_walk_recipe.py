'''
http://code.activestate.com/recipes/578629-windows-directory-walk-using-ctypes/
UNDER MIT LICENSE
'''
import os
import sys
import ctypes
from ctypes import Structure
from ctypes import byref
import ctypes.wintypes as wintypes
from ctypes import addressof
#import logging

FILE_ATTRIBUTE_DIRECTORY = 16
OPEN_EXISTING = 3
MAX_PATH = 260

GetLastError = ctypes.windll.kernel32.GetLastError

class FILETIME(Structure):
  _fields_ = [("dwLowDateTime", wintypes.DWORD),
              ("dwHighDateTime", wintypes.DWORD)]

class WIN32_FIND_DATAW(Structure):
  _fields_ = [("dwFileAttributes", wintypes.DWORD),
              ("ftCreationTime", FILETIME),
              ("ftLastAccessTime", FILETIME),
              ("ftLastWriteTime", FILETIME),
              ("nFileSizeHigh", wintypes.DWORD),
              ("nFileSizeLow", wintypes.DWORD),
              ("dwReserved0", wintypes.DWORD),
              ("dwReserved1", wintypes.DWORD),
              ("cFileName", wintypes.WCHAR * MAX_PATH),
              ("cAlternateFileName", wintypes.WCHAR * 20)]
#in_local_ctypes, in_local_ctypes_windll_kernel32, in_local_print, in_local_WindowsError, in_local_byref, in_local_FILE_ATTRIBUTE_DIRECTORY
#def windows_walk(folder, local_ctypes=ctypes, local_ctypes_windll_kernel32=ctypes.windll.kernel32, local_print=print, local_WindowsError=WindowsError, local_byref=byref, local_FILE_ATTRIBUTE_DIRECTORY=FILE_ATTRIBUTE_DIRECTORY):
def windows_walk(folder, in_local_ctypes=ctypes, in_local_ctypes_windll_kernel32=ctypes.windll.kernel32, in_local_print=print, in_local_WindowsError=WindowsError, in_local_byref=byref, in_local_FILE_ATTRIBUTE_DIRECTORY=FILE_ATTRIBUTE_DIRECTORY, in_local_WIN32_FIND_DATAW=WIN32_FIND_DATAW):
    local_ctypes = in_local_ctypes
    local_ctypes_windll_kernel32 = in_local_ctypes_windll_kernel32
    local_print = in_local_print
    local_WindowsError = in_local_WindowsError
    local_byref = in_local_byref
    local_FILE_ATTRIBUTE_DIRECTORY=in_local_FILE_ATTRIBUTE_DIRECTORY
    #folder = str(folder)
    #print("debug: folder name: ", folder)
    #if not folder.startswith('\\\\?\\'):
        #logging.debug("%s not startswith \\\\?\\" % folder)
        #if folder.startswith('\\\\'):
            #logging.debug("\t%s startswith \\\\" % folder)
            #logging.debug("\t\tnetwork drive")
            # network drive
            #folder = '\\\\?\\UNC' + folder[1:]
        #else:
            #logging.debug("\t%s is a local drive" % folder)
            # local drive
    #folder = '\\\\?\\%s' % folder
    local_windows_walk=windows_walk
    dirs = []
    files = []
    local_WIN32_FIND_DATAW = in_local_WIN32_FIND_DATAW
    data = local_WIN32_FIND_DATAW()
    gle = 0
    #lpFileName = os.path.join(folder, '*')
    lpFileName = "%s\\%s" % (folder, '*')
    h = local_ctypes_windll_kernel32.FindFirstFileW(lpFileName, local_byref(data))#type 'int'
    #h = local_ctypes.windll.kernel32.FindFirstFileW(lpFileName, byref(data))#type 'int'
    if __debug__:
        logging.debug("type(h): %s" % str(type(h)))
        logging.debug("h: %s" % str(h))
        logging.debug("lpFileName: %s" % str(lpFileName))
    gle = local_ctypes_windll_kernel32.GetLastError()
    #gle = local_ctypes.windll.kernel32.GetLastError()
    if h < 0:
        #logging.debug("\nh (%i) < 0" % (int(h)))
        local_ctypes_windll_kernel32.FindClose(h)
        #if not sys.stderr.isatty():
            #pass
            #logging.warning('\tFailed to find first file %s' % (os.path.join(folder, '*')))
        if gle != 5: # access denied.
            #logging.debug("\t\tgle (%i) != 5" % (int(gle)))
            raise local_WindowsError('FindFirstFileW %s, Error: %d' % (folder, local_ctypes_windll_kernel32.GetLastError()))
        return
    
    
    if data.dwFileAttributes & local_FILE_ATTRIBUTE_DIRECTORY:
        if __debug__:
            logging.debug("\n\t\tdata.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY : %s - (data.dwFileAttributes, FILE_ATTRIBUTE_DIRECTORY): %s, %s" % (str(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY), str(data.dwFileAttributes), str(FILE_ATTRIBUTE_DIRECTORY)))
        #print("\tdata.cFileName: '", data.cFileName, "'")
        #print()
        #pass
        if data.cFileName not in ('.', '..'):
            if __debug__:
                logging.debug("\t\t%s not in '.' or '..'" % str(data.cFileName))
            dirs.append(data.cFileName[:])
        else:
            local_print(end='')
            #pass
            if __debug__:
                logging.debug("\t\t\tfile in '.' or '..'! fileName is: %s" % str(data.cFileName))
    else:
        files.append(data.cFileName[:])
        if __debug__:
            logging.debug("\t\t\t\tAppended : ", files[-1])

    try:
        while local_ctypes_windll_kernel32.FindNextFileW(h, local_byref(data)):
            if data.dwFileAttributes & local_FILE_ATTRIBUTE_DIRECTORY:
                if data.cFileName not in ('.', '..'):
                    if __debug__:
                        logging.debug("\t'%s' not in '.' or '..' - it must be a directory - descending directory... " %  str(data.cFileName))
                    dirs.append(data.cFileName[:])
            else:
                files.append(data.cFileName[:])
    except local_WindowsError as e:
        #if not sys.stderr.isatty():
            #local_print('Failed to find next file %s, handle %d, buff addr: 0x%x' % (("%s\\%s" % (folder, '*')), h, addressof(data)))
        #else:
        #
        sys.exit('Failed to find next file %s\\*, handle %d, buff addr: 0x%x' % (folder, h, addressof(data)))
        
    local_ctypes_windll_kernel32.FindClose(h)
    if __debug__:
        logging.debug("\tyielding folder %s:" % (str(folder)))
    #for a_dir in dirs:
        #logging.debug("\t\tdir a_dir %s:" % (str(a_dir)))
        #for a_file in files:
            #logging.debug("\t\t\tfile %s" % str(a_file))
    yield folder, dirs, files
    for d in dirs:
        #logging.debug("\n\t\td (%s) in dirs" % (str(d)))
        for base, ds, fs in local_windows_walk("%s\\%s" %(folder, d), local_ctypes, local_ctypes_windll_kernel32, local_print, local_WindowsError, local_byref, local_FILE_ATTRIBUTE_DIRECTORY, in_local_WIN32_FIND_DATAW):
            #logging.debug("\t\t\td:(%s), base:(%s), ds:(%s), fs:(%s)" % (str(d), str(base), str(ds), str(fs)))
            yield base, ds, fs


def _profile(continuation):
    prof_file = 'walk.prof'
    import cProfile
    import pstats
    #print('Profiling using cProfile')
    cProfile.runctx('continuation()', globals(), locals(), prof_file)
    stats = pstats.Stats(prof_file)
    stats.strip_dirs()
    #for a in ['calls', 'cumtime', 'cumulative', 'ncalls', 'time', 'tottime']:
    print("\n\n\n\n")
    print("------------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------------")
    for a in ['cumtime', 'ncalls']:
        print("------------------------------------------------------------------------------------------------------------------------------")
        try:
            stats.sort_stats(a)
            stats.print_stats(500)
            stats.print_callees(500)
            stats.print_callers(500)
        except KeyError:
            pass
    os.remove(prof_file)


def safe_main():
    #logging.basicConfig(level=logging.DEBUG)
    anInt = 0
    numFiles = 0
    for root, dirs, files in windows_walk(os.getcwd()):
        #logging.debug("\n\n\nroot, dirs, files: %s, %s, %s" % (str(root), str(dirs), str(files)))
        anInt += 1
        for f in files:
            numFiles += 1
            #abspath = os.path.join(root, f)
            abspath = "\t%s\\%s" % (str(root),str(f))
            try:
                #print("\t%s\\%s" % (str(root),str(f)))
                pass
            except UnicodeEncodeError:
                pass
    print(anInt)
    print(numFiles)

if __name__=='__main__':
    if sys.flags.optimize == 0:
      print("Consider running python with the '-OO' flag!")
    _profile(safe_main)
