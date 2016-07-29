#!/usr/bin/python3

import os, shutil, sys, platform
def check_version():
	if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
		return True
	else:
		print("This version of Python may not run 21Lane. Sorry.")
		print("We are working on compatibility issues.")
		try:
			input("Press Enter to exit...")
		except:
			pass
		sys.exit(1)


# start here
check_version()
# get user home directory
# this method works for Windows as well as Linux
homedir = os.path.expanduser('~')

desktop_entry_linux = '''
[Desktop Entry]
Version=1.0
Name=21Lane
Comment=Share data between computers on your network over FTP.
Exec=$MAINDIR$/21lane.sh
Icon=$MAINDIR$/icons/favicon.ico
Terminal=false
Type=Application
Categories=Utility;Application;

'''

desktop_entry_windows = '''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "$DESKTOPDIR$\21lane.LNK"
Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "$MAINDIR$\21lane.bat"
 '  oLink.Arguments = ""
 '  oLink.Description = "21Lane"   
 '  oLink.IconLocation = "$MAINDIR$\icons\favicon.ico, 2"
 '  oLink.WindowStyle = "1"   
 '  oLink.WorkingDirectory = "$MAINDIR$"
oLink.Save

'''


# destination directory
destdir = os.path.join(homedir, '21Lane')
if (os.path.isdir(destdir)):
	print("21Lane is already installed. Press 'n' to remove it.")
	reply = input("Press any other key and enter to continue : ")
	if (reply == 'n' or reply == 'N'):
		shutil.rmtree(destdir)
		print("21Lane removed from ", destdir)
		if (sys.argv[1] == 'uninstall')
			try:
				input("Press Enter to exit...")
			except:
				pass
			sys.exit(0)

	else:
		print("Setup ends.")
		try:
			input("Press Enter to exit...")
		except:
			pass
		sys.exit(0)

# # create directory and copy all contents
shutil.copytree(os.path.join(os.getcwd(),'21Lane'), destdir)
required_files = ['log.txt', 'snapshot.json', 'user_database.json', 'settings.json']
for file in required_files:
	f = open(os.path.join(destdir, file), 'w')
	f.close()


if 'linux' in platform.platform().lower():
	# create menu entry
	f = open('~/.local/share/applications/21Lane.desktop')
	desktop_entry_linux = desktop_entry_linux.replace("$MAINDIR$", destdir)
	f.write(desktop_entry_linux)
	f.close()
	shutil.copy2('21lane.sh', destdir)
	os.system('chmod +x '+destdir+'/21lane.sh')
	os.system('chmod +x ~/.local/share/applications/21Lane.desktop')

elif 'windows' in platform.platform().lower():
	# create vbscript file to create desktop shortcut
	f = open('create_shortcut.vbs')
	desktop_entry_windows = desktop_entry_windows.replace("$MAINDIR$", destdir)
	desktop_entry_windows = desktop_entry_windows.replace("$DESKTOPDIR$", os.path.join(homedir,'Desktop'))
	f.write(desktop_entry_windows)
	f.close()
	os.system("cscript create_shortcut.vbs")
	os.remove("create_shortcut.vbs")

	# create start menu entry
	# todo for next version
	shutil.copy2('21lane.bat', destdir)

