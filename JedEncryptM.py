import os

class JedEncrypt:
	def __init__(self):

		self.base = [""" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-_=+[{]}\|;:'",<.>/?""",
		"""BA+?@ZR%O)W&Jy<K\HPo3n]=h5tFL[ekCD6|#{u(*-si}`qYUv4 wz,N$'/d0"7GM!rpQ9IXab;SmTfcl_Vx:g21j8^.~E>""",
		"""b.$ZYutPCMhIq#i8o]y+d70D;9L-_GU6|s5?1zTwgKSEn!fW*BOmJr,e%<2=k){jv& axV4Q3FcRAXp}~/H:@\>`l['N("^""",
		"""H{?Wq})X`,Koe#@-zijp*!v9n8a:DcIl=T_$bVL<&.Ur S/BO6Q[2'57%E"P;xC|R4Yf]13wku(^dF0\gZs~MhtJN>GmA+y""",
		""""vb$7-B1:}VFLxm~QE[RiXe8(_ch%'KlOM{@`tkpagZu30;zw5#Cn4Hj^PT)f*sJ+?IG26dSWU|A.\&N=D/>q9 y]!Y<or,""",
		"""^B`|lu/2mLJrStekIDPE<s~W"+5!FA8\Xb U.&)%}zfia-=0w1*?C:nQM4Y9o;c7{dqH$(_>,G]p#KR[6VZ@jyxNT3h'gvO""",
		"""NQkl}a!5L3 6:W\u<{ET_mv^wg0A#f-4;M2)|tBcGK$od"e`IH'bR*%psY~i/1Dz+,UhP[7OjCVF.nX=y>S9&?J]qxr(8Z@"""]

		self.disks = []
		for n in range(0, 100):
			self.disks = self.disks + self.base

		self.pkey = self.disks[0]

		self.pos = []
		for n in range(0, len(self.disks)-1):
			self.pos += [0]
		self.refl = 1
		self.enckey = self.disks[0][self.refl]
		for n in range(0, len(self.disks)-1):
			self.enckey += '_'

	def encrypttxt(self,s):
		with open(s) as file:
			ol = open("encrypted.txt", 'w')
			fs = ''
			for line in file:
				fs += (line[:-1] + '%$AYOLOB$%')
		fs = self.encrypt(fs)
		ol.write(fs)
		ol.close()

	def decrypttxt(self,s):
		with open(s) as file:
			ol = open("decrypted.txt", 'w')
			org = ''
			fs = []
			for line in file:
				org += line[:-1]
		org = self.decrypt(org)
		fs = org.split('%$AYOLOB$%')
		for n in range(0, len(fs)):
			if(n != len(fs)-1):
				ol.write(fs[n] + '\n')
			if(n == len(fs)-1):
				ol.write(fs[n][:-9])
		ol.close()

	def decrypttxtinconsole(self,s):
		org = s
		dec = ''
		fs = []
		org = self.decrypt(org)
		fs = org.split('%$AYOLOB$%')
		for n in range(0, len(fs)):
			if(n != len(fs)-1):
				dec += (fs[n] + '\n')
			if(n == len(fs)-1):
				dec +=(fs[n][:-9])
		return dec

	def encrypt(self,s):
		ret = ''
		shift = []
		spos = []
		pos = self.pos
		disks = self.disks
		pkey = self.pkey
		refl = self.refl
		for n in range(0,len(pos)):
			shift += [0]
			spos += [0]
			spos[n] = pos[n]
		loc = 0

		for i in range(0, len(s)):
			loc = i

			for n in range(0, len(disks)-2):
				if (n == 0):
					loc = disks[n+1].find(disks[n+2][(disks[n].find(s[loc])+ spos[n+1]) % len(pkey)]) - spos[n]
					if (loc < 0):
						loc += len(pkey)
					if (loc >= 0):
						loc = loc % len(pkey)
				if (n != 0):
					loc = disks[n+1].find(disks[n+2][(loc + spos[n+1]) % len(pkey)]) - spos[n]
					if (loc < 0):
						loc += len(pkey)
					if (loc >= 0):
						loc = loc % len(pkey)

			loc = (loc + refl) % len(pkey)

			for n in range(0, len(disks)-2):
				loc = disks[len(disks)-1-n].find(disks[len(disks)-2-n][(loc + spos[len(spos)-2-n]) % len(pkey)]) - spos[len(spos)-1-n] 
				if (loc < 0):
					loc += len(pkey)
				if (loc >= 0):
					loc = loc % len(pkey)

			for n in range(1, len(disks)-1):
				if (shift[n-1] != 0):
					if ((shift[n-1]) % len(pkey) == 0):
						shift[n] = shift[n] + 1
						shift[n-1] = 1

			shift[0] = shift[0] + 1

			for n in range(0, len(pos)):
				spos[n] = spos[n] + shift[n]

			ret += pkey[loc % len(pkey)]

		#print ret
		return ret

	def decrypt(self,s):
		ret = ''
		shift = []
		spos = []
		pos = self.pos
		disks = self.disks
		pkey = self.pkey
		refl = self.refl
		for n in range(0,len(pos)):
			shift += [0]
			spos += [0]
			spos[n] = pos[n]
		loc = 0
		for i in range(0, len(s)):
			loc = i

			for n in range(0, len(disks)-2):
				if (n == 0):
					loc = disks[n+1].find(disks[n+2][(disks[n].find(s[loc])+ spos[n+1]) % len(pkey)]) - spos[n]
				if (loc < 0):
					loc += len(pkey)
				if (loc >= 0):
					loc = loc % len(pkey)
				if (n != 0):
					loc = disks[n+1].find(disks[n+2][(loc + spos[n+1]) % len(pkey)]) - spos[n]
				if (loc < 0):
					loc += len(pkey)
				if (loc >= 0):
					loc = loc % len(pkey)

			if (loc - refl < 0):
				loc = ((loc - refl) + len(pkey) % len(pkey))
			elif (loc - refl >= 0):
				loc = (loc - refl) % len(pkey)

			for n in range(0, len(disks)-2):
				loc = disks[len(disks)-1-n].find(disks[len(disks)-2-n][(loc + spos[len(spos)-2-n]) % len(pkey)]) - spos[len(spos)-1-n] 
				if (loc < 0):
					loc += len(pkey)
				if (loc >= 0):
					loc = loc % len(pkey)

			for n in range(1, len(disks)-1):
				if (shift[n-1] != 0):
					if ((shift[n-1]) % len(pkey) == 0):
						shift[n] = shift[n] + 1
						shift[n-1] = 1

			shift[0] = shift[0] + 1

			for n in range(0, len(pos)):
				spos[n] = spos[n] + shift[n]

			ret += disks[0][loc % len(pkey)]

		#print ret
		return ret

	def key(self,s):
		pos = self.pos
		pkey = self.pkey
		if (len(s) < (len(pos)+1)):
			s += s[1:]*((len(pos)+1/len(s)) + 1)
		self.enckey = s[:len(pos)+1]
		self.refl = pkey.find(s[0])
		for n in range(0, len(pos)):
			self.pos[n] = pkey.find(s[n+1])
