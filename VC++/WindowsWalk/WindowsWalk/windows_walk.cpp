/*

THIS IS ___REALLY___ ALPHA

from ctypes import byref

def windows_walk(folder, 
				 in_local_ctypes_windll_kernel32=ctypes.windll.kernel32, 
				 in_local_WindowsError=WindowsError)
	local_ctypes_windll_kernel32 = in_local_ctypes_windll_kernel32
	local_byref = in_local_byref
	local_FILE_ATTRIBUTE_DIRECTORY=in_local_FILE_ATTRIBUTE_DIRECTORY
	local_windows_walk=windows_walk
	dirs = []
	files = []
	local_WIN32_FIND_DATAW = in_local_WIN32_FIND_DATAW
	data = local_WIN32_FIND_DATAW()
	gle = 0
	lpFileName = "%s\\%s" % (folder, '*')
	h = local_ctypes_windll_kernel32.FindFirstFileW(lpFileName, local_byref(data))#type 'int'
	gle = local_ctypes_windll_kernel32.GetLastError()
	if h < 0:
		local_ctypes_windll_kernel32.FindClose(h)
		if gle != 5: # access denied.
			raise local_WindowsError('FindFirstFileW %s, Error: %d' % (folder, local_ctypes_windll_kernel32.GetLastError()))
		return

	if data.dwFileAttributes & local_FILE_ATTRIBUTE_DIRECTORY:
		if data.cFileName not in ('.', '..'):
			dirs.append(data.cFileName[:])
		else:
			local_print(end='')
	else:
		files.append(data.cFileName[:])
	try:
		while local_ctypes_windll_kernel32.FindNextFileW(h, local_byref(data)):
			if data.dwFileAttributes & local_FILE_ATTRIBUTE_DIRECTORY:
				if data.cFileName not in ('.', '..'):
					dirs.append(data.cFileName[:])
			else:
				files.append(data.cFileName[:])
	except local_WindowsError as e:
		sys.exit('Failed to find next file %s\\*, handle %d, buff addr: 0x%x' % (folder, h, addressof(data)))
		
	local_ctypes_windll_kernel32.FindClose(h)
	yield folder, dirs, files
	for d in dirs:
		for base, ds, fs in local_windows_walk("%s\\%s" %(folder, d), local_ctypes, local_ctypes_windll_kernel32, local_print, local_WindowsError, local_byref, local_FILE_ATTRIBUTE_DIRECTORY, in_local_WIN32_FIND_DATAW):
			yield base, ds, fs



def safe_main():
	anInt = 0
	numFiles = 0
	for root, dirs, files in windows_walk(os.getcwd()):
		anInt += 1
		for f in files:
			numFiles += 1
			abspath = "\t%s\\%s" % (str(root),str(f))
	print(anInt)
	print(numFiles)



*/
#include <Windows.h>
#include <vector>
#include <comdef.h>
#include <tchar.h>
#include <WinBase.h>



struct walk_yield {
	WCHAR baseDirectoryPath[ MAX_PATH ];
	std::vector<WCHAR> directories;
	std::vector<WCHAR> files;
	};

int main(int argc, TCHAR *argv[] ) { 
	TCHAR* aFileName = argv[ 1 ];
	LPTSTR aName = aFileName;
	WIN32_FIND_DATA aFileData;
	HANDLE aFile = FindFirstFile(aName, &aFileData);
	if ( aFile == INVALID_HANDLE_VALUE ) {
		return 666;
		}
	else {
		printf( "Succeeded!\r\n");
		printf( _T("%s\r\n"), aFileData.cFileName);
		FindClose( aFile );
		}
	}
