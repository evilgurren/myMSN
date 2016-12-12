#coding:utf-8
import thread
import tkFileDialog
import time
import Tkinter as tk
from mysocket import *

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.ip = tk.StringVar()
		self.port = tk.StringVar()
		self.addr = tk.StringVar()
		self.addr_port = tk.StringVar()
		self.ip.set('0.0.0.0')
		self.port.set('12345')
		self.s = None
		self.data = None
		self.head = '@#@#@#%d&&&&&'
		# self.filedata = None


		self.zone1 = tk.LabelFrame(self, text='聊天区域', height=80, width=80, padx=5, pady=5)
		self.zone1.pack(side=tk.LEFT, padx=5, pady=5)
		# zone1.grid(row=0, column=0)
		self.zone2 = tk.LabelFrame(self, text='当前状态', height=80, width=80, padx=5, pady=5)
		self.zone2.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
		# zone2.grid(row=0, column=1)

		self.scrollbar = tk.Scrollbar(self.zone1)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.display_text = tk.Text(self.zone1, width=70, height=15, yscrollcommand=self.scrollbar.set)#state=tk.DISABLED)
		self.display_text.tag_config('self', foreground='green')
		self.display_text.tag_config('other', foreground='blue')
		self.display_text.tag_config('file', foreground='gray')
		self.display_text.pack(padx=5, pady=5)

		self.scrollbar.config(command=self.display_text.yview)

		self.send_text = tk.Text(self.zone1, width=70, height=6)
		# send_entry.grid(row=1, column=0)
		self.send_text.pack(padx=5, pady=5)

		self.send_button = tk.Button(self.zone1, text='发送文件', command=self.sendfile)
		self.send_button.pack(side=tk.LEFT)
		self.file_button = tk.Button(self.zone1, text='发送信息', command=self.senddata)
		self.file_button.pack(side=tk.RIGHT)
		self.quit_button = tk.Button(self.zone1, text='    退出    ', command=self.quit)
		self.quit_button.pack(side=tk.RIGHT)


		self.ip_label = tk.Label(self.zone2, text='ip:', padx=10, pady=10)
		self.ip_label.grid(row=0, column=0)
		self.port_label = tk.Label(self.zone2, text='port:', padx=10, pady=10)
		self.port_label.grid(row=1, column=0)
		self.addr_label = tk.Label(self.zone2, text='socket-ip:', padx=10, pady=10)
		self.addr_label.grid(row=2, column=0)
		self.adpo_label = tk.Label(self.zone2, text='socket-port:', padx=10, pady=10)
		self.adpo_label.grid(row=3, column=0)

		self.ip_entry = tk.Entry(self.zone2, width=20, textvariable=self.ip)
		self.ip_entry.grid(row=0, column=1)
		self.port_entry = tk.Entry(self.zone2, width=20, textvariable=self.port)
		self.port_entry.grid(row=1, column=1)
		self.addr_entry = tk.Entry(self.zone2, width=20, textvariable=self.addr, state='readonly')
		self.addr_entry.grid(row=2, column=1)
		self.adpo_entry = tk.Entry(self.zone2, width=20, textvariable=self.addr_port, state='readonly')
		self.adpo_entry.grid(row=3, column=1)

		self.c_button = tk.Button(self.zone2, text='Client', command=self.client)
		# send_button.pack(side=tk.LEFT)
		self.c_button.grid(row=4, column=0)
		self.s_button = tk.Button(self.zone2, text='Server', command=self.server)
		# send_button.pack(side=tk.RIGHT)
		self.s_button.grid(row=4, column=1, sticky=tk.E)


	def client(self):
		self.s = c_create(self.ip.get(), int(self.port.get()))
		print self.s.getsockname()
		ip, port = self.s.getsockname()
		self.addr.set(ip)
		self.addr_port.set(str(port))
		thread.start_new_thread(recvdata, (self.s, self.display_text, 'Server %s'))

	def server(self):
		self.sock = s_create(self.ip.get(), int(self.port.get()))
		print self.sock.getsockname()
		self.s, addr = self.sock.accept()
		ip, port = self.s.getsockname()
		self.addr.set(ip)
		self.addr_port.set(str(port))
		thread.start_new_thread(recvdata, (self.s, self.display_text, 'Client %s'))

	def senddata(self):
		self.data = self.send_text.get(1.0, tk.END)
		self.data = self.data.encode('utf-8')
		self.display_text.insert(tk.END, '我 %s'%time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '\n', 'self')
		self.display_text.insert(tk.END, '  ' + self.data)
		self.send_text.delete(1.0, tk.END)
		# print self.text
		send(self.s, self.data)

	def sendfile(self):
		self.path = tkFileDialog.askopenfilename()
		# with open(path, 'r') as f:
		# 	self.filedata = f.read()
		if self.path != '':
			self.data = packdata(self.path)
			if self.data == -1:
				pass
			else:
				self.display_text.insert(tk.END, '\t\t\t文件发送成功！\n', 'file')
				send(self.s, self.head%len(self.data))
				send(self.s, self.data)

if __name__ == '__main__':
	app = Application()
	app.master.title('低配MSN')
	app.master.resizable(width=False, height=False)
	app.mainloop()