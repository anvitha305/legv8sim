import toml
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scrollframe import *
import interpreter
import ast
import logging
import sys
global filename
global darkMode
global parsed
global tabl
global errors
global blankSpace
global logger
global progFile
global app
global logfilename
global confFile

class AssemblySimApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		global darkMode
		global tabl
		global errors
		global filename 
		global blankSpace
		global confFile
		global progFile
		errors = ""
		filename =""
		tk.Tk.__init__(self, *args, **kwargs)
		self.title = "legv8 assembly simulator"
		self.geometry("1000x700+200+200")
		self.style = ttk.Style(self.master)
		self.style.configure("My.TLabel", font=('Arial', 20))
		self.style.configure("Cont.TLabel", font=('Arial', 15))
		self.style.configure("TEntry", font=('Arial', 15))
		self.style.configure("TButton", font=('Arial, 15'))
		self.label1 = ttk.Label(text="File View", style="My.TLabel")
		self.label1.grid(row=0, column = 0, padx=10, pady=10)
		self.button1 = ttk.Button(text="Dark Mode", command=self.darkMode)
		self.button1.grid(row = 0, column = 1, padx=10, pady=10)
		self.button2 = ttk.Button(text="Light Mode", command=self.lightMode)
		self.button2.grid(row = 0, column = 2, padx=10, pady=10)
		self.button3 = ttk.Button(text = "Open File", command = self.browseFiles) 
		self.button3.grid(row=0, column=3,padx=10,pady=10)
		self.button4 = ttk.Button(text="Step", command = self.update)
		self.button4.grid(row=0, column=4,padx=10,pady=10)
		self.button5 = ttk.Button(text="Reset", command = self.restart)
		self.button5.grid(row=0, column=5,padx=10,pady=10)
		self.label2 = ttk.Label(text = "File to be simulated:", style="Cont.TLabel")
		self.label2.grid(row=1, column=0, padx=10,pady=10, columnspan = 6, sticky = tk.W+tk.E)
		self.label3 = ttk.Label(text="Registers View", style="My.TLabel")
		self.label3.grid(row=3, column=0,padx=10,pady=10, columnspan = 6, sticky = tk.W+tk.E)
		self.frame = tk.Frame()
		self.frame.grid(row=4, column=0, columnspan = 6)
		self.sf1 = ScrollFrame(self.frame)
		my_list = [("x"+str(i), 0) for i in range(32) ]
		tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
		self.regis =Table(self.sf1.viewPort, tabl, updateRegisters)
		self.sf1.grid(row=4, column=0,padx=1,pady=1, columnspan = 6)
		self.label3 = ttk.Label(text="Memory View", style="My.TLabel")
		self.label3.grid(row=5, column=0,padx=10,pady=10)
		self.frame2 = tk.Frame()
		self.sf = ScrollFrame(self.frame2)
		self.frame2.grid(row=6, column=0,padx=0,pady=0, columnspan = 6)
		self.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 6)
		self.label4 = ttk.Label(text="Error View", style="My.TLabel")
		self.label4.grid(row=7, column=0,padx=10,pady=10, columnspan = 6, sticky = tk.W+tk.E)
		self.frame3 = tk.Frame()
		self.sf2 = ScrollFrame(self.frame3)
		self.frame3.grid(row=8, column=0,padx=0,pady=0, columnspan = 6)
		self.sf2.grid(row=8, column=0,padx=1,pady=1, columnspan = 6)
		self.memor = Table(self.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
		self.memor.e1 = ttk.Entry(self.sf.viewPort, style="TEntry")
		self.memor.e2 = ttk.Entry(self.sf.viewPort, style="TEntry")
		self.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
		self.memor.e1.grid(row=len(interpreter.mem), column=0)
		self.memor.e2.grid(row=len(interpreter.mem), column=1)
		self.label5 = ttk.Label(text="", style="My.TLabel")
		self.label5.grid(row=9, column = 0,padx=1,pady=1, columnspan = 6)
		darkMode = False
		blankSpace = False
		confFile = ""
		progFile = ""
	def darkMode(self):
		global darkMode	
		global logger
		self.configure(bg='black')
		self.style.configure("TLabel", background="black",foreground="white")
		self.style.configure("TFrame", background="black",foreground="white")
		self.sf.viewPort.configure(bg='black')
		self.sf1.viewPort.configure(bg='black')
		self.sf2.viewPort.configure(bg='black')
		try:
			logger.info("dark mode")
			self.labelcont.configure(bg="black",fg="white")
		except Exception as e:
			pass
		darkMode = True
	def lightMode(self):
		global darkMode
		global logger
		self.configure(bg='white')
		self.style.configure("TLabel", background="white", foreground="black")
		self.style.configure("TFrame", background="white",foreground="black")
		self.sf.viewPort.configure(bg='white')
		self.sf1.viewPort.configure(bg='white')
		self.sf2.viewPort.configure(bg='white')
		try:
			self.labelcont.configure(bg="white",fg="black")
			logger.info("light mode")
		except Exception as e:
			pass
		darkMode = False
	def browseFiles(self):
		global darkMode
		global parsed
		global errors
		global filename
		global logger
		global progFile
		global confFile
		filename = tk.filedialog.askopenfilename(initialdir = "-",title = "Select a legv8 (.s, .legv8) file to run",filetypes = (("Assembly","*.s"), ("LEGV8","*.legv8"),("Config Files", "*.conf"),("All Files","*.*")))
		if filename.endswith(".conf"):
			confFile = filename
			if len(progFile) > 0:
				try:
					logger.info("using conf file + " + confFile)
				except Exception as e:
					pass
			for widget in app.sf.viewPort.winfo_children():
				widget.destroy()
			interpreter.registers = dict(zip(["x"+str(i) for i in range(0,32)],[0]*32))
			interpreter.flags={"n":0, "c":0, "z":0, "v":0}
			interpreter.mem = dict()
			data = toml.load(filename)
			for i in data["registers"].keys():
				interpreter.registers[i] = data["registers"][i]
			#print(data["memory"])
			for j in data["memory"].keys():
				try:
					if int(j)%4 == 0:
						interpreter.mem[j] = data["memory"][j]
				except Exception as e:
					errors+= "Error with memory value " + str(data["memory"][j]) + "\n"
					self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
					self.labelError.grid(row =0,column=0)
					self.sf2.canvas.update_idletasks()
					self.sf2.canvas.yview_moveto(1.0)

					
			#print(interpreter.registers)
			my_list = [(k, v) for k, v in interpreter.registers.items()]
			tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
			self.regis =Table(self.sf1.viewPort, tabl, updateRegisters)
			self.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 6)
			self.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
			self.memor.e1 = ttk.Entry(app.sf.viewPort, style="TEntry")
			self.memor.e2 = ttk.Entry(app.sf.viewPort, style="TEntry")
			self.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
			self.memor.e1.grid(row=len(interpreter.mem), column=0)
			self.memor.e2.grid(row=len(interpreter.mem), column=1)
			return
		try:
			self.labelfile.destroy()
			self.labelcont.destroy()
			self.label5.destroy()
		except Exception as e:
			pass
		try:
			file = open(filename)
			if not (filename.endswith(".s") or filename.endswith(".legv8")):				raise Exception()
		except Exception as e:
			errors+= "Open a valid LEGV8 file before stepping through!\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)
		progFile = filename
		logging.basicConfig(filename=progFile+".log",format='%(asctime)s %(message)s',filemode='a', level=logging.INFO)
		logger = logging.getLogger()
		logger.info("opened file " + filename)
		if len(confFile) > 0:
			logger.info("using conf file + " + confFile)
		txt = file.read()
		file.close()
		self.labelfile = ttk.Label(text=filename.split("/")[-1], style="Cont.TLabel")
		self.labelfile.grid(row=1, column=1, pady=10)
		self.labelcont = scrolledtext.ScrolledText(wrap = tk.WORD, height = 4, font = ("Arial", 15))
		if darkMode:
			self.labelcont.configure(bg="black",fg="white")
		else:
			self.labelcont.configure(bg="white", fg="black")
		self.labelcont.grid(row=2, column=0,columnspan=7, padx=10, pady=10)
		self.labelcont.insert(tk.INSERT, txt)
		my_list = [(k, v) for k, v in interpreter.registers.items()]
		tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
		self.regis =Table(self.sf1.viewPort, tabl, updateRegisters)
		interpreter.flags={"n":0, "c":0, "z":0, "v":0}
		interpreter.pc = (None, 0)
		interpreter.ret_instr = (None,0)
		interpreter.mem = dict()
		self.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
		self.memor.e1 = ttk.Entry(app.sf.viewPort, style="TEntry")
		self.memor.e2 = ttk.Entry(app.sf.viewPort, style="TEntry")
		self.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
		self.memor.e1.grid(row=len(interpreter.mem), column=0)
		self.memor.e2.grid(row=len(interpreter.mem), column=1)
		txt = "Place in code: branch " + str(interpreter.pc[0]) + ", instruction #: " + str((interpreter.pc[1]))
		self.label5 = ttk.Label(text=txt, style="My.TLabel")
		self.label5.grid(row=9, column = 0,padx=1,pady=1, columnspan = 6)
		try:
			parsed = interpreter.parse(filename)
		except Exception as e:
			errors+= "Error parsing the filename " +filename + ".\n"+ str(e) + "\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)
		self.labelcont.configure(state="disabled")
	def restart(self):
		global logger
		logger.info("Restarting")
		global parsed
		global errors
		global filename
		global progFile
		try:
			self.label5.destroy()
		except Exception as e:
			pass
		my_list = [("x"+str(i), 0) for i in range(32) ]
		tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
		self.regis =Table(self.sf1.viewPort, tabl, updateRegisters)
		for widget in app.sf.viewPort.winfo_children():
			widget.destroy()
		interpreter.registers = dict(zip(["x"+str(i) for i in range(0,32)],[0]*32))
		interpreter.mem = dict()
		interpreter.flags={"n":0, "c":0, "z":0, "v":0}
		interpreter.pc = (None, 0)
		interpreter.ret_instr = (None,0)
		self.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 6)
		self.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
		self.memor.e1 = ttk.Entry(app.sf.viewPort, style="TEntry")
		self.memor.e2 = ttk.Entry(app.sf.viewPort, style="TEntry")
		self.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
		self.memor.e1.grid(row=len(interpreter.mem), column=0)
		self.memor.e2.grid(row=len(interpreter.mem), column=1)
		txt = "Place in code: branch " + str(interpreter.pc[0]) + ", instruction #: " + str((interpreter.pc[1]))
		self.label5 = ttk.Label(text=txt, style="My.TLabel")
		self.label5.grid(row=9, column = 0,padx=1,pady=1, columnspan = 6)

		try:
			parsed = interpreter.parse(progFile)
		except Exception as e:
			errors+= "Error parsing the filename " +progFile + ".\n"+ str(e) + "\n"
			logger.info("Error parsing the filename " +progFile + " " + str(e))

			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)

	#dummy code for updating memory
	def update(self):
		global parsed
		global errors
		global logger
		try:
			self.label5.destroy()
		except Exception:
			pass
		try:
			self.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
		except IndexError:
			pass
		try:
			interpreter.interpretOne(parsed[interpreter.pc[0]][interpreter.pc[1]], interpreter.registers, interpreter.flags)
			my_list = list(interpreter.registers.items())
			tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
			self.regis =Table(self.sf1.viewPort, tabl, updateRegisters)
			for widget in app.sf.viewPort.winfo_children():
				widget.destroy()
			self.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 6)
			for i in interpreter.mem.keys():
				print(i)
				if int(i)%4!=0:
					raise ValueError
			self.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
			self.memor.e1 = ttk.Entry(app.sf.viewPort, style="TEntry")
			self.memor.e2 = ttk.Entry(app.sf.viewPort, style="TEntry")
			self.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
			self.memor.e1.grid(row=len(interpreter.mem), column=0)
			self.memor.e2.grid(row=len(interpreter.mem), column=1)
			txt = "Place in code: branch " + str(interpreter.pc[0]) + ", instruction #: " + str((interpreter.pc[1]))
			self.label5 = ttk.Label(text=txt, style="My.TLabel")
			self.label5.grid(row=9, column = 0,padx=1,pady=1, columnspan = 6)
			logger.info("PC " + str(interpreter.pc))
			logger.info("Regs " + str(interpreter.registers))
			logger.info("Flags "+ str(interpreter.flags))
			logger.info("Mem " + str(interpreter.mem))
		except ValueError:
			errors+= "Invalid memory access! Meant to be allocating multiples of 4 bytes in memory.\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)
		except IndexError:
			errors+= "Stepped through end of code\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)
		except NameError:
			errors+= "Open a valid LEGV8 file before stepping through!\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)
		except Exception as e:
			errors+= str(e)+"\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
			self.sf2.canvas.update_idletasks()
			self.sf2.canvas.yview_moveto(1.0)
def updateRegisters(event):
	global app
	global logger
	text = event.widget.get()
	global errors

	logger.info("Registers " + str([i.get() for i in app.regis.entries]))
	try:
		interpreter.registers = dict(zip(["x"+str(i) for i in range(0,32)],[ast.literal_eval(i.get()) for i in app.regis.entries]))
		
	except IndexError:
		pass
	except Exception as e:
		errors += 'Invalid value for register! \n'
		logger.info("Error " + str(e))
		app.labelError = ttk.Label(app.sf2.viewPort, text = errors)
		app.labelError.grid(row =0,column=0)
		app.sf2.canvas.update_idletasks()
		app.sf2.canvas.yview_moveto(1.0)
	logger.info("Regs "+str(interpreter.registers))
def updateMemory(ev):
	global app
	global errors
	global logger
	if app.memor.e1.get() != "" and app.memor.e2.get() !="":
		try:
			interpreter.mem[int(app.memor.e1.get())] = ast.literal_eval(app.memor.e2.get())
			for i in interpreter.mem.keys():
				if int(i)%4!=0 or i < 0:
					raise ValueError
			for widget in app.sf.viewPort.winfo_children():
				widget.destroy()
			app.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 6)
			app.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
			app.memor.e1 = ttk.Entry(app.sf.viewPort, style="TEntry")
			app.memor.e2 = ttk.Entry(app.sf.viewPort, style="TEntry")
			app.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
			app.memor.e1.grid(row=len(interpreter.mem), column=0)
			app.memor.e2.grid(row=len(interpreter.mem), column=1)
			logger.info("Mem " + str(interpreter.mem))
		except ValueError:
			for widget in app.sf.viewPort.winfo_children():
				widget.destroy()
			app.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 6)
			app.memor = Table(app.sf.viewPort, [[i] for i in interpreter.mem.items()], updateMemory)
			app.memor.e1 = ttk.Entry(app.sf.viewPort, style="TEntry")
			app.memor.e2 = ttk.Entry(app.sf.viewPort, style="TEntry")
			app.memor.e2.bind('<Key-Return>', lambda ev: updateMemory(ev))
			app.memor.e1.grid(row=len(interpreter.mem), column=0)
			app.memor.e2.grid(row=len(interpreter.mem), column=1)
			errors += 'Invalid value for memory! \n'
			logger.info("Error " + str(app.memor.e1) + " " + str(app.memor.e2))
			app.labelError = ttk.Label(app.sf2.viewPort, text = errors)
			app.labelError.grid(row =0,column=0)
			app.sf2.canvas.update_idletasks()
			app.sf2.canvas.yview_moveto(1.0)

	elif app.memor.e1.get() == "" and app.memor.e2.get() == "":
		try:
			mem = list(zip([i.cget("text") for i in app.memor.labels], [ast.literal_eval(i.get()) for i in app.memor.entries]))
			for m in mem:
				interpreter.mem[m[0]] = m[1]
		except Exception as e:
			logger.info("Error " + str(app.memor.e1) + " " + str(app.memor.e2))
			errors += 'Invalid value for memory! \n'
			app.labelError = ttk.Label(app.sf2.viewPort, text = errors)
			app.labelError.grid(row =0,column=0)
			app.sf2.canvas.update_idletasks()
			app.sf2.canvas.yview_moveto(1.0)
	else:
		errors += 'Enter a memory value! \n'
		app.labelError = ttk.Label(app.sf2.viewPort, text = errors)
		app.labelError.grid(row =0,column=0)
		app.sf2.canvas.update_idletasks()
		app.sf2.canvas.yview_moveto(1.0)
class Table:
	def __init__(self,root, lst, ud):
		# code for creating table
		total_rows = len(lst)
		try:
			total_columns = len(lst[0])
		except IndexError:
			total_columns = 0
		self.labels = []
		self.entries = []
		for i in range(total_rows):
			for j in range(total_columns):
				self.lab = ttk.Label(root, text = lst[i][j][0], style="Cont.TLabel")
				self.lab.grid(row=i, column = 2*j)
				self.labels.append(self.lab)
				self.e = ttk.Entry(root, width=20, style="TEntry")
				self.e.insert(0, lst[i][j][1]) 
				self.e.bind('<Key-Return>', lambda ev: ud(ev))
				self.entries.append(self.e)
				self.e.grid(row=i, column=2*j+1)

app = AssemblySimApp()
app.mainloop()
