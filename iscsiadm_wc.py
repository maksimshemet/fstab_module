class Iscsiadm(object):
	"""manipulate with iscsi"""
	def __init__(self, portal):
		self.portal = portal
		

	def discovering(self, iqn_unik):
		self.iqn_unik = iqn_unik

		command = os.popen("iscsiadm -m node -T $(iscsiadm -m discovery -t st -p {} | awk -F ' '".format(self.portal) + " '{print $2}' " + "| grep {} ) --login".format(self.iqn_unik))
		result = command.read()
		command.close()
		print(result)

		return result

	def getDevice(self,iqn_unik):
		self.iqn_unik = iqn_unik
		
		command = os.popen("ls -l /dev/disk/by-path/ | grep $(iscsiadm -m discovery -t st -p {} | awk -F ' '".format(self.portal) + " '{print $2}' " + "| grep {} ) ".format(self.iqn_unik) + "| awk -F '/' '{print $3}' ")
		result = command.read()
		command.close()
		
		return result

 	def getUUID(self,iqn_unik):																									#home should be exist or be fatal error=)
    	self.iqn_unik = iqn_unik
    	dev = self.getDevice(self.iqn_unik)
    	dev = re.sub('[\n]',' ',dev)
    	command = os.popen("ls -l /dev/disk/by-uuid/ | grep {} | awk -F ' ' ".format(dev)+"'{print $9}' 2>/dev/null ")
    	result = command.read()
    	result = re.sub('[\n]',' ',result)
    	command.close()

    	return result 
