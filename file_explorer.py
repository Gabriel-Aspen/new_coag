from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

def filesearch(title = None):
	Tk().withdraw()
	filename = askopenfilename(initialdir='./', title=title)
	return filename

FILEPATH = filesearch(title = 'Select an Input File')
df = pd.read_excel(df)
print(df.shape)