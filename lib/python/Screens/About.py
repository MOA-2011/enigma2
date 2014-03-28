from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Components.ScrollLabel import ScrollLabel
from Components.Button import Button

from Tools.StbHardware import getFPVersion
from Tools.HardwareInfo import HardwareInfo
from os import path as os_path
from enigma import eTimer

class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)

		from Tools.HardwareInfo import HardwareInfo
		model = HardwareInfo().get_device_name()
		if model == "optimussos2":
			AboutText = _("Hardware: ") + "OPTIMUSS OS2" + "\n"
		elif model == "optimussos1":
			AboutText = _("Hardware: ") + "OPTIMUSS OS1" + "\n"
		if model == "optimussos2plus":
			AboutText = _("Hardware: ") + "OPTIMUSS OS2+" + "\n"
		elif model == "optimussos1plus":
			AboutText = _("Hardware: ") + "OPTIMUSS OS1+" + "\n"
		else:
			AboutText = _("Hardware: ") + about.getHardwareTypeString() + "\n"

		import fcntl, socket, struct
		def getHwAddr(ifname):
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
			return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
		macaddress = getHwAddr("eth0") 
		self["MacAddress"] = StaticText(_("Mac Address:") + " " + macaddress)
		AboutText += _("Mac Address:") + " " + macaddress + "\n"

		if HardwareInfo().has_micom():
			AboutText += _("Micom Version: ") + about.getMicomVersionString() + "\n"
		AboutText += _("Image: ") + about.getImageTypeString() + "\n"
		AboutText += _("Kernel version: ") + about.getKernelVersionString() + "\n"

		EnigmaVersion = "Enigma: " + about.getEnigmaVersionString()
		self["EnigmaVersion"] = StaticText(EnigmaVersion)
		AboutText += EnigmaVersion + "\n"

		ImageVersion = _("Last upgrade: ") + about.getImageVersionString()
		self["ImageVersion"] = StaticText(ImageVersion)
		AboutText += ImageVersion + "\n"

# [iq
		if model == "mediabox":
			AboutText += _("Powered by Jepssen") + "\n"
		elif model == "optimussos1" or model == "optimussos2":
			AboutText += _("Powered by Edision") + "\n"
		else:
			AboutText += _("Powered by 4D") + "\n"
# iq]
# [iq
#		fp_version = getFPVersion()
#		if fp_version is None:
#			fp_version = ""
#		else:
#			fp_version = _("Frontprocessor version: %d") % fp_version
#			AboutText += fp_version + "\n"
#
#		self["FPVersion"] = StaticText(fp_version)
# iq]

		self["TunerHeader"] = StaticText(_("Detected NIMs:"))
		AboutText += "\n" + _("Detected NIMs:") + "\n"

		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if count < 4:
				self["Tuner" + str(count)] = StaticText(nims[count])
			else:
				self["Tuner" + str(count)] = StaticText("")
			AboutText += nims[count] + "\n"

		self["HDDHeader"] = StaticText(_("Detected HDD:"))
		AboutText += "\n" + _("Detected HDD:") + "\n"

		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				if hddinfo:
					hddinfo += "\n"
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					hddinfo += "%s\n(%s, %d GB %s)" % (hdd.model(), hdd.capacity(), hdd.free()/1024, _("free"))
				else:
					hddinfo += "%s\n(%s, %d MB %s)" % (hdd.model(), hdd.capacity(), hdd.free(), _("free"))
		else:
			hddinfo = _("none")
		self["hddA"] = StaticText(hddinfo)
		AboutText += hddinfo
		self["AboutScrollLabel"] = ScrollLabel(AboutText)
		self["key_green"] = Button(_("Translations"))
		self["key_red"] = Button(_("Latest Commits"))

		self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"red": self.showCommits,
				"green": self.showTranslationInfo,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

		self["hidden_action"] = ActionMap(["ColorActions"],
		{
			"red": self.red_action,
			"blue": self.blue_action,
			"info": self.info_action,
			"1": self.first_action,
			"2": self.second_action,
			"3": self.third_action,
		},-1)

		self.key_status = -1

	def red_action(self):
		if self.key_status == 1:
			self.key_status = 2
		else:
			self.key_status = -1

	def blue_action(self):
		if self.key_status == 2:
			from Screens.ChangeRCU import ChangeRCU
			self.session.open(ChangeRCU)
			self.close()
		else:
			self.key_status = 1

	def info_action(self):
		model = HardwareInfo().get_device_name() 
		
		if self.key_status == 1:
			self.key_status = 2
			print "info_action two"
		else:
			self.key_status = 1
			print "info_action one"

	def first_action(self):
		if self.key_status == 2:
			self.key_status = 3
			print "first_action"
		else:
			self.key_status = -1
	
	def second_action(self):
		if self.key_status == 3:
			print "second_action"
			self.key_status = 4
		else:
			self.key_status = -1 

	def third_action(self):
		if self.key_status == 4:
			print "third_action"
                        if os_path.exists("/etc/factory"):
                                return
                        else:
                                from Screens.ModeSetup import Mode4DSSetup 
                                self.session.open(Mode4DSSetup)
                                self.close()
		else:
			self.key_status == -1

	def showTranslationInfo(self):
		self.session.open(TranslationInfo)

	def showCommits(self):
		self.session.open(CommitInfo)

class TranslationInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		# don't remove the string out of the _(), or it can't be "translated" anymore.

		# TRANSLATORS: Add here whatever should be shown in the "translator" about screen, up to 6 lines (use \n for newline)
		info = _("TRANSLATOR_INFO")

		if info == "TRANSLATOR_INFO":
			info = "(N/A)"

		infolines = _("").split("\n")
		infomap = {}
		for x in infolines:
			l = x.split(': ')
			if len(l) != 2:
				continue
			(type, value) = l
			infomap[type] = value
		print infomap

		self["TranslationInfo"] = StaticText(info)

		translator_name = infomap.get("Language-Team", "none")
		if translator_name == "none":
			translator_name = infomap.get("Last-Translator", "")

		self["TranslatorName"] = StaticText(translator_name)

		self["actions"] = ActionMap(["SetupActions"],
			{
				"cancel": self.close,
				"ok": self.close,
			})

class CommitInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = ["CommitInfo", "About"]
		self["AboutScrollLabel"] = ScrollLabel(_("Please wait"))

		self["actions"] = ActionMap(["SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

		self.Timer = eTimer()
		self.Timer.callback.append(self.readCommitLogs)
		self.Timer.start(50, True)

	def readCommitLogs(self):
		urls = [ 'http://sourceforge.net/p/openpli/enigma2/feed',
			'http://sourceforge.net/p/openpli/openpli-oe-core/feed']
		commitlog = ""
		from urllib2 import urlopen
		try:
			for url in urls:
				commitlog += 80 * '-' + '\n'
				commitlog += url.split('/')[-2] + '\n'
				commitlog += 80 * '-' + '\n'
				for x in  urlopen(url, timeout=5).read().split('<title>')[2:]:
					for y in x.split("><"):
						if '</title' in y:
							title = y[:-7]
						if '</dc:creator' in y:
							creator = y.split('>')[1].split('<')[0]
						if '</pubDate' in y:
							date = y.split('>')[1].split('<')[0][:-6]
					commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'
		except:
			commitlog = _("Currently the commit log cannot be retreived - please try later again")
		self["AboutScrollLabel"].setText(commitlog)
