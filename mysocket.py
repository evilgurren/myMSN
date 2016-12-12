#coding:utf-8
import socket
import os
import struct
import re
import time
import Tkinter as tk
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES
KEY = 'f3489f0jfi2o3jfy'
MODE = AES.MODE_CBC

def s_create(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(1)
	return s

def c_create(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	return s

def send(s, data):
	ciphertext = encrypt(data)
	s.sendall(ciphertext)

def recvdata(s, showtext, name):
	s.setblocking(0)
	buff = ''
	buff_file = ''
	ciphertext = ''
	cipherbuff = ''
	cipherfile = ''
	size = 0
	while True:
		try:
			ciphertext = s.recv(4096)
		except socket.error, e:
			pass
		if ciphertext != '':
			cipherbuff += ciphertext
			ciphertext = ''
		elif cipherbuff != '':
			buff = decrypt(cipherbuff)
			cipherbuff = ''
			r = re.search('@#@#@#(\d+)&&&&&', buff)
			if r:
				while True:
					try:
						ciphertext = s.recv(int(r.group(1)))
					except socket.error, e:
						pass
					if ciphertext != '':
						cipherfile += ciphertext
						time.sleep(0.001)
						ciphertext = ''
					else:
						buff_file = decrypt(cipherfile)
						if len(buff_file) == int(r.group(1)):
							break
				data, filename = unpackdata(buff_file)
				buff = ''
				buff_file = ''
				cipherfile = ''
				filename = filename.decode('utf-8')
				with open(filename, 'wb') as f:
					f.write(data)
				showtext.insert(tk.END, '\t\t\t文件接收成功！\n', 'file')
			else:
				text = name%time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+ '\n'
				showtext.insert(tk.END, text, 'other')
				showtext.insert(tk.END, '  ' + buff)
				buff = ''

def packdata(path):
	filename = os.path.basename(path).encode('utf-8')
	with open(path, 'rb') as f:
		filedata = f.read()
	format = '%ds%ds' % (len(filedata), len(filename))
	if len(format) < 20:
		data = struct.pack(format, filedata, filename)
		for i in range(20 - len(format)):
			format += '#'
		return format + data
	else:
		return -1

def unpackdata(buff):
	head, p_data = buff[:20], buff[20:]
	m = re.match('^\d+s\d+s#+$', head)
	# if m:
	format = re.search('\d+s\d+s', m.string).group()
	# print format, len(p_data)
		# filedata, filename = struct.unpack(format, p_data)
	return (struct.unpack(format, p_data))

def encrypt(text):
	cryptor = AES.new(KEY, MODE, b'0000000000000000')
	length = 16
	size = len(text)
	add = length - (size % length)
	text += ('\0' * add)
	ciphertext = cryptor.encrypt(text)
	return b2a_hex(ciphertext)

def decrypt(text):
	cryptor = AES.new(KEY, MODE, b'0000000000000000')
	plaintext = cryptor.decrypt(a2b_hex(text))
	return plaintext.rstrip('\0')