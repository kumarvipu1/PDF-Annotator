import warnings
warnings.filterwarnings('ignore')
import fitz
from tkinter import *
from tkinter import filedialog

#=======MAIN FUNCTION==========================#
#==============================================#
class Annotate_keywords:
    def __init__(self, path, kw):
        self.path = path
        self.kw = kw

    def sentence_break(self):
        path = self.path
        doc = fitz.open(path)
        para = []
        for page in doc:
                blocks = page.getText("dict")["blocks"]
                for b in blocks:
                    if b['type'] == 0:
                        block_string = ""
                        for l in b["lines"]:
                            for s in l["spans"]:
                                if s['text'].strip():
                                    block_string = s['text']
                                    para.append(block_string)
        return para

    def sentence_to_highlight(self):
        para = self.sentence_break()
        sentence_to_highlight = []
        kw = self.kw
        for sentence in para:
            for word in kw:
                if word in sentence:
                    sentence = sentence.replace('\n', '')
                    sentence_to_highlight.append(sentence)

        return sentence_to_highlight

    #t = sentence_to_highlight
    #q = kw

    def annotate(self):
        doc = fitz.open(self.path)
        n = doc.page_count
        q = self.kw
        t = self.sentence_to_highlight()
        for i in range(n):
            page = doc[i]
            for i in range(len(t)):
                rl = page.search_for(t[i], quads = True)
                highlight = page.addHighlightAnnot(rl)
                highlight.update()

            for i in range(len(q)):
                r2 = page.search_for(q[i], quads = True)
                highlight2 = page.addSquigglyAnnot(r2)
                highlight2.update()

        doc.save('new_doc5.pdf')


#===================GUI===========================#
#=================================================#
root = Tk()

myLabel2 = Label(root, text = 'Enter Keyword')
e2 = Entry(root, width = 50)
myLabel2.pack()
e2.pack()

kw = []
def update_keyword():
    global kw
    kw.append(e2.get())
    myLabel3 = Label(root, text='Add another keyword and update or select document to annotate')
    myLabel3.pack()

my_btn3 = Button(root, text = 'Update Keyword', command = update_keyword).pack()

path1 = ''
def open():
    global path1
    root.filename = filedialog.askopenfilename(initialdir = 'C:/',
                                           title = 'select doc')
    path1 = root.filename
    myLabel3 = Label(root, text= 'you are annotating' + path1)
    myLabel3.pack()

my_btn1 = Button(root, text = 'Select your file', command = open).pack()

def myClick():
    Annotate_keywords(path1, kw).annotate()
    myLabel3 = Label(root, text= 'Your File is ready, check in folder')
    myLabel3.pack()

    '''
    myLabel3 = Label(root, text='Your annotated document is ready, check your folder')
    myLabel3.pack()
    '''

myButton = Button(root, text = 'Get Document', command = myClick)
myButton.pack()

root.mainloop()

#=====================================================================================================#





