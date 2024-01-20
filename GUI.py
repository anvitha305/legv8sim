import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scrollframe import *
import interpreter
import ast
global filename
global darkMode
global stringvars
global entries
global parsed
global tabl
global errors
global app
class AssemblySimApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		global darkMode
		global tabl
		global errors
		errors = ""
		tk.Tk.__init__(self, *args, **kwargs)
		self.title = "legv8 assembly simulator"
		self.geometry("1000x700+200+200")
		self.style = ttk.Style(self.master)
		self.style.configure("My.TLabel", font=('Arial', 20))
		self.style.configure("Cont.TLabel", font=('Arial', 15))
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
		self.label2 = ttk.Label(text = "File to be simulated:", style="Cont.TLabel")
		self.label2.grid(row=1, column=0, padx=10,pady=10, columnspan = 5, sticky = tk.W+tk.E)
		self.label3 = ttk.Label(text="Registers View", style="My.TLabel")
		self.label3.grid(row=3, column=0,padx=10,pady=10, columnspan = 5, sticky = tk.W+tk.E)
		self.frame = tk.Frame()
		self.frame.grid(row=4, column=0, columnspan = 5)
		self.sf1 = ScrollFrame(self.frame)
		my_list = [("x"+str(i), 0) for i in range(32) ]
		tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
		self.regis =Table(self.sf1.viewPort, tabl)
		self.sf1.grid(row=4, column=0,padx=1,pady=1, columnspan = 5)
		self.label3 = ttk.Label(text="Memory View", style="My.TLabel")
		self.label3.grid(row=5, column=0,padx=10,pady=10, columnspan = 5, sticky = tk.W+tk.E)
		self.frame2 = tk.Frame()
		self.sf = ScrollFrame(self.frame2)
		self.frame2.grid(row=6, column=0,padx=0,pady=0, columnspan = 5)
		self.sf.grid(row=6, column=0,padx=1,pady=1, columnspan = 5)
		self.label4 = ttk.Label(text="Error View", style="My.TLabel")
		self.label4.grid(row=7, column=0,padx=10,pady=10, columnspan = 5, sticky = tk.W+tk.E)
		self.frame3 = tk.Frame()
		self.sf2 = ScrollFrame(self.frame3)
		self.frame3.grid(row=8, column=0,padx=0,pady=0, columnspan = 5)
		self.sf2.grid(row=8, column=0,padx=1,pady=1, columnspan = 5)
		darkMode = False
	def darkMode(self):
		global darkMode	
		self.configure(bg='black')
		self.style.configure("TLabel", background="black",foreground="white")
		self.style.configure("TEntry", background="black",foreground="white")
		self.style.configure("TFrame", background="black",foreground="white")
		self.sf.viewPort.configure(bg='black')
		self.sf1.viewPort.configure(bg='black')
		self.sf2.viewPort.configure(bg='black')
		try:
			self.labelcont.configure(bg="black",fg="white")
		except Exception as e:
			pass
		darkMode = True
	def lightMode(self):
		global darkMode
		self.configure(bg='white')
		self.style.configure("TLabel", background="white", foreground="black")
		self.style.configure("TEntry", background="white",foreground="black")
		self.style.configure("TFrame", background="white",foreground="black")
		try:
			self.labelcont.configure(bg="white",fg="black")
		except Exception as e:
			pass
		darkMode = False
	def browseFiles(self):
		global darkMode
		global parsed
		global errors
		filename = tk.filedialog.askopenfilename(initialdir = "-",title = "Select a legv8 (.s, .legv8) file to run",filetypes = (("Assembly","*.s"), ("LEGV8","*.legv8"),("All Files","*.*")))
		try:
			self.labelfile.destroy()
			self.labelcont.destroy()
		except Exception as e:
			pass
		file = open(filename)
		txt = file.read()
		file.close()
		self.labelfile = ttk.Label(text=filename, style="Cont.TLabel")
		self.labelfile.grid(row=1, column=1, columnspan=5, padx=10, pady=10)
		self.labelcont = scrolledtext.ScrolledText(wrap = tk.WORD, height = 4, font = ("Arial", 15))
		if darkMode:
			self.labelcont.configure(bg="black",fg="white")
		else:
			self.labelcont.configure(bg="white", fg="black")
		self.labelcont.grid(row=2, column=0,columnspan=6, padx=10, pady=10)
		self.labelcont.insert(tk.INSERT, txt)
		my_list = [("x"+str(i), 0) for i in range(32) ]
		tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
		self.regis =Table(self.sf1.viewPort, tabl)
		interpreter.registers = dict(zip(["x"+str(i) for i in range(0,32)],[0]*32))
		interpreter.flags={"n":0, "c":0, "z":0, "v":0}
		interpreter.mem = dict()
		interpreter.pc = (None, 0)
		interpreter.ret_instr = (None,0)
		try:
			parsed = interpreter.parse(filename)
		except Exception as e:
			errors+= "Error parsing the filename " +filename + ".\n"+ str(e) + "\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
		self.labelcont.configure(state="disabled")

	#dummy code for updating memory
	def update(self):
		global parsed
		global errors
		try:
			interpreter.interpretOne(parsed[interpreter.pc[0]][interpreter.pc[1]], interpreter.registers, interpreter.flags)
			my_list = list(interpreter.registers.items())
			tabl = [my_list[i * 4:(i + 1) * 4] for i in range((len(my_list) + 4 - 1) // 4 )] 
			self.regis =Table(self.sf1.viewPort, tabl)
		except IndexError:
			errors+= "Stepped through end of code\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
		except NameError:
			errors+= "Open a valid LEGV8 file before stepping through!\n"
			self.labelError = ttk.Label(self.sf2.viewPort, text = errors)
			self.labelError.grid(row =0,column=0)
def updateRegisters(event):
	global app
	text = event.widget.get()
	global errors
	try:
		interpreter.registers = dict(zip(["x"+str(i) for i in range(0,32)],[ast.literal_eval(i.get()) for i in entries]))
	except Exception as e:
		errors += 'Invalid value for register! \n'
		app.labelError = ttk.Label(app.sf2.viewPort, text = errors)
		app.labelError.grid(row =0,column=0)
class Table:
	def __init__(self,root, lst):
		global entries
		# code for creating table
		total_rows = len(lst)
		total_columns = len(lst[0])
		entries = []
		for i in range(total_rows):
			for j in range(total_columns):
				self.lab = tk.Label(root, text = lst[i][j][0])
				self.lab.grid(row=i, column = 2*j)
				self.e = tk.Entry(root, width=20)
				self.e.bind('<Key-Return>', lambda ev: updateRegisters(ev))
				entries.append(self.e)
				self.e.grid(row=i, column=2*j+1)
				self.e.insert(tk.END, lst[i][j][1])
app = AssemblySimApp()

app.mainloop()
