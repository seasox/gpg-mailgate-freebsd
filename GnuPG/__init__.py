import os
import subprocess

# This is a fork of gpg-mailgate (https://code.google.com/p/gpg-mailgate/)
# This software is licensed under the GNU GPLv3 license: https://www.gnu.org/licenses/gpl.html
# January 9th 2014

def public_keys( keyhome ):
	cmd = '/usr/local/bin/gpg --homedir %s --list-keys --with-colons' % keyhome
	p = subprocess.Popen( cmd.split(' '), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	p.wait()
	keys = list()
	for line in p.stdout.readlines():
		if line[0:3] == 'uid':
			key = line.split('<')[1].split('>')[0]
			if keys.count(key) == 0:
				keys.append(key)
	return keys

class GPGEncryptor:
	def __init__(self, keyhome, recipients = None):
		self._keyhome = keyhome
		self._message = ''
		self._recipients = list()
		if recipients != None:
			self._recipients.extend(recipients)

	def update(self, message):
		self._message += message

	def encrypt(self):
		p1 = subprocess.Popen( ["echo", self._message ], stdout=subprocess.PIPE)
		p2 = subprocess.Popen( self._command(), stdin=p1.stdout, stdout=subprocess.PIPE)

		encdata = p2.communicate()[0]
		return encdata

	def _command(self):
		cmd = "/usr/local/bin/gpg --homedir %s --no-version --trust-model always --armor --batch --yes --pgp7 --no-secmem-warning --encrypt --recipient %s" % (self._keyhome, '--recipient ' .join(self._recipients))
		return cmd.split()
