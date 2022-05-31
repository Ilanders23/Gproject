from tkinter import *
from tkinter import ttk
import time
from time import strftime

class StopWatch(Frame):                                                           
    def __init__(self, parent=None):        
        Frame.__init__(self, parent)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.laps = []
        self.timestr = StringVar()
        self.makeWidgets()
        self.prevLapHolder = 0
        self.lapcounter = 1

    def makeWidgets(self):                         
        self.e = Entry(self)
        timerframe = LabelFrame(self)
        timerframe.pack(fill="both", pady=(0,0))
        timer = Label(timerframe, textvariable=self.timestr,font=('Times New Roman', 40, 'bold'))
        self._setTime(self._elapsedtime)
        timer.pack(anchor = N,pady=(0,0),side=TOP)
        tree = ttk.Treeview(self)
        tree.pack(pady=(0,0),fill="both",expand=YES)
        tree_scroll = Scrollbar(tree)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.treeall = ttk.Treeview(tree,yscrollcommand=tree_scroll.set, height=6)
        self.treeall.pack() 
        self.treeall['columns'] = ("#", "Lap Time", "Split Time")
        self.treeall.column("#0", width=0, stretch=NO)
        self.treeall.column("#", anchor=CENTER, width=60)
        self.treeall.column("Lap Time", anchor=CENTER, width=100)
        self.treeall.column("Split Time", anchor=CENTER, width=100)
        self.treeall.heading("0", text="", anchor=W)
        self.treeall.heading("#", text="#", anchor=CENTER)
        self.treeall.heading("Lap Time", text="Lap Time", anchor=CENTER)
        self.treeall.heading("Split Time", text="Split Time", anchor=CENTER)
        self.treeall.pack()
        
        
    def _update(self): 
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)
    
    def Start(self):                                          
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1 

    def Stop(self):                                    
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
            
         
    def Reset(self):
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.prevLapHolder = 0
        self.lapcounter = 1
        self.laps = []   
        self._setTime(self._elapsedtime)
        self.after_cancel(self._timer)            
        self._elapsedtime = 0.0
        self.treeall.delete(*self.treeall.get_children())
        self._running = 0
    
    def Lap(self):
       tempo = self._elapsedtime - self.prevLapHolder
       if self._running:
           self.laps.append(self._setLapTime(tempo))
           self.treeall.insert(parent='',index=0,text='', values=(self.lapcounter,self._setLapTime(tempo),self._setLapTime(self._elapsedtime)))
           self.lapcounter +=1
   
def timeb():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, timeb) 
    


root = Tk()
root.title('Stopwatch(Exam)')
root.geometry("510x249")
root.resizable(False, False)
root.wm_attributes("-topmost", 1)
root.config (bg ='#e6e2d8' )
sw = StopWatch(root)
sw.config(bg='#e6e2d8')
sw.pack(side=LEFT,padx=(15,0),pady=(0,0))
lbl = Label(root)
lbl.pack(side=TOP,pady=(30,0))
lbl.config(bg ='#e6e2d8',font=('Tahoma', 20))
extraframe = Frame(root)
extraframe.config(bg ='#e6e2d8')
extraframe.pack(side=RIGHT,fill='both', expand=1,pady=(20,15),padx=(15,15))
for r in range(2):
    extraframe.rowconfigure(r, weight=1)
for r in range(2):
    extraframe.columnconfigure(r, weight=1)
        
    
Button(extraframe, text='Lap', height=1, width=5, font=('Tahoma', 20), bg='#66e3a9',
fg='white', activebackground='#6f9e8a', activeforeground='white', command=sw.Lap).grid(column=0,row=0)

Button(extraframe, text='Start', height=1, width=5, font=('Tahoma', 20), bg='#66e3a9',
fg='white', activebackground='#6f9e8a', activeforeground='white', command=sw.Start).grid(column=1,row=0)

Button(extraframe, text='Stop', height=1, width=5, font=('Tahoma', 20), bg='#66e3a9',
fg='white', activebackground='#6f9e8a', activeforeground='white',command=sw.Stop).grid(column=0,row=1)

Button(extraframe, text='Reset', height=1, width=5, font=('Tahoma', 20), bg='#66e3a9',
fg='white', activebackground='#6f9e8a', activeforeground='white',command=sw.Reset).grid(column=1,row=1)
timeb()
root.mainloop()
