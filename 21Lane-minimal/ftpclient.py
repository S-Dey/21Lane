import sys, os
import ftplib
from pprint import pprint
from copy import deepcopy

# make sure port number is an integer

configFile = 'ftp-client.conf'

class FTPClient:
	def __init__(self, hostname='localhost', port=2121):
		self.hostname = hostname
		self.port = int(port)
		self.pwd = '/'
		self.filelist = None
		self.getDownloadPath()

	def ping(self):
		# return alive status
		ftp = ftplib.FTP()
		try:
			ftp.connect(host=self.hostname, port=self.port, timeout=2)
			ftp.quit()
			return True
		except Exception as e:
			raise e
			return False


	def ftplist(self):
		# remark : directory is also a file
		try:
			l = []
			ftp = ftplib.FTP()
			ftp.connect(host=self.hostname, port=self.port)
			ftp.login()
			ftp.dir(self.pwd, l.append)
			ftp.quit()
			m = deepcopy(l)
			for i in range(len(l)):
				l[i] = l[i].split()
			tmplist = {}
			for i in range(len(l)):
				# l[i] = [ x for x in l[i] if x!= '' ] # no need if using string.split(), which was string.split(' ') earlier
				isDir = l[i][0].startswith('d')
				filesize = l[i][4]
				for item in l[i][:8]:
					m[i] = m[i].replace(item, '', 1)
				filename = m[i].strip()
				tmplist[i] = {'isDir':isDir, 'filesize':filesize, 'filename':filename, 'pathname':self.pwd }
		except Exception as e:
			ftp.close()
			print('error occured')
			return None
		else:
			return tmplist

	def ftplistrecur(self, path):
		# self.ftplist should be typecasted to an empty lists
		# self.pwd has to be set to blank and absolute path should be provided
		try:
			self.pwd = path
			pprint(self.pwd)
			retval = self.ftplist()
			if not len(retval) > 0:
				return 
				# dictionary append would lose duplicate keys
			for val in list(retval.values()):
				if val['isDir']:
					self.ftplistrecur(os.path.join(path, val['filename']))
				else:
					self.filelist.append(val)
				self.pwd = path
		except Exception as e:
			raise e
			return False

	def ftprecur(self, path):
		self.pwd = ''
		self.filelist = []
		return self.ftplistrecur(path)

	def getDownloadPath(self):
		try:
			conf = open(configFile, 'r')
			self.downloadPath = conf.readline().strip()
			conf.close()
			if (len(self.downloadPath) == 0):
				raise IOError
		except IOError:
			self.downloadPath = os.path.join(os.path.expanduser('~'), 'Downloads')

	def downloadFile(self, pathname, filename, destpath=''):
		if (len(filename) == 0 or len(pathname) == 0):
			return False
		ftp = ftplib.FTP()
		if destpath.startswith('/'):
			destpath = destpath[1:]
		downloadPath = self.downloadPath
		if (destpath != ''):
			downloadPath = os.path.join(downloadPath, destpath)
			# counter = 0
			# dummy = downloadPath
			# while (os.path.exists(dummy)):
			# 	dummy = downloadPath+'_'+str(counter)
			# 	counter+=1
			# if (counter != 0):
			# 	downloadPath = dummy

			try:
				os.makedirs(downloadPath)
			except Exception as e:
				pass

		targetFile = os.path.join(downloadPath, filename)
		dummy = targetFile
		basename = os.path.splitext(targetFile)[0]
		extension = os.path.splitext(targetFile)[1]
		counter = 0
		while (os.path.exists(dummy)):
			dummy = basename+'_'+str(counter)+extension
			counter+=1
		if (counter != 0):
			targetFile = dummy

		write_stream = open(targetFile, 'wb')
		try:
			print('trying to connect to', self.hostname, self.port)
			ftp.connect(host=self.hostname, port=self.port)
			ftp.login()
			print('retrieving ', pathname,'/', filename)
			ftp.retrbinary('RETR %s' % pathname+'/'+filename, write_stream.write)
			ftp.quit()
			write_stream.close()
			return True
		except Exception as e:
			write_stream.close()
			ftp.close()
			os.remove(targetFile)
			print(pathname+'/'+filename)
			raise e
			return False

	# def downloadFolder(self, pathname, dirname):
	# 	if (len(pathname) == 0):
	# 		return False
	# 	ftp = ftplib.FTP()
	# 	self.getDownloadPath()
	# 	downloadDir = os.path.join(self.downloadPath, dirname)
	# 	try:
	# 		tries = 0
	# 		if (os.path.exists(downloadDir)):
	# 			while(os.path.exists(downloadDir+'_'+str(tries))):
	# 				tries += 1
	# 		if (tries != 0):
	# 			downloadDir += str(tries)
	# 		os.mkdir(downloadDir)
	# 		self.pwd = pathname
	# 		self.ftplist()
	# 		entrylist = [ entry for entry in list(self.filelist.values()) if not entry['isDir'] ]
	# 		files = []
	# 		for entry in entrylist:
	# 			files.append(entry['filename'])
	# 		return 
	# 	except Exception as e:
	# 		raise e




