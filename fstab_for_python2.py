import os
import re		

class Fstab:

	def __init__(self,file):
		self.file = file

	



	def parseFstabOnlyUUID(self):									#list only home mountpoints in array
		fstab = open(self.file,'r')
		BeforeParsArray = re.sub('[\t]',' ',fstab.read())
		BeforeParsArray = BeforeParsArray.split("\n")

		parsedArray = []

		for i in BeforeParsArray:
			if (i.find('#') == -1 and i.find('UUID') != -1 and i.find('home') != -1 ):
				BeforeParsArray = i.split(" ")
				parsedArray.append(list(filter(None,BeforeParsArray)))


		fstab.close()
		return parsedArray



	def GetHomeMountpoints(self):									#list only home number in array
		fstab = self.parseFstabOnlyUUID()
		homes = []
		
		for i in fstab:
			homes.append(i[1][1:])


		
		return homes


	def GetAllField(self):											#get all fstab fields in array without spaces and comment
		fstab = open(self.file,'r')
		FArray = re.sub('[\t]',' ',fstab.read())
		FArray = FArray.split("\n")
		MountpointArray = []

		for i in FArray:
			if (i.find('#') == -1 and i.find(' ') != -1 ):
				FArray = i.split(" ")
				MountpointArray.append(list(filter(None,FArray)))

		fstab.close()
		return MountpointArray

	def parseAllFileToArry(self):											#get all fstab fields in array
		fstab = open(self.file,'r')
		FArray = re.sub('[\t]',' ',fstab.read())
		FArray = FArray.split("\n")
		MountpointArray = []

		for i in FArray:
				FArray = i.split(" ")
				MountpointArray.append(list(filter(None,FArray)))

		fstab.close()
		return MountpointArray
		

	def GetAllMountpoints(self):									#list all mountpoints in array
		fstab = self.GetAllField()
		homes = []
		
		for i in fstab:
			homes.append(i[1][:])

		return homes

	def find(self,case):											#find somthing by mountpoint or dev
		fstab = self.GetAllField()
		self.case  = case
		result = []
		
		for i in fstab:
			try:
				if (i[0:2].index(case)+1):
					result.append(i)
			except Exception as e:
				pass
				

		if result != []:
			return result
		else:
			return 0 

	def addMountpoint(self,device_spec,mount_point,fs_type='xfs',options='_netdev,defaults,usrquota,noatime',dump=0,passF=0):							#add mount-point def value for fs_type='xfs',options='_netdev,defaults,usrquota,noatime',dump=0,passF=0
		fstab = open(self.file,'a')
																																						#can specify like: 	a.addMountpoint(device_spec="UUID=a5ced61-83d3-4b8c-b106-45251542a562a",passF=4,mount_point="/home212")			
		self.device_spec = device_spec																													#or a.addMountpoint("UUID=a5ced61-83d3-4b8c-b106-45251542a562a","/home212","xfs")
		self.mount_point = mount_point
		self.fs_type  	 = fs_type
		self.options     = options
		self.dump		 = dump
		self.passF       = passF
		

		if (self.find(self.mount_point) == 0 and self.find(self.device_spec) == 0):
			fstab.write("{}       {}  {}     {}       {}       {}\n".format(self.device_spec,self.mount_point,self.fs_type,self.options,self.dump,self.passF))
			fstab.close()
			print(("{}       {}  {}     {}       {}       {}\n".format(self.device_spec,self.mount_point,self.fs_type,self.options,self.dump,self.passF)))
			return 0 
		else:
			print('device or mount-point already axist!!!')
			fstab.close()
			return 1

	def get_line_number(self,phrase):													
		self.phrase = phrase
		self.file_name = self.file
		print(self.file_name)
		with open(self.file_name) as f:
			for i, line in enumerate (f,1):
				
				if self.phrase in re.sub('[\t]',' ',line):

					return i

	def RmMountpoint(self,dev_or_mount):
		self.dev_or_mount  = dev_or_mount
		
		if (self.find(self.dev_or_mount) != 0):

			line_number = self.get_line_number(self.dev_or_mount + " ")
			print(line_number)
			command = os.popen("sed -i '{}d' {}".format(line_number,self.file))
			command.read()
			command.close()
			print('{} removed!'.format(self.dev_or_mount))
			return 0 
		else:
			print('erorr')
			return 1 

