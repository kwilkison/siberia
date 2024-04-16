#  This is the python implememtation of Moscow, the GUI for SIBERIA.
#
#  NOTES:
#	1.	All lists and tuples start with a empty entry just to reduce potential confusion
#		between the FORTRAN array convention (starting at 1) and the C/Python convention
#		(starting from 0). Accordingly we have adopted the FORTRAN convention.




# ----------------------------------
# ----------------------------------
#		 GLOBAL IMPORTS
# ----------------------------------
# ----------------------------------

from Tkinter import *
from tkFileDialog import *
from sys import *
from math import *
from array import *
import os,Pmw


# ----------------------------------
# ----------------------------------
#		 GLOBAL DECLARATIONS
# ----------------------------------
# ----------------------------------

Version="4.00"

NumFileParameters=10
NumRealParameters=50
NumIntegerParameters=20

SiberiaParameterText =(
	"The Data Set Title",
#	1
	"Duration of simulation (years)",
	"Period between output of diagnostic statistics (years)",
	"Easting Dimension of the grid (no of nodes)",
	"Northing Dimension of the grid (no of nodes)",
#	5
	"Mode for initial elevations in blank runs",
	"Duration of the tectonic uplift (years)",
	"Mode for Sediment Transport Solver",
	"Mode for Drainage Directions Model",
	"Mode for Tectonic Uplift Model",
#	10
	"Mode for random perturbation solver",
	"Mode for Sediment Transport Model",
	"Mode for Runoff Model",
	"Mode for Channel Model",
	"Mode for Dependent Model",
#	15
	"Mode of Monte-Carlo risk assessment solver",
	"Averaging region for drainage directions solver",
	"Mode for soil pedogensis model",
	"",
	"",
#	20
	"",
	"Diffusivity of diffusive transport",
	"Nonlinearity of diffusive transport",
	"Diffusive transport threshold (0.0 = disabled)",
	"Fluvial transport threshold (0.0 = disabled)",
#	25
	"Maximum value for FACTOR in fluvial sediment solver",
	"Mean of perturbations in random model",
	"CIF threshold",
	"The CIF for fixed Z points in fluvial sediment solver",
	"CV of perturbations in random model",
#	30
	"SD of short-term variations in runoff rate",
	"SD for long-term variations in runoff rate",
	"Amplitude of the cyclic uplift (m)",
	"Period of the cyclic uplift (years)",
	"Phase of the cyclic uplift (t=0, radians)",
#	35
	"SD of randomisation in the initial elevations for blank runs",
	"Discharge factor between fluvial transport and CIF",
	"Power on the area in discharge relationship",
	"Coefficient on the area in the discharge relationship",
	"Coefficient on the fluvial transport relationship",
#	40
	"Exponent on discharge in the fluvial transport relationship",
	"Exponent on slope in the fluvial transport relationship",
	"Bulk density of soil",
	"Time step (years)",
	"Coefficient on the Channel Initiation Function (CIF) relationship",
#	45
	"Exponent on slope in the CIF relationship",
	"Initial elevation for runs with no DEM input, total uplift for other runs",
	"Exponent on discharge in the CIF relationship",
	"YHOLD threshold in the CIF switching relationship",
	"Duration of total uplift for uplift solver",
#	50
	"Vegetation cover factor",
	"Maximum stable slope (0.0 = disabled)",
	"Rate of channel formation",
	"The ratio of overland:channel fluvial transport rates",
	"Grid resolution (m)",
#	55
	"Easting of the bottom left hand corner of the grid (m)",
	"Northing of the bottom left hand corner of the grid (m)",
	"Coefficent in the channel geometry model (0.0 = disabled)",
	"Exponent in the channel geometry model",
	"Coefficent on the supplementary fluvial transport relationship (0.0 = disabled)",
#	60
	"Exponent on discharge for the supplementary fluvial transport relationship",
	"Coefficent for the soil model",
	"Exponent 1 in the soil model",
	"Exponent 2 in the soil model",
	"Saturation excess runoff threshold",
#	65
	"Soil moisture weighting",
	"",
	"",
	"",
	"",
#	70
	""
	)

SiberiaFileText = (
	"",
#	1
	"Input Model File: Sediment Transport",
	"Input Model File: Runoff",
	"Input Model File: Tectonic Uplift",
	"Input Model File: Drainage Directions",
#	5
	"Input Model File: Monte-Carlo",
	"Input Model File: Channel",
	"Input Model File: Layering",
	"",
	"Input Model File: Control",
#	10
	"Input Model File: Dependent Model"
	)

SiberiaParameterName = (
	"DataSetName",
#	1
	"RunTime",
	"StatsTime",
	"Domain_X",
	"Domain_Y",
#	5
	"ModeIC",
	"TimeUplift",
	"ModeSolver",
	"ModeDir",
	"ModeUplift",
#	10
	"ModeRandom",
	"ModeErode",
	"ModeRunoff",
	"ModeChanel",
	"ModeDP",
#	15
	"ModeMCarlo",
	"DirReg",
	"ModeSoil",
	"------",
	"------",
#	20
	"------",
	"dZ	   ",
	"dZn   ",
	"dZTHold",
	"QsTHold",
#	25
	"FactMax",
	"FRanMin",
	"1/at	",
	"YFix	",
	"FRanCV",
#	30
	"b3SDs",
	"b3SDl",
	"UpAmp",
	"UpPeriod",
	"UpPhase",
#	35
	"FRanZ",
	"------",
	"m3	   ",
	"b3	   ",
	"b1	   ",
#	40
	"m1	   ",
	"n1	   ",
	"BulkDen",
	"TimeStep",
	"b5	   ",
#	45
	"n5	   ",
	"SInit",
	"m5	   ",
	"YHold",
	 "Notch",
#	50
	"Cover",
	"s0max",
	"DTime",
	"OTime",
	"GridXY",
#	55
	"East  ",
	"North ",
	"b6	   ",
	"m6	   ",
	"b1_2",
#	60
	"m1_2",
	"SoilRate",
	"SoilExp1",
	"SoilExp2",
	"SMTHold",
#	65
	"SoilSMWgt",
	"------",
	"------",
	"------",
	"------",
#	70
	"------"
	)

SiberiaFileName = (
	"",
#	1
	"Erosion",
	"Runoff",
	"Uplift",
	"Directions",
#	5
	"MonteCarlo",
	"Channel",
	"Layers",
	"------",
	"Control",
#	10
	"Others"
	)

DefaultSiberiaParameterValue = [
	"Default",
#	1
	"1000", "1", "40", "40",
#	5
	"0", "100", "4", "0", "0",
#	10
	"0", "0", "0", "0", "0",
#	15
	"0", "1", "0", "0", "0",
#	20
	"0", "0.0", "1.0", "0.0", "0.0",
#	25
	"1.0", "1.0", "0.0004", "1.0", "0.0",
#	30
	"0.0", "0.0", "0.0", "0.0", "0.0",
#	35
	"0.005", "1.0", "1.0", "1.0", "0.01",
#	40
	"1.8", "2.1", "1.0", "-0.025", "2.5",
#	45
	"0.3", "10.0", "0.4", "0.1", "100.0",
#	50
	"1.0", "0.0", "1.0", "1.0", "1.0",
#	55
	"0.0", "0.0", "0.0", "1.0", "0.0",
#	60
	"1.8", "0.00001", "1.0", "1.0", "1.0",
#	65
	"0.0", "0.0", "0.0", "0.0", "0.0",
#	70
	"0.0"
	]

DefaultSiberiaFileValue = [
	" ",
#	1
	" "," "," "," ",
#	5
	" "," "," "," "," ",
#	10
	" "
	]

ExtractCommandFilename="extract_command.input.txt"
ExtractLogFilename="extract.log.txt"

DiscreteCommandFilename="discrete_command.input.txt"
DiscreteLogFilename="discrete.log.txt"

InputXYZCommandFilename="inputxyz_command.input.txt"
InputXYZLogFilename="inputxyz.log.txt"

InputRAWCommandFilename="inputraw_command.input.txt"
InputRAWLogFilename="inputraw.log.txt"

SiberiaCommandFilename="siberia_command.input.txt"
SiberiaLogFilename="siberia.log.txt"

SDBtoSD3CommandFilename="sbdtosd3_command.input.txt"
SDBtoSD3LogFilename="sbdtosd3.log.txt"


DefaultImportFilename=' '
DefaultBoundBox=[-1,-1,-1,-1]
DefaultGridResolution=1.0
DefaultDBFilename='untitled'
DefaultRandomSeed=1
DefaultInputSubsample=1
DefaultInputStarttime=0
DefaultInputTimes=-1
Defaultdbdatasettitles=[]
DefaultRunData=(' ',' ',' ',DefaultInputSubsample,' ',DefaultInputStarttime,str(DefaultInputTimes))

SiberiaParameterValue=DefaultSiberiaParameterValue[:]
SiberiaFileValue=DefaultSiberiaFileValue[:]
ImportFilename=DefaultImportFilename
BoundBox=DefaultBoundBox[:]
GridResolution=DefaultGridResolution
DBFilename=DefaultDBFilename
RandomSeed=DefaultRandomSeed
Subsample=DefaultInputSubsample
RunData=DefaultRunData
dbdatasettitles=Defaultdbdatasettitles[:]

# ----------------------------------
# ----------------------------------
#	   OS SERVICE SUBROUTINES
# ----------------------------------
# ----------------------------------


def MyCPU(root):
#
#  cpu is
#	1. the platform operating system
#	2. The path to the executables that are optimised for this platform
#	3. Fallback executables that will always work on this platform in the absense of the optimal
#	4. The suffix to affix to the executable name for that platform
#
#	See MyExecute() for how this informatino is used.
#
	import platform
	import string
	machine=platform.uname()
#		Macintosh
	if string.lower(machine[0]) == 'darwin':
		if string.lower(machine[5]) == 'i386':
			cpu=('osx','/bin/osx-intel/release/','/bin/osx-ppc/release/','')
		elif string.lower(machine[5]) == 'powerpc':
			cpu=('osx','/bin/osx-ppc/release/','/bin/osx-ppc1/release/','')
		else:
			cpu=('osx','','')
			print("Unknown OSX CPU:",machine[5])
#		Linux
	elif string.lower(machine[0]) == 'linux':
		if string.lower(machine[5]) == 'x86':
			cpu=('linux','/bin/linux-intel/release/','/bin/linux-intel/release/','')
		elif string.lower(machine[5]) == 'x86_64':
			cpu=('linux','/bin/linux-intel64/release/','/bin/linux-intel/release/','')
		elif string.lower(machine[5]) == 'athlon':
			cpu=('linux','/bin/linux-intel/release/','/bin/linux-intel/release/','')
		else:
			cpu=('linux','','')
			print("Unknown Linux CPU ",machine[5])
#		Windows
	elif string.lower(machine[0]) == 'windows':
		cpu=('win','\\bin\\win\\release\\','\\bin\\win\\release\\','.exe')
#		SunOS
	elif string.lower(machine[0]) == 'sunos':
		if string.lower(machine[5]) == 'i386':
			cpu=('sunos','/bin/sunos-intel/release/','/bin/sunos-intel/release/','')
		elif string.lower(machine[5]) == 'sparc':
			cpu=('sunos','/bin/sunos-sparc/release/','/bin/sunos-sparc/release/','')
		else:
			cpu=('sunos','','')
			print("Unknown SunOS CPU ",machine[5])
	else:
		cpu=('','','')
		print("Unknown Operating System ",machine[0])
	return (cpu)

def SetTKPlatform(root):
	global cpu,BorderWidth
#	Global options
#		 root.option_add('*Entry*border','2')
	BorderWidth=2
#	Macintosh specific options
	if cpu[0] == 'osx':
		root.option_add('*background','whitesmoke')
		root.option_add('*Entry*background','white')
		root.option_add('*Text*background','white')
		root.option_add('*Pmw.ScrolledText*background','white')
		root.option_add('*Entry*relief','sunken')
		root.option_add('*Text*relief','sunken')
		root.option_add('*Font','LucidaGrande 13')
#	Windows specific options
	elif cpu[0] == 'win':
		root.option_add('*Font','Helvetica 9')
#	LINUX specific options
	elif cpu[0] == 'linux':
		root.option_add('*Font','Helvetica 12')
	return ()

def MyExecute(image,commandfile,logfile):
	
#	This routine is to execute an external binary
#	It first trys to find the software optimal for this architecture
#	then if not found falls back to one guaranteed to work on this architecture

	import os,Pmw
	global cpu
	global root
	workdir=os.getcwd()
#	optimal executable
	fullimage=workdir+cpu[1]+image+cpu[3]
#	fallback executable
	if not os.path.exists(fullimage):
		fullimage=workdir+cpu[2]+image+cpu[3]
		if not os.path.exists(fullimage):
			junk=Pmw.MessageDialog(root,title='Error',buttons=('OK',),
								   message_text="Warning the required executable '"+image+"' doesn't exist.\nThis is an installation problem.")
			return (1)
	commandline=fullimage+' < '+commandfile+' > '+logfile+' &'
#	commandline=fullimage+' < '+commandfile+' > '+logfile
	temp=root.cget('cursor')
	root.configure(cursor='watch')
	print(commandline)
	exitstatus=os.system(commandline)
#	exitstatus=os.spawnl(os.P_NOWAIT,'sh',('sh','-c',commandline))
	root.configure(cursor=temp)
	print('done',exitstatus)
	return (0)

# ----------------------------------
# ----------------------------------
#		END OF OS SERVICE SUBROUTINES
# ----------------------------------
# ----------------------------------


class BoundBoxDialog:
	def __init__(self,parent):
		global DefaultBoundBox,BorderWidth
		top=self.top=Toplevel(parent)
		self.top.focus_set()
		top.title('Bounding Box Input')
		Label(self.top, text='Input the Bounding Box for gridding\n').pack()
#  north
		self.top.line1=Frame(top)
		l1=Label(self.top.line1, text="North").pack(side=TOP)
		self.entryN=Entry(self.top.line1,border=BorderWidth)
		self.entryN.pack(side=TOP)
		top.line1.pack(padx=5)
		self.entryN.insert(0,str(DefaultBoundBox[0]))
#  east west
		self.top.line2=Frame(top)
		self.top.line2.left=Frame(self.top.line2)
		self.top.line2.right=Frame(self.top.line2)
		l3=Label(self.top.line2.left, text="West").pack(side=TOP)
		self.entryW=Entry(self.top.line2.left,border=BorderWidth)
		self.entryW.insert(0,str(DefaultBoundBox[1]))
		self.entryW.pack(side=TOP)
		l4=Label(self.top.line2.right, text="East").pack(side=TOP)
		self.entryE=Entry(self.top.line2.right,border=BorderWidth)
		self.entryE.insert(0,str(DefaultBoundBox[2]))
		self.entryE.pack(side=TOP)
		top.line2.left.pack(side=LEFT)
		top.line2.right.pack(side=LEFT)
		top.line2.pack(padx=5)
#  south
		self.top.line3=Frame(top)
		l4=Label(self.top.line3, text="South").pack(side=TOP)
		self.entryS=Entry(self.top.line3,border=BorderWidth)
		self.entryS.insert(0,str(DefaultBoundBox[3]))
		self.entryS.pack(side=TOP)
		top.line3.pack(padx=5)
# cancel/OK
		self.top.line4=Frame(top)
		c = Button(self.top.line4, text="Cancel", command=self.cancel)
		b = Button(self.top.line4, text="OK", command=self.ok)
		top.bind('<Return>',self.ok)
		top.bind('<Escape>',self.cancel)
		b.pack(pady=5,side=RIGHT,anchor=E)
		c.pack(pady=5,side=RIGHT,anchor=E)
		self.top.line4.pack(side=TOP,anchor=E,padx=10)
		
	def ok(self,event=None):
		global DefaultBoundBox
		north=self.entryN.get()
		south=self.entryS.get()
		east=self.entryE.get()
		west=self.entryW.get()
		self.box=(north,west,east,south)
		DefaultBoundBox=self.box
		self.top.destroy()
		return ()
	
	def cancel(self,event=None):
		self.top.destroy()
		self.box=()
		return ()

	
class SingleRealEntry:
	def __init__(self,parent,default,title,prompt):
		top=self.top=Toplevel(parent)
		self.top.focus_set()
		top.title('Data Entry')
		Label(self.top, text=title+'\n').pack()
#  entry
		self.top.line1=Frame(top)
		l1=Label(self.top.line1, text=prompt).pack(side=LEFT)
		self.entry=Entry(self.top.line1,border=BorderWidth)
		self.entry.pack(side=LEFT)
		top.line1.pack(padx=5)
		self.entry.insert(0,default)
# cancel/OK
		self.top.line4=Frame(top)
		c = Button(self.top.line4, text="Cancel", command=self.cancel)
		b = Button(self.top.line4, text="OK", command=self.ok)
		top.bind('<Return>',self.ok)
		top.bind('<Escape>',self.cancel)
		b.pack(pady=5,side=RIGHT,anchor=E)
		c.pack(pady=5,side=RIGHT,anchor=E)
		self.top.line4.pack(side=TOP,anchor=E,padx=10)
		
	def ok(self,event=None):
		self.value=self.entry.get()
		self.top.destroy()
		return ()
	
	def cancel(self,event=None):
		self.value=' '
		self.top.destroy()
		return ()
	
class MyMessageDialog:
	def __init__(self,parent,title,text):
		top=self.top=Toplevel(parent)
		self.top.focus_set()
		top.title('Information')
		Label(self.top, text=title+'\n').pack(padx=30)
		self.top.line1=Frame(top)
		l1=Label(self.top.line1, text=text).pack(side=LEFT,anchor=W)
		top.line1.pack(padx=5,anchor=W)
# cancel/OK
		self.top.line4=Frame(top)
		b = Button(self.top.line4, text="OK", command=self.ok)
		top.bind('<Return>',self.ok)
		top.bind('<Escape>',self.ok)
		b.pack(pady=5,side=RIGHT,anchor=E)
		self.top.line4.pack(side=TOP,anchor=E,padx=10)
		
	def ok(self,event=None):
		self.top.destroy()
		return ()
	

def GetBoundBox():
	global root
	BoundBoxData = BoundBoxDialog(root)
	root.wait_window(BoundBoxData.top)
	return (BoundBoxData.box)

def GetGridResolution():
	global root, DefaultGridResolution
	Resolution=SingleRealEntry(root,default=DefaultGridResolution
				,title='Input the gridding resolution',prompt='Resolution')
	root.wait_window(Resolution.top)
	return (Resolution.value)
	


# ----------------------------------
# ----------------------------------
#		 FILE MENU
# ----------------------------------
# ----------------------------------

def TINImportData():
	global root,ImportFilename,GridResolution,BoundBox
	line1='File to Import: '+str(ImportFilename)+'\n'
	line2='Gridding Resolution: '+str(GridResolution)+' (m)\n\n'
	line3='Bounding Box\n'
	line4=' (-1 => unconstrained on that side)\n'
	line5='Southwest corner : ('+str(BoundBox[1])+','+str(BoundBox[3])+')\n'
	line6='Northeast corner : ('+str(BoundBox[2])+','+str(BoundBox[0])+')\n'
	MyMessageDialog(root,title='Importing Data',text=line1+line2+line3+line4+line5+line6)
	return

def SiberiaRunData():
	global root,RunData,SiberiaCommandFilename
	line1='Gridded Input File : '+RunData[1]+'\n'
	line2='Boundary File (if .rst2 input) : '+RunData[2]+'\n'
	line3='SIBERIA command file : '+SiberiaCommandFilename+'\n'
	line4='SIBERIA log file : '+SiberiaLogFilename+'\n'
	line5='DEM Subsampling : '+str(RunData[3])+'\n'
	line6='Simulation Output : '+RunData[4]+'\n'
	MyMessageDialog(root,title='SIBERIA Run Data',text=line1+line2+line3+line4+line5+line6)
	return


def SiberiaNumericalParameters():
	global SiberiaParameterText
	text=''
	for i in range(1,NumIntegerParameters+NumRealParameters+1,2):
		text=text+'('+str(i)+') '+str(SiberiaParameterName[i])+' :\t'+str(SiberiaParameterValue[i])+ \
		'\t\t('+str(i+1)+') '+str(SiberiaParameterName[i+1])+' :\t'+str(SiberiaParameterValue[i+1])+'\n'
	MyMessageDialog(root,title='SIBERIA Parameters',text=text)
	return

def SiberiaFileParameters():
	global NumFileParameters,SiberiaFileValue
	text=''
	for i in range(1,NumFileParameters+1):
		text=text+'('+str(i)+') '+str(SiberiaFileName[i])+' : '+str(SiberiaFileValue[i])+'\n'
	MyMessageDialog(root,title='SIBERIA File Parameters',text=text)
	return

def myexit():
#  do any cleanup before exiting
	exit(0)


# ----------------------------------
# ----------------------------------
#		 IMPORT MENU
# ----------------------------------
# ----------------------------------

def Extract(filename,box):
	global ExtractCommandFilename
	index=filename.rfind('.')
	RootFilename=filename[:index]
	CommandFile=open(ExtractCommandFilename,'w')
	CommandFile.write(filename+'\n')
	CommandFile.write(RootFilename+'.spt'+'\n')
	CommandFile.write(RootFilename+'.ctr'+'\n')
	CommandFile.write(RootFilename+'.raw'+'\n')
	CommandFile.write(RootFilename+'.ctr.dxf'+'\n')
	CommandFile.write(box[0]+'\n')
	CommandFile.write(box[3]+'\n')
	CommandFile.write(box[2]+'\n')
	CommandFile.write(box[1]+'\n')
	CommandFile.close()
	MyExecute('extractdxf',ExtractCommandFilename,ExtractLogFilename)
#	 print('call extract')
	return

def Discrete(filename,box,resolution):
	global DiscreteCommandFilename
	index=filename.rfind('.')
	RootFilename=filename[:index]
	CommandFile=open(DiscreteCommandFilename,'w')
	CommandFile.write(RootFilename+'.raw'+'\n')
	CommandFile.write(RootFilename+'.grid.raw'+'\n')
	CommandFile.write(resolution+'\n')
	CommandFile.close()
	MyExecute('discrete',DiscreteCommandFilename,DiscreteLogFilename)
#	 print('call discrete')
	return

def importDXF():
	global DefaultImportFilename,DefaultBoundBox,DefaultGridResolution,ImportFilename,BoundBox,GridResolution
	DXFformats=[ ('Select a DXF file','*.dxf *.DXF *.dxf.txt *.DXF.TXT') ]
	ImportFilenameT=askopenfilename(filetypes=DXFformats,title='Input DXF file')
	if not (ImportFilenameT =='' or str(ImportFilenameT).isspace()):
		ImportFilename=ImportFilenameT
		BoundBoxT=GetBoundBox()
		if not BoundBoxT == ():
			BoundBox=BoundBoxT
			GridResolutionT=GetGridResolution()
			if not str(GridResolutionT).isspace() :
				GridResolution=GridResolutionT
				DefaultImportFilename=ImportFilename
				DefaultBoundBox=BoundBox[:]
				DefaultGridResolution=GridResolution
				Extract(ImportFilename,BoundBox)
				Discrete(ImportFilename,BoundBox,GridResolution)
	return

def importXYZ():
	global DefaultImportFilename,DefaultBoundBox,DefaultGridResolution,ImportFilename,BoundBox,GridResolution
	XYZformats=[ ('Select a XYZ file','*.xyz *.XYZ *.xyz.txt *.XYZ.TXT') ]
	ImportFilenameT=askopenfilename(filetypes=XYZformats,title='Input XYZ file')
	if not (ImportFilenameT =='' or str(ImportFilenameT).isspace()):
		ImportFilename=ImportFilenameT
		BoundBoxT=GetBoundBox()
		if not BoundBoxT == ():
			BoundBox=BoundBoxT
			GridResolutionT=GetGridResolution()
			if not str(GridResolutionT).isspace() :
				GridResolution=GridResolutionT
				DefaultImportFilename=ImportFilename
				DefaultBoundBox=BoundBox[:]
				DefaultGridResolution=GridResolution
				Extract(ImportFilename,BoundBox)
				Discrete(ImportFilename,BoundBox,GridResolution)
	return

def importRAW():
	global DefaultImportFilename,DefaultBoundBox,DefaultGridResolution,ImportFilename,BoundBox,GridResolution
	RAWformats=[ ('Select a RAW file','*.raw *.RAW *.raw.txt *.RAW.TXT') ]
	ImportFilenameT=askopenfilename(filetypes=RAWformats,title='Input RAW file')
	if not (ImportFilenameT =='' or str(ImportFilenameT).isspace()):
		ImportFilename=ImportFilenameT
		BoundBoxT=GetBoundBox()
		if not BoundBoxT == ():
			BoundBox=BoundBoxT
			GridResolutionT=GetGridResolution()
			if not str(GridResolutionT).isspace() :
				GridResolution=GridResolutionT
				DefaultImportFilename=ImportFilename
				DefaultBoundBox=BoundBox[:]
				DefaultGridResolution=GridResolution
				Discrete(ImportFilename,BoundBox,GridResolution)
	return


# ----------------------------------
# ----------------------------------
#		 SIBERIA RUN MENU
# ----------------------------------
# ----------------------------------
	
class InputRunDataDialog:
	def __init__(self,parent,filetype):
		import Pmw
		global BorderWidth,RunData
		top=self.top=Toplevel(parent)
		self.filetype=filetype
		self.data=(' ',' ',' ',' ',' ',' ')
		self.top.focus_set()
		self.top.title('Input Run Data')
		Label(self.top, text='Input Data for this SIBERIA Run\n').pack()
		self.top.data=Frame(top)
		row=0
#  rst2 file
		if self.filetype == 'rst2':
			l1=Label(self.top.data, text="Start RST2 file").grid(column=0,row=row,sticky=W)
			row=row+1
			top.entryDEM=Entry(self.top.data,border=BorderWidth,width=40)
			top.entryDEM.grid(column=0,columnspan=2,row=row)
			top.browseDEM=Button(self.top.data,text="Browse ...",command=self.NewDEMFile)
			top.browseDEM.grid(column=3,row=row)
			top.browseDEMClear=Button(self.top.data,text="Clear",command=self.ClearDEMFile)
			top.browseDEMClear.grid(column=2,row=row)
			top.entryDEM.insert(0,str(RunData[1]))
			row=row+1
#  bnd file 
			l2=Label(self.top.data, text="Start BND file (if any)").grid(column=0,row=row,sticky=W)
			row=row+1
			top.entryBND=Entry(self.top.data,border=BorderWidth,width=40)
			top.entryBND.grid(column=0,columnspan=2,row=row)
			top.browseBND=Button(self.top.data,text="Browse ...",command=self.NewBNDFile)
			top.browseBND.grid(column=3,row=row)
			top.browseBNDClear=Button(self.top.data,text="Clear",command=self.ClearBNDFile)
			top.browseBNDClear.grid(column=2,row=row)
			top.entryBND.insert(0,str(RunData[2]))
			row=row+1
		elif self.filetype == 'gridraw':
			l1=Label(self.top.data, text="Start RAW file").grid(column=0,row=row,sticky=W)
			row=row+1
			top.entryDEM=Entry(self.top.data,border=BorderWidth,width=40)
			top.entryDEM.grid(column=0,columnspan=2,row=row)
			top.browseDEM=Button(self.top.data,text="Browse ...",command=self.NewDEMFile)
			top.browseDEM.grid(column=3,row=row)
			top.browseDEMClear=Button(self.top.data,text="Clear",command=self.ClearDEMFile)
			top.browseDEMClear.grid(column=2,row=row)
			top.entryDEM.insert(0,str(RunData[1]))
#  generic output file
			row=row+1
		elif self.filetype == 'gridxyz':
			l1=Label(self.top.data, text="Start XYZ file").grid(column=0,row=row,sticky=W)
			row=row+1
			top.entryDEM=Entry(self.top.data,border=BorderWidth,width=40)
			top.entryDEM.grid(column=0,columnspan=2,row=row)
			top.browseDEM=Button(self.top.data,text="Browse ...",command=self.NewDEMFile)
			top.browseDEM.grid(column=3,row=row)
			top.browseDEMClear=Button(self.top.data,text="Clear",command=self.ClearDEMFile)
			top.browseDEMClear.grid(column=2,row=row)
			top.entryDEM.insert(0,str(RunData[1]))
			row=row+1
		l3=Label(self.top.data, text="Generic Output Filename").grid(column=0,row=row,sticky=W)
		row=row+1
		top.entryGenericFile=Entry(self.top.data,border=BorderWidth,width=40)
		top.entryGenericFile.grid(column=0,columnspan=2,row=row)
		top.browseGeneric=Button(self.top.data,text="Clone Name ...",command=self.NewGenericFile)
		top.browseGeneric.grid(column=3,row=row)
		top.browseGenericClear=Button(self.top.data,text="Clear",command=self.ClearGenericFile)
		top.browseGenericClear.grid(column=2,row=row)
		top.entryGenericFile.insert(0,str(RunData[4]))
		row=row+1
#		if self.filetype in ( 'gridxyz'):
#		 if self.filetype in ('gridraw', 'gridxyz'):
#			l4=Label(self.top.data, text="Grid thining: Spacing").grid(column=0,row=row,sticky=E)
#			top.entrySubsample=Entry(self.top.data,border=BorderWidth)
#			top.entrySubsample.grid(pady=15,column=1,row=row)
#			top.entrySubsample.insert(0,str(RunData[3]))
#			row=row+1			
#  absolute start time
		l4=Label(self.top.data, text="Absolute Start Time").grid(column=0,row=row,sticky=E)
		top.entryStartTime=Entry(self.top.data,border=BorderWidth)
		top.entryStartTime.grid(pady=5,column=1,row=row)
		top.entryStartTime.insert(0,str(RunData[5]))
		row=row+1
#  output times
		l5=Label(self.top.data, text="Times for output\n\n-Ascending in Time"+
			"\n-No Blank Lines\n-For regular output input"+
			"\none negative number \n").grid(column=0,row=row,sticky=E)
		top.entryOutputTimes=Text(self.top.data,border=BorderWidth,width=20)
		top.entryOutputTimes.grid(column=1,row=row,sticky=W)
		top.TimesClear=Button(self.top.data,text="Clear",command=self.ClearTimes)
		top.TimesClear.grid(column=2,row=row)
		top.entryOutputTimes.insert('0.0',str(RunData[6])+'\n')
		top.data.pack(padx=10)
# cancel/OK
		self.top.bottom=Frame(top)
		c = Button(self.top.bottom, text="Cancel", command=self.cancel)
		b = Button(self.top.bottom, text="OK", command=self.ok)
#		 top.bind('<Return>',self.ok)
		top.bind('<Escape>',self.cancel)
		b.pack(pady=5,side=RIGHT,anchor=E)
		c.pack(pady=5,side=RIGHT,anchor=E)
		self.top.bottom.pack(side=TOP,anchor=E,padx=10)
		
	def ok(self,event=None):
		demfile=self.top.entryDEM.get()
		generic=self.top.entryGenericFile.get()
		starttime=self.top.entryStartTime.get()
		times=self.top.entryOutputTimes.get('0.0',END).rstrip('\n')
		if self.filetype == 'rst2':
			bndfile=self.top.entryBND.get()
			subsample='1'
		elif self.filetype == 'gridraw':
			bndfile=' '
			subsample='1'
#			 subsample=self.top.entrySubsample.get()
		elif self.filetype == 'gridxyz':
			bndfile=' '
			subsample='1'
#			subsample=self.top.entrySubsample.get()
		else:
			filetype=' '
			demfile=' '
			bndfile=' '
			generic=' '
			subsample=' '
			starttime=' '
			times=' '
		self.data=(self.filetype,demfile,bndfile,subsample,generic,starttime,times)
		self.top.destroy()
		return()
	
	def cancel(self,event=None):
		self.filetype=' '
		demfile=' '
		bndfile=' '
		generic=' '
		subsample=' '
		starttime=' '
		times=' '
		self.data=(self.filetype,demfile,bndfile,subsample,generic,starttime,times)
		self.top.destroy()
		return ()
		
	def null(self,event=None):
		return

	def NewDEMFile(self,event=None):
		if self.filetype == 'rst2':
			format=[ ('Select a RST2 file','*.rst2 *.RST2 *.rst2.txt *.RST2.TXT') ]
			title='Input RST2 file'
		elif self.filetype == 'gridxyz':
			format=[ ('Select a gridded XYZ file','*.grid.xyz *.GRID.XYZ *.grid.xyz.txt *.GRID.XYZ.TXT') ]
			title='Input XYZ file'
		elif self.filetype == 'gridraw':
			format=[ ('Select a gridded RAW file','*.grid.raw *.GRID.RAW *.grid.raw.txt *.GRID.RAW.TXT') ]
			title='Input RAW file'
		else:
			return
		Filename=askopenfilename(filetypes=format,title=title)
		if not (Filename =='' or str(Filename).isspace()):
			self.top.entryDEM.delete(0,END)
			self.top.entryDEM.insert(0,Filename)
		return ()

	def ClearDEMFile(self,event=None):
		self.top.entryDEM.delete(0,END)
		return ()

	def NewBNDFile(self,event=None):
		format=[ ('Select a BND file','*.bnd *.BND *.bnd.txt *.BND.TXT') ]
		title='Input BND file'
		Filename=askopenfilename(filetypes=format,title=title)
		if not (Filename =='' or str(Filename).isspace()):
			self.top.entryBND.delete(0,END)
			self.top.entryBND.insert(0,Filename)
		return ()

	def ClearBNDFile(self,event=None):
		self.top.entryBND.delete(0,END)
		return ()

	def NewGenericFile(self,event=None):
		format=[ ('Select a file name to clone','* *') ]
		title='Input a filename to clone'
		Filename=askopenfilename(filetypes=format,title=title)
		if not (Filename =='' or str(Filename).isspace()):
			index=Filename.rfind('.')
			RootFilename=Filename[:index]
			self.top.entryGenericFile.delete(0,END)
			self.top.entryGenericFile.insert(0,RootFilename)
		return ()	 

	def ClearGenericFile(self,event=None):
		self.top.entryGenericFile.delete(0,END)
		return ()
	
	def ClearTimes(self,event=None):
		self.top.entryOutputTimes.delete('0.0',END)
		return ()
	
def ReadRST2Header(RST2filename):
	import Pmw
	global SiberiaParameterValue,SiberiaFileValue,root
	RSTFile=open(RST2filename,'r')
	header1=RSTFile.readline()
	if header1 == '':
		junk=Pmw.MessageDialog(root,title='Error',buttons=('OK',),
								   message_text="The requested RST2 file appears to be empty")
		return (1)
	start=header1.split()
	if start[0].lower() != 'siberia':
		junk=Pmw.MessageDialog(root,title='Error',buttons=('OK',),
								   message_text="The requested RST2 file does not appear to contain RST2 data")
		return(1)
	intline=''
	realline=''
	fileline=''
	for i in range(0,4):
		intline=intline+RSTFile.readline()
	intpar=intline.split()
	for i in range(0,10):
		realline=realline+RSTFile.readline()
	realpar=realline.split()
	for i in range(0,10):
		fileline=fileline+RSTFile.readline()
	filepar=fileline.split('\n')
	SiberiaParameterValue[0]='RST2 file input: '+RST2filename.strip()
	numint=len(intpar)
	numreal=len(realpar)
	numfile=len(filepar)
	if (numint < NumIntegerParameters or numreal < NumRealParameters or numfile < NumFileParameters):
		junk=Pmw.MessageDialog(root,title='Error',buttons=('OK',),
								   message_text="The parameters in the requested RST2 file appear to be incomplete")
		return(1)
	SiberiaParameterValue[1:NumIntegerParameters]=intpar[0:NumIntegerParameters-1]
	SiberiaParameterValue[NumIntegerParameters+1:NumRealParameters]=realpar[0:NumRealParameters-NumIntegerParameters-1]
	SiberiaFileValue[1:NumFileParameters]=filepar[0:NumFileParameters-1]
	RSTFile.close()
	return(0)

def ReadRAWHeader(RAWfilename):
	global SiberiaParameterValue
	RAWFile=open(RAWfilename,'r')
	header1=RAWFile.readline()
	header1=header1.replace('=',' ')
	header1=header1.replace(',',' ')
	data1=header1.split()
	header2=RAWFile.readline()
	header2=header2.replace('=',' ')
	header2=header2.replace(',',' ')
	data2=header2.split()
	er=min(float(data1[4]),float(data1[5]))
	er2=max(float(data1[4]),float(data1[5]))
	nr=min(float(data1[7]),float(data1[8]))
	kx=int(data2[1])
	ky=int(data2[2])
	grid=(er2-er)/(kx-1)
	SiberiaParameterValue[3]=kx
	SiberiaParameterValue[4]=ky
	SiberiaParameterValue[55]=er
	SiberiaParameterValue[56]=nr
	SiberiaParameterValue[54]=grid
	RAWFile.close()
	return   

def ReadXYZHeader(XYZfilename):
	import math,os
	global SiberiaParameterValue
	XYZFile=open(XYZfilename,'r')
	header1=XYZFile.readline()
	header1=header1.replace(',',' ')
	data1=header1.split()
	header2=XYZFile.readline()
	header2=header2.replace(',',' ')
	data2=header2.split()
	lastx=float(data2[0])
	lasty=float(data2[1])
	er=float(data1[0])
	er2=float(data2[0])
	nr=float(data1[1])
	nr2=float(data2[1])
	grid=math.hypot((er2-er),(nr2-nr))
	criteria=grid*0.1
#  aligned EW or NS
	if math.fabs(er2-er) > math.fabs(nr2-nr):
		byX=0
	else:
		byX=1
#	print(os.times())
	for i in range(2,10000000):
		line=XYZFile.readline()
		if line.strip() == '':
			break
		lastline=line
	lastline=lastline.replace(',',' ')
	data=lastline.split()
	lastx=float(data[0])
	lasty=float(data[1])
#	print(os.times())
	kx=int(round((float(lastx)-float(data1[0]))/float(grid))+1)
	ky=int(round((float(lasty)-float(data1[1]))/float(grid))+1)
	SiberiaParameterValue[3]=kx
	SiberiaParameterValue[4]=ky
	SiberiaParameterValue[55]=er
	SiberiaParameterValue[56]=nr
	SiberiaParameterValue[54]=grid
	XYZFile.close()
	return
	

def inputRST2():
	global RunData,DefaultRunData
	RunDataT=InputRunDataDialog(root,filetype='rst2')
	root.wait_window(RunDataT.top)
	if not (RunDataT.data[1].isspace() or RunDataT.data[1] == ''):
		RunData=RunDataT.data
		err=ReadRST2Header(RunData[1])
		if err != 0:
			RunData=DefaultRunData
			return(err)
	else:
		RunData=RunDataT.data
		junk=Pmw.MessageDialog(root,title='Warning',
					message_text='No initial RST2 file was selected\nUsing default parameters, initial conditions, and DEM domain',buttons=('OK',))
	return

def inputRAW():
	import Pmw
	global root,RunData
	RunDataT=InputRunDataDialog(root,filetype='gridraw')
	root.wait_window(RunDataT.top)
	if not (RunDataT.data[1].isspace() or RunDataT.data[1] == ''):
		RunData=RunDataT.data
		ReadRAWHeader(RunData[1])
	else:
		junk=Pmw.MessageDialog(root,title='Error',
					message_text='No DEM file was selected',buttons=('OK',))
	return

def inputXYZ():
	import Pmw
	global root,RunData
	RunDataT=InputRunDataDialog(root,filetype='gridxyz')
	root.wait_window(RunDataT.top)
	if not (RunDataT.data[1].isspace() or RunDataT.data[1] == ''):
		RunData=RunDataT.data
		ReadXYZHeader(RunData[1])
	else:
		junk=Pmw.MessageDialog(root,title='Error',
					message_text='No DEM file was selected',buttons=('OK',))
	return
	
def MyEOFError():
	print('Premature end of the raw file')
	return

def ConvertRAWtoRST2(InFilename,OutFilename,BndFilename):
	global SiberiaParameterValue,Version,SiberiaFileValue
	RAWFile=open(InFilename,'r')
	RST2File=open(OutFilename,'w')
	BNDFile=open(BndFilename,'w')
#  Read the header of the raw file
# ---------------------------------
	header1=RAWFile.readline()
	header1=header1.replace('=',' ')
	header1=header1.replace(',',' ')
	data1=header1.split()
	header2=RAWFile.readline()
	header2=header2.replace('=',' ')
	header2=header2.replace(',',' ')
	data2=header2.split()
	er=min(float(data1[4]),float(data1[5]))
	er2=max(float(data1[4]),float(data1[5]))
	nr=min(float(data1[7]),float(data1[8]))
	kx=int(data2[1])
	ky=int(data2[2])
	grid=(er2-er)/(kx-1)
	SiberiaParameterValue[3]=kx
	SiberiaParameterValue[4]=ky
	SiberiaParameterValue[55]=er
	SiberiaParameterValue[56]=nr
	SiberiaParameterValue[54]=grid
	header3=RAWFile.readline()
	header4=RAWFile.readline()
#	Create the header for the rst2 file
# --------------------------------------
	RST2File.write('SIBERIA			   8.30\n')
	num=0
	for i in range(0,3):
		for j in range(1,7):
			num=num+1
			RST2File.write(str(SiberiaParameterValue[int(num)])+' ')
		RST2File.write('\n')
	RST2File.write(str(SiberiaParameterValue[19])+' ')
	RST2File.write(str(SiberiaParameterValue[20])+'\n')
	num=20
	for i in range(0,10):
		for j in range(1,6):
			num=num+1
			RST2File.write(str(SiberiaParameterValue[int(num)])+' ')
		RST2File.write('\n')
	for i in range(1,11):
		RST2File.write(SiberiaFileValue[int(i)]+'\n')
# dummy flow outlets
	RST2File.write('1\n')
	RST2File.write('1 1\n')
#	Create the header for the bnd file
#  ------------------------------------
	BNDFile.write('Boundary File generated by Moscow V'+Version+', Input File: '+InFilename.strip()+'\n')
	BNDFile.write(str(kx)+' '+str(ky)+'\n')
	BNDdata=[]
#  do the body of the rst2 and bnd files
# ---------------------------------------
	eof=0
	for j in range(1,ky+1):
		bndline=[]
		for i in range(1,kx+1):
#	read/write the Z data 
			line=RAWFile.readline()
			if line == '':
				MyEOFError()
				eof=1
				break
			data=line.split()
			value=float(data[1])
			RST2File.write('0 0 0 '+str(value)+' 0 5 0 0\n')
#	construct the boundary file
			if value > 0:
				bndline.append('*')
			else:
				bndline.append('.')
		BNDdata.append(bndline)
		if eof == 1 : break
#	do the inside of the domain
	for j in range(1,ky-1):
		for i in range(1,kx-1):
			if BNDdata[j][i] == '*':
				if (BNDdata[j][i-1] == '.' or BNDdata[j][i+1] == '.' or 
				   		BNDdata[j-1][i-1] == '.' or BNDdata[j-1][i+1] == '.' or 
						BNDdata[j+1][i-1] == '.' or BNDdata[j+1][i+1] == '.' or 
						BNDdata[j-1][i] == '.' or BNDdata[j+1][i] == '.'): 
					BNDdata[j][i]='^'
#	do the BC
	for j in range(0,ky):
		i=0
		if BNDdata[j][i] == '*':
			BNDdata[j][i]='^'
		i=kx-1
		if BNDdata[j][i] == '*':
			BNDdata[j][i]='^'
	for i in range(1,kx-1):
		j=0
		if BNDdata[j][i] == '*':
			BNDdata[j][i]='^'
		j=ky-1
		if BNDdata[j][i] == '*':
			BNDdata[j][i]='^'
	line=''
	for j in range(0,ky):
		for i in range(0,kx):
			line=line+BNDdata[j][i]
		line=line+'\n'
	BNDFile.writelines(line)
	RAWFile.close()
	RST2File.close()
	BNDFile.close()
	return

def ConvertXYZtoRST2(InFilename,OutFilename,BndFilename):
	import array,math,os
	global SiberiaParameterValue,SiberiaFileValue,Version
	XYZFile=open(InFilename,'r')
	RST2File=open(OutFilename,'w')
	BNDFile=open(BndFilename,'w')
#	read the start of the XYZ file
# --------------------------------------
	header1=XYZFile.readline()
	header1=header1.replace(',',' ')
	data1=header1.split()
	header2=XYZFile.readline()
	header2=header2.replace(',',' ')
	data2=header2.split()
	lastx=float(data2[0])
	lasty=float(data2[1])
	lastz=float(data2[2])
	er=float(data1[0])
	er2=float(data2[0])
	nr=float(data1[1])
	nr2=float(data2[1])
	grid=math.hypot((er2-er),(nr2-nr))
	criteria=grid*0.1
	kx=SiberiaParameterValue[3]
	ky=SiberiaParameterValue[4]
#  aligned EW or NS
	if math.fabs(er2-er) > math.fabs(nr2-nr):
		byX=0
	else:
		byX=1
	print('byX=',byX)
#	Create the header for the rst2 file
# --------------------------------------
	RST2File.write('SIBERIA			   8.30\n')
	num=0
	for i in range(0,3):
		for j in range(1,7):
			num=num+1
			RST2File.write(str(SiberiaParameterValue[int(num)])+' ')
		RST2File.write('\n')
	RST2File.write(str(SiberiaParameterValue[19])+' ')
	RST2File.write(str(SiberiaParameterValue[20])+'\n')
	num=20
	for i in range(0,10):
		for j in range(1,6):
			num=num+1
			RST2File.write(str(SiberiaParameterValue[int(num)])+' ')
		RST2File.write('\n')
	for i in range(1,11):
		RST2File.write(SiberiaFileValue[int(i)]+'\n')
# dummy flow outlets
	RST2File.write('1\n')
	RST2File.write('1 1\n')
#	Create the header for the bnd file
#  ------------------------------------
	BNDFile.write('Boundary File generated by Moscow V'+Version+', Input File: '+InFilename.strip()+'\n')
	BNDFile.write(str(kx)+' '+str(ky)+'\n')
	BNDdata=[]
	Zdata=[]
	Zline=[]
#	Zline=array.array('d')
#  do the body of the rst2 and bnd files
# ---------------------------------------
	XYZFile.close()
	XYZFile=open(InFilename,'r')
	if byX == 0:
		eof=0
		for j in range(1,ky+1):
			bndline=[]
			Zline=[]
			for i in range(1,kx+1):
#	read the Z data 
				line=XYZFile.readline()
				if line.strip() == '':
					MyEOFError()
					eof=1
					break
				data=line.split()
				value=float(data[2])
				Zline.append(value)
#	construct the boundary file
				if value > 0:
					bndline.append('*')
				else:
					bndline.append('.')
			BNDdata.append(bndline)
			Zdata.append(Zline)
			if eof == 1 : break
#	output the rst2 file
		for j in range(0,ky):
			for i in range(0,kx):
				RST2File.write('0 0 0 '+str(Zdata[j][i])+' 0 5 0 0\n')
#	do the inside of the domain
		for j in range(1,ky-1):
			for i in range(1,kx-1):
				if BNDdata[j][i] == '*':
					if (BNDdata[j][i-1] == '.' or BNDdata[j][i+1] == '.' or 
							BNDdata[j-1][i-1] == '.' or BNDdata[j-1][i+1] == '.' or 
							BNDdata[j+1][i-1] == '.' or BNDdata[j+1][i+1] == '.' or 
							BNDdata[j-1][i] == '.' or BNDdata[j+1][i] == '.'): 
						BNDdata[j][i]='^'
#	do the BC
		for j in range(0,ky):
			i=0
			if BNDdata[j][i] == '*':
				BNDdata[j][i]='^'
			i=kx-1
			if BNDdata[j][i] == '*':
				BNDdata[j][i]='^'
		for i in range(1,kx-1):
			j=0
			if BNDdata[j][i] == '*':
				BNDdata[j][i]='^'
			j=ky-1
			if BNDdata[j][i] == '*':
				BNDdata[j][i]='^'
		line=''
		for j in range(0,ky):
			for i in range(0,kx):
				line=line+BNDdata[j][i]
			line=line+'\n'
		BNDFile.writelines(line)
	else:
		eof=0
		for i in range(1,kx+1):
			bndline=[]
			Zline=[]
			for j in range(1,ky+1):
#	read the Z data 
				line=XYZFile.readline()
				if line.strip() == '':
					MyEOFError()
					eof=1
					break
				data=line.split()
				value=float(data[2])
				Zline.append(value)
#	construct the boundary file
				if value > 0:
					bndline.append('*')
				else:
					bndline.append('.')
			BNDdata.append(bndline)
			Zdata.append(Zline)
			if eof == 1 : break
#	output the rst2 file
		for j in range(0,ky):
			for i in range(0,kx):
				RST2File.write('0 0 0 '+str(Zdata[i][j])+' 0 5 0 0\n')
#	do the inside of the domain
		for j in range(1,ky-1):
			for i in range(1,kx-1):
				if BNDdata[i][j] == '*':
					if (BNDdata[i][j-1] == '.' or BNDdata[i][j+1] == '.' or 
							BNDdata[i-1][j-1] == '.' or BNDdata[i-1][j+1] == '.' or 
							BNDdata[i+1][j-1] == '.' or BNDdata[i+1][j+1] == '.' or 
							BNDdata[i-1][j] == '.' or BNDdata[i+1][j] == '.'): 
						BNDdata[i][j]='^'
#	do the BC
		for j in range(0,ky):
			i=0
			if BNDdata[i][j] == '*':
				BNDdata[i][j]='^'
			i=kx-1
			if BNDdata[i][j] == '*':
				BNDdata[i][j]='^'
		for i in range(1,kx-1):
			j=0
			if BNDdata[i][j] == '*':
				BNDdata[i][j]='^'
			j=ky-1
			if BNDdata[i][j] == '*':
				BNDdata[i][j]='^'
		line=''
		for j in range(0,ky):
			for i in range(0,kx):
				line=line+BNDdata[i][j]
			line=line+'\n'
		BNDFile.writelines(line)
	XYZFile.close()
	RST2File.close()
	BNDFile.close()
	return

def prepareSIBERIA():
	global SiberiaCommandFilename,RunData
	SiberiaCommandFile=open(SiberiaCommandFilename,'w')
	if RunData[0] == 'rst2':
		SiberiaCommandFile.write(RunData[1]+'\n')
		SiberiaCommandFile.write(RunData[2]+'\n')
#
#	 .grid.raw input
# --------------------
#
	elif RunData[0] == 'gridraw':
#  check filename entered
		if RunData[1].isspace() or RunData[1] == '':
			return
		if RunData[1][-3:].lower() =='txt':
			RootFilename=RunData[1][:-13]
		else:
			RootFilename=RunData[1][:-9]
		OutFilename=RootFilename+'-start.rst2'
		BndFilename=RootFilename+'.bnd'
		ConvertRAWtoRST2(RunData[1],OutFilename,BndFilename)
		SiberiaCommandFile.write(OutFilename+'\n')
		SiberiaCommandFile.write(BndFilename+'\n')
#
#	 .grid.xyz input
# --------------------
#
	elif RunData[0] == 'gridxyz':
		if RunData[1].isspace() or RunData[1] == '':
			return
		if RunData[1][-3:].lower() =='txt':
			RootFilename=RunData[1][:-13]
		else:
			RootFilename=RunData[1][:-9]
		OutFilename=RootFilename+'-start.rst2'
		BndFilename=RootFilename+'.bnd'
		ConvertXYZtoRST2(RunData[1],OutFilename,BndFilename)
		SiberiaCommandFile.write(OutFilename+'.rst2\n')
		SiberiaCommandFile.write(BndFilename+'.bnd\n')

#  if requesting output files
	if not (RunData[4].isspace() or RunData[4] == ''):
		SiberiaCommandFile.write('-1\n')
		SiberiaCommandFile.write(RunData[6]+'\n\n')
		SiberiaCommandFile.write(RunData[4]+'\n')
		SiberiaCommandFile.write(RunData[5]+'\n')
	else:
		SiberiaCommandFile.write(' \n')
#  if not inputtting a starting rst2 file then write DEM initilisation data
	if RunData[1].isspace() or RunData[1] == '':
		SiberiaCommandFile.write(str(RandomSeed)+'\n')
		SiberiaCommandFile.write(' \n')
	for i in range(1,NumIntegerParameters+NumRealParameters+1):
#  don't output the DEM parameters if a DEM has been input
		if RunData[1].strip() != '' and not (i in (3,4,54,55,56)):
			SiberiaCommandFile.write(str(i)+'\n'+str(SiberiaParameterValue[i])+'\n')
	for i in range(1,NumFileParameters+1):
		SiberiaCommandFile.write(' -'+str(i).lstrip()+'\n'+str(SiberiaFileValue[i])+'\n')
	SiberiaCommandFile.write('0\n')
	SiberiaCommandFile.write('1\n')
#  add a few blank lines at the bottom of command file
	SiberiaCommandFile.write('\n\n\n')
	SiberiaCommandFile.close()
	return

def runSIBERIA():
	global SiberiaCommandFilename,SiberiaLogFilename
	prepareSIBERIA()
	MyExecute('siberia',SiberiaCommandFilename,SiberiaLogFilename)
	return

def runbkSIBERIA():
	prepareSIBERIA()
	print('Running SIBERIA in background not yet supported')
	return


# ----------------------------------
# ----------------------------------
#	 DATABASE AND PARAMETERS MENU
# ----------------------------------
# ----------------------------------

class ModifyParametersDialog:
	def __init__(self,parent,parameters,component,ptype,modify):
		import Pmw
		global BorderWidth,RunData
		top=self.top=Toplevel(parent)
		self.top.focus_set()
		if modify == 0:
			self.top.title('Modify '+ptype+' Parameters')
			Label(self.top, text='Modify '+ptype+' Parameters from Parameter Set: \n'+SiberiaParameterValue[0]+'\n').pack()
		else:
			self.top.title(ptype+' Parameters')
			Label(self.top, text=ptype+' Parameters from Parameter Set: \nWARNING: SIBERIA may crash if you modify these parameters\n'+SiberiaParameterValue[0]+'\n').pack()
		self.top.data=Frame(top)
		row=0
		top.parameters=parameters
		top.paraentry=[]
		top.browse=[]
		title=Label(self.top.data, text='Parameter',anchor=CENTER).grid(column=0,row=row)
		title=Label(self.top.data, text='Description',anchor=CENTER).grid(column=1,row=row)
		title=Label(self.top.data, text='Value',anchor=CENTER).grid(column=2,row=row)
		row=row+1
		for i in range(0,len(parameters)):
#  rst2 file
			paraname1=str(component)+'.'+str(i+1).lstrip()+' ('+str(parameters[i])+'):	'
			paranumt=Label(self.top.data, text=paraname1).grid(column=0,row=row,sticky=W)
			if parameters[i] > 0:
				paratextt=Label(self.top.data, text=SiberiaParameterText[parameters[i]],width=50,anchor=W,wraplength=400,justify=LEFT).grid(column=1,row=row)
				paraentryt=Entry(self.top.data,border=BorderWidth,width=15)
				paraentryt.grid(column=2,row=row,sticky=E)
				top.paraentry.append(paraentryt)
				paraentryt.insert(0,str(SiberiaParameterValue[parameters[i]]))
				top.browse.append('')
			else:
				num=-parameters[i]
				paratextt=Label(self.top.data, text=SiberiaFileText[num],justify=LEFT).grid(column=1,row=row,sticky=W)
				row=row+1
				paraentryt=Entry(self.top.data,border=BorderWidth,width=70)
				paraentryt.grid(column=1,columnspan=2,row=row,sticky=E)
				top.paraentry.append(paraentryt)
				paraentryt.insert(0,SiberiaFileValue[num])
				browset=Button(self.top.data,text="Browse ...",command=lambda pp=paraentryt: self.BrowseFile(pp=pp))
				browset.grid(column=3,row=row)
				top.browse.append(browset)
			row=row+1
		top.data.pack(padx=10)
# cancel/OK
		self.top.bottom=Frame(top)
		c = Button(self.top.bottom, text="Cancel", command=self.cancel)
		b = Button(self.top.bottom, text="OK", command=self.ok)
		top.bind('<Escape>',self.cancel)
		b.pack(pady=5,side=RIGHT,anchor=E)
		c.pack(pady=5,side=RIGHT,anchor=E)
		self.top.bottom.pack(side=TOP,anchor=E,padx=10)
		
	def ok(self,event=None):
		for i in range(0,len(self.top.parameters)):
			paranum=self.top.parameters[i]
			paravalue=self.top.paraentry[i].get()
			if paranum > 0:
				SiberiaParameterValue[paranum]=paravalue
			else:
				num=-paranum
				SiberiaFileValue[num]=paravalue
		self.top.destroy()
		return()
	
	def cancel(self,event=None):
		self.top.destroy()
		return ()
		
	def BrowseFile(self,pp,event=None):
		format=[ ('Select a model file ','*.model *.MODEL *.model.txt *.MODEL.TXT') ]
		title='Input a model file'
		Filename=askopenfilename(filetypes=format,title=title)
		if not (Filename =='' or str(Filename).isspace()):
			pp.delete(0,END)
			pp.insert(0,Filename)
		return ()	 
		pp.delete(0,END)
		return ()

def ConvertSDBtoSD3(DBFilename):
	global root
	import Pmw
	junk=Pmw.MessageDialog(root,title='Warning',
					   message_text='You have selected a V2 or earlier SIBERIA database (i.e. .sbd extension) \n'+
					   'which must be converted to V3 format (i.e. .sd3 extension) before it can be read. The V2 file\n'+
					   'will remain after the conversion\n'
					   'Do you wish to continue (database will not be read if No)?',
					   buttons=('Yes','No'),defaultbutton=1)
	result=junk.activate()
	if result == 'No' :
		return
	comfile=open(SDBtoSD3CommandFilename,'w')
	comfile.write(DBFilename+'\n')
	comfile.write(DBFilename[len(DBFilename)-4:]+'.sd3\n')
	MyExecute('sdbtosd3',SDBtoSD3CommandFilename,SDBtoSD3LogFilename)
	comfile.close()
	return

def newDB():
	global DBFilename,DefaultDBFilename
	DBformats=[('Select a ascii format database','*.sd3 *.SD3')]
	DBFilename=DefaultDBFilename
#	DBFilename=asksaveasfilename(filetypes=DBformats,title='Input SIBERIA database file',defaultextension='.sd3')
#	print(DBFilename)
	return

def openDB():
	global dbheader,dbnumdata,dbdata,dbdatasettitles,DBFilename
	DBformats=[
		('Select a ascii format database','*.sd3 *.SD3'),
		('Select a binary format database','*.sdb *.SDB')
		]
	DBFilename=askopenfilename(filetypes=DBformats,title='Input SIBERIA database file')
	if DBFilename[len(DBFilename)-4:].lower() == '.sdb':
		ConvertSDBtoSD3(DBFilename)
	DBFilename=DBFilename[:len(DBFilename)-4]+'.sd3'
	dbfile=open(DBFilename,'r')
	dbheader=dbfile.readline()
	dbnumdata=dbfile.readline()
	dbdata=dbfile.readlines()
	dbdatasettitles=[]
	for i in range(0,len(dbdata)):
		title=dbdata[i][:40].strip()
		dbdatasettitles.append(title)
	dbfile.close()
	return

def saveDB():
	global DBFilename,DefaultDBFilename
	DBformats=[('Save the database to','*.sd3 *.SD3')]
	if DBFilename==DefaultDBFilename or DBFilename.strip()=='':
		DBFilename=asksaveasfilename(filetypes=DBformats,title='SIBERIA database file name',defaultextension='.sd3',initialfile=DefaultDBFilename)
		if DBFilename.strip() == '': return
		if not DBFilename[len(DBFilename)-4:].lower() == '.sd3':
			DBFilename=DBFilename.strip()+'.sd3'
		print(DBFilename)
	return

def closeDB():
	global dbheader,dbnumdata,dbdata,dbdatasettitles,DBFilename
	dbdata=[]
	dbdatasettitles=[]
	dbheader=''
	dbnumdata=0
	DBFilename=''
	return

def SelectNewParameters():
	import Pmw
	global root,dbdatasettitles,dbdata,SiberiaParameterValue
	paradialog=Pmw.ComboBoxDialog(root,title='Select Parameter Set',
								  buttons=('OK','Cancel'), defaultbutton='OK',
								  scrolledlist_items=dbdatasettitles,listbox_width=40)
	result=paradialog.activate()
	if result == 'Cancel':
		return(' ')
	name=paradialog.get()
	if name in dbdatasettitles:
		index=dbdatasettitles.index(name)
	else:
		junk=Pmw.MessageDialog(root,title='Error',
					message_text='The parameter set name you have entered "'+name+'"is not in the database',
					buttons=('OK',))
		return(' ')
	datalist=dbdata[index][40:].split()
#  setting the parameters
	SiberiaParameterValue[0]=name
	SiberiaParameterValue[1:]=datalist
	return(name)

def CloneNewParameters():
	global root,SiberiaParameterValue
	import Pmw
	name=SelectNewParameters()
	if str(name).isspace() or name == '':
		return
	clonename=Pmw.PromptDialog(root,title='New dataset name',entryfield_labelpos=N,
							buttons=('OK','Cancel'), defaultbutton='Cancel',
						   label_text='New name for the cloned dataset')
	result=clonename.activate()
	if result == 'Cancel':
		return
	name=clonename.get()
	if str(name).isspace() or name == '':
		junk=Pmw.MessageDialog(root,title='Error',
					message_text='Invalid name for data set',
					buttons=('OK',))
		return
	SiberiaParameterValue[0]=name
	return
	
def ResetParameters():
	global SiberiaParameterValue,DefaultSiberiaParameterValue
	SiberiaParameterValue=DefaultSiberiaParameterValue[:]
	return

def editParameters1():
	global root
	parameters=(1,43,2,-9,15,-5)
	ModifyParametersDialog(root,parameters,1,'Run',0)
	return

def editParameters2():
	global root
	parameters=(3,4,54,55,56)
	ModifyParametersDialog(root,parameters,1,'DEM',1)
	return

def editParameters3():
	global root
	parameters=(12,-2,8,-4,38,37)
	ModifyParametersDialog(root,parameters,1,'Hydrology',0)
	return

def editParameters4():
	global root
	parameters=(11,-1,39,40,41,50,59,60,24)
	ModifyParametersDialog(root,parameters,1,'Erosion',0)
	return

def editParameters5():
	global root
	parameters=(21,22,23,51)
	ModifyParametersDialog(root,parameters,1,'Mass Movement',0)
	return

def editParameters6():
	global root
	parameters=(13,-6,27,44,47,45,36,52,57,58,25,53)
	ModifyParametersDialog(root,parameters,1,'Channel',0)
	return

def editParameters7():
	global root
	parameters=(9,-3,6,46,49,32,33,34)
	ModifyParametersDialog(root,parameters,1,'Tectonics',0)
	return

def editParameters8():
	global root
	parameters=(17,42,61,62,63,64,65)
	ModifyParametersDialog(root,parameters,1,'Soil Pedogenesis',1)
	return

def editParameters9():
	global root
	parameters=(14,-10,5,7,10,16,26,28,29,30,31,35,48)
	ModifyParametersDialog(root,parameters,1,'Internal',1)
	return

def SaveParameters():
	return


# ----------------------------------
# ----------------------------------
#			HELP MENU
# ----------------------------------
# ----------------------------------


def aboutEAMS():
	import Pmw
	global root,Version
	Pmw.aboutversion(Version)
	Pmw.aboutcopyright('Copyright Prof Garry Willgoose 2007\nAll rights reserved')
	Pmw.aboutcontact(
		'For information about EAMS contact:\n' +
		'Prof. Garry Willgoose\nTelluric Research\n' +
		'g.willgoose@telluricresearch.com\n\n' +
		'For more information visit\n' +
		'www.telluricresearch.com/eams'
		)
	about=Pmw.AboutDialog(root,applicationname='EAMS')
	return

def usingEAMS():
	import webbrowser,os
	cwd="file://"+os.getcwd()+"/help/moscow-homepage.html"
	webbrowser.open_new(cwd)
	return

def howtoEAMS():
	import webbrowser,os
	cwd="file://"+os.getcwd()+"/help/moscow-howto/index.html"
	webbrowser.open_new(cwd)
	return

def troubleshooting():
	import webbrowser,os
	cwd="file://"+os.getcwd()+"/help/troubleshooting/index.html"
	webbrowser.open_new(cwd)
	return

def gotoTelluricResearch():
	import webbrowser
	webbrowser.open_new("http://www.telluricresearch.com")
	return

def gotoEAMShomepage():
	import webbrowser
	webbrowser.open_new("http://www.telluricresearch.com/eams-homepage.html")
	return

def gotoSiberiahomepage():
	import webbrowser
	webbrowser.open_new("http://www.telluricresearch.com/siberia-homepage.html")
	return

# ---------------------
# ---------------------
#	testing stuff
# ---------------------
# ---------------------

def mytest():
	print ('0,10 =',range(0,10))
	print ('0,10,1 =',range(0,10,1))
	print ('10,0,-1 =',range(10,0,-1))

# ---------------------
# ---------------------
#	CONSTRUCT MENUS
# ---------------------
# ---------------------

def makeFileMenu():
	Btn = Menubutton(mBar, text='File', borderwidth=6)
	Btn.pack(side=LEFT, padx="1m")
	Btn.menu = Menu(Btn,tearoff=0)
	Btn.menu.debug = Menu(Btn,tearoff=0)
	Btn.menu.debug.add_command(label='Show Import Data',command=TINImportData)
	Btn.menu.debug.add_command(label='Show SIBERIA Run Data',command=SiberiaRunData)
	Btn.menu.debug.add_command(label='Show SIBERIA Numerical Parameters',command=SiberiaNumericalParameters)
	Btn.menu.debug.add_command(label='Show SIBERIA File Parameters',command=SiberiaFileParameters)
	Btn.menu.add_cascade(label='Debug',menu=Btn.menu.debug)	   
	Btn.menu.add('separator')
	Btn.menu.add_command(label='Test',command=mytest)
	Btn.menu.add_command(label='Quit',command=myexit)
	Btn['menu'] = Btn.menu
	return Btn

def makeImportMenu():
	global cpu
	Btn = Menubutton(mBar, text='Import TIN', borderwidth=6)
	Btn.pack(side=LEFT, padx="1m")
	Btn.menu = Menu(Btn,tearoff=0)
	Btn.menu.add_command(label='Import .DXF',command=importDXF)
	Btn.menu.add_command(label='Import .XYZ',command=importXYZ)
	Btn.menu.add_command(label='Import .RAW',command=importRAW)
	Btn['menu'] = Btn.menu
	return Btn

def makeSiberiaMenu():
	global cpu
	Btn = Menubutton(mBar, text='SIBERIA', borderwidth=6)
	Btn.pack(side=LEFT, padx="1m")
	Btn.menu = Menu(Btn,tearoff=0)
	Btn.menu.add_command(label='Input from .RST2',command=inputRST2)
	Btn.menu.add_command(label='Input from gridded .RAW',command=inputRAW)
	Btn.menu.add_command(label='Input from gridded .XYZ',command=inputXYZ)
	Btn.menu.add('separator')
	Btn.menu.add_command(label='Prepare SIBERIA only',command=prepareSIBERIA)
	Btn.menu.add_command(label='Prepare and run SIBERIA',command=runSIBERIA)
	Btn.menu.add_command(label='Prepare and background SIBERIA',command=runbkSIBERIA)
	Btn['menu'] = Btn.menu
	return Btn

def makeParametersMenu():
	global cpu
	Btn = Menubutton(mBar, text='Parameters ', borderwidth=6)
	Btn.pack(side=LEFT, padx="1m")
	Btn.menu = Menu(Btn,tearoff=0)
	Btn.menu.add_command(label='New Database',command=newDB)
	Btn.menu.add_command(label='Open Database',command=openDB)
	Btn.menu.add_command(label='Save Database',command=saveDB)
	Btn.menu.add_command(label='Close Database',command=closeDB)
	Btn.menu.add('separator')
	Btn.menu.add_command(label='Select Parameter Set',command=SelectNewParameters)
	Btn.menu.add_command(label='Clone New Parameter Set',command=CloneNewParameters)
	Btn.menu.add_command(label='Reset to Default Parameter Set',command=ResetParameters)
	Btn.menu.add_command(label='Save Modified Parameter Set',command=SaveParameters)
	Btn.menu.edit=Menu(Btn.menu,tearoff=0)
	Btn.menu.edit.add_command(label='1. Run Parameters',command=editParameters1)
	Btn.menu.edit.add_command(label='2. DEM Properties',command=editParameters2)
	Btn.menu.edit.add_command(label='3. Hydrology Parameters',command=editParameters3)
	Btn.menu.edit.add_command(label='4. Erosion Parameters',command=editParameters4)
	Btn.menu.edit.add_command(label='5. Mass Movement Parameters',command=editParameters5)
	Btn.menu.edit.add_command(label='6. Channel/Gully Parameters',command=editParameters6)
	Btn.menu.edit.add_command(label='7. Tectonics Parameters',command=editParameters7)
	Btn.menu.edit.add_command(label='8. Soil Genesis Parameters',command=editParameters8)
	Btn.menu.edit.add_command(label='9. Internal Parameters',command=editParameters9)
	Btn.menu.add_cascade(label='Edit Parameters',menu=Btn.menu.edit)
	Btn['menu'] = Btn.menu
	return Btn

def makeHelpMenu():
	global cpu
	Btn = Menubutton(mBar, text='Help', borderwidth=6)
	Btn.pack(side=LEFT, padx="1m")
	Btn.menu = Menu(Btn,tearoff=0)
	Btn.menu.add_command(label='About EAMS',command=aboutEAMS)
	Btn.menu.add_command(label='Using EAMS',command=usingEAMS)
	Btn.menu.add_command(label='How To ...',command=howtoEAMS)
	Btn.menu.add_command(label='Troubleshooting',command=troubleshooting)
	Btn.menu.add('separator')
	Btn.menu.add_command(label='Go To Telluric Research ...',command=gotoTelluricResearch)
	Btn.menu.add_command(label='Go To EAMS homepage ...',command=gotoEAMShomepage)
	Btn.menu.add_command(label='Go To Siberia homepage ...',command=gotoSiberiahomepage)
	Btn['menu'] = Btn.menu
	return Btn

def MakeMenuBar():
	global cpu
	global mBar
	mBar = Frame(root, relief=RAISED, borderwidth=0)
	mBar.pack(fill=X)
	FileBtn = makeFileMenu()
	ImportBtn = makeImportMenu()
	SiberiaBtn = makeSiberiaMenu()
	ParametersBtn = makeParametersMenu()
	HelpMenu = makeHelpMenu()
	mBar.tk_menuBar(FileBtn, ImportBtn, SiberiaBtn, ParametersBtn, HelpMenu)
	return

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
#			MAIN PROGRAM
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

def moscow():
	import Pmw
	global root, cpu
	root = Tk()
	cpu=MyCPU(root)
	print (cpu)
	SetTKPlatform(root)
	Pmw.initialise()
#	root.withdraw()
	MakeMenuBar()
	root.title('EAMS 4.00')
	root.mainloop()

