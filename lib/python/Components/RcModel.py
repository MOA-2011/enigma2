import os

class RcModel:
	RCTYPE_DMM = 0
	RCTYPE_IOS100 = 1
	RCTYPE_IOS200 = 2
	RCTYPE_IOS300 = 3
	RCTYPE_TMTWIN = 4
	RCTYPE_TM2T = 5
	RCTYPE_TMSINGLE = 6
	RCTYPE_TMNANO = 7
	RCTYPE_MEDIABOX = 8
	RCTYPE_FORCE1 = 9
	RCTYPE_TMNANOSUPER = 10
	RCTYPE_TM2TSUPER = 11
	RCTYPE_OPTIMUSSOS1 = 12
	RCTYPE_OPTIMUSSOS2 = 13
	RCTYPE_TMNANO2T = 14
	RCTYPE_OPTIMUSSOS1PLUS = 15
	RCTYPE_OPTIMUSSOS2PLUS = 16
	RCTYPE_FORCE1PLUS = 17
	RCTYPE_FORCE2 = 18
	RCTYPE_TMNANO2TSUPER = 19

	def __init__(self):
		self.currentRcType = self.RCTYPE_DMM
		self.readRcTypeFromProc()

	def rcIsDefault(self):
		if self.currentRcType != self.RCTYPE_DMM:
			return False
		return True

	def readFile(self, target):
		fp = open(target, 'r')
		out = fp.read()
		fp.close()
		return out.split()[0]
#[iq
	def readRcTypeFromProc(self):
		if os.path.exists('/proc/stb/info/hwmodel'):
			model = self.readFile('/proc/stb/info/hwmodel')
			if model == "tmtwinoe":
				self.currentRcType = self.RCTYPE_TMTWIN
			elif model == "ios100hd":
				self.currentRcType = self.RCTYPE_IOS100
			elif model == "ios200hd":
				self.currentRcType = self.RCTYPE_IOS200
			elif model == "ios300hd":
				self.currentRcType = self.RCTYPE_IOS300
			elif model == "tm2toe":
				self.currentRcType = self.RCTYPE_TM2T
			elif model == "tmsingle":
				self.currentRcType = self.RCTYPE_TMSINGLE
			elif model == "tmnanooe":
				self.currentRcType = self.RCTYPE_TMNANO
			elif model == "mediabox":
				self.currentRcType = self.RCTYPE_MEDIABOX
			elif model == "force1":
				self.currentRcType = self.RCTYPE_FORCE1
			elif model == "force1plus":
				self.currentRcType = self.RCTYPE_FORCE1PLUS
			elif model == "force2":
				self.currentRcType = self.RCTYPE_FORCE2
			elif model == "tmnanosuper":
				self.currentRcType = self.RCTYPE_TMNANOSUPER
			elif model == "tmnano2super":
				self.currentRcType = self.RCTYPE_TMNANO2SUPER
			elif model == "tm2tsuper":
				self.currentRcType = self.RCTYPE_TM2TSUPER
			elif model == "optimussos1":
				self.currentRcType = self.RCTYPE_OPTIMUSSOS1
			elif model == "optimussos2":
				self.currentRcType = self.RCTYPE_OPTIMUSSOS2
			elif model == "tmnano2t":
				self.currentRcType = self.RCTYPE_TMNANO2T
			elif model == "optimussos1plus":
				self.currentRcType = self.RCTYPE_OPTIMUSSOS1PLUS
			elif model == "optimussos2plus":
				self.currentRcType = self.RCTYPE_OPTIMUSSOS2PLUS

		elif os.path.exists('/proc/stb/info/boxtype'):
			model = self.readFile('/proc/stb/info/boxtype')
			if model.startswith('et') or model.startswith('xp'):
				rc = self.readFile('/proc/stb/ir/rc/type')
				if rc == '4':
					self.currentRcType = self.RCTYPE_DMM
				elif rc == '6':
					self.currentRcType = self.RCTYPE_DMM

	def getRcLocation(self):
		if self.currentRcType == self.RCTYPE_TMTWIN:
			return '/usr/share/enigma2/rc_models/tm/tmtwinoe/'
		elif self.currentRcType == self.RCTYPE_IOS100:
			return '/usr/share/enigma2/rc_models/tm/ios100/'
		elif self.currentRcType == self.RCTYPE_IOS200:
			return '/usr/share/enigma2/rc_models/tm/ios200/'
		elif self.currentRcType == self.RCTYPE_IOS300:
			return '/usr/share/enigma2/rc_models/tm/ios300/'
		elif self.currentRcType == self.RCTYPE_TM2T:
			return '/usr/share/enigma2/rc_models/tm/tm2toe/'
		elif self.currentRcType == self.RCTYPE_TMSINGLE:
			return '/usr/share/enigma2/rc_models/tm/tmsingle/'
		elif self.currentRcType == self.RCTYPE_TMNANO:
			return '/usr/share/enigma2/rc_models/tm/tmnanooe/'
		elif self.currentRcType == self.RCTYPE_MEDIABOX:
			return '/usr/share/enigma2/rc_models/tm/mediabox/'
		elif self.currentRcType == self.RCTYPE_FORCE1:
			return '/usr/share/enigma2/rc_models/tm/force1/'
		elif self.currentRcType == self.RCTYPE_FORCE1PLUS:
			return '/usr/share/enigma2/rc_models/tm/force1plus/'
		elif self.currentRcType == self.RCTYPE_FORCE2:
			return '/usr/share/enigma2/rc_models/tm/force2/'
		elif self.currentRcType == self.RCTYPE_TMNANOSUPER:
			return '/usr/share/enigma2/rc_models/tm/tmnanosuper/'
		elif self.currentRcType == self.RCTYPE_TMNANO2TSUPER:
			return '/usr/share/enigma2/rc_models/tm/tmnano2tsuper/'
		elif self.currentRcType == self.RCTYPE_TM2TSUPER:
			return '/usr/share/enigma2/rc_models/tm/tm2tsuper/'
		elif self.currentRcType == self.RCTYPE_OPTIMUSSOS1:
			return '/usr/share/enigma2/rc_models/tm/optimussos1/'
		elif self.currentRcType == self.RCTYPE_OPTIMUSSOS2:
			return '/usr/share/enigma2/rc_models/tm/optimussos2/'
		elif self.currentRcType == self.RCTYPE_OPTIMUSSOS1PLUS:
			return '/usr/share/enigma2/rc_models/tm/optimussos1plus/'
		elif self.currentRcType == self.RCTYPE_OPTIMUSSOS2PLUS:
			return '/usr/share/enigma2/rc_models/tm/optimussos2plus/'
		elif self.currentRcType == self.RCTYPE_TMNANO2T:
			return '/usr/share/enigma2/rc_models/tm/tmnano2t/'
rc_model = RcModel()
