from tkinter import *
from tkinter import ttk,messagebox
import subprocess
from ttkthemes import ThemedTk
import tkinter.font as font
import os
from PIL import ImageTk, Image 


'''
command needed:
pip show <package>
-pip list-
-pip install <package>-
pip uninstall <ackage>
'''

root = ThemedTk(theme='equilux')
root.geometry("500x500")
root.resizable(0,0)
icon = PhotoImage(file="easy pip.png")
root.iconphoto(False, icon)
root.title("easy pip")

def get_pip_list():
    raw_list = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE, text=True).stdout.splitlines(False)

    heeder_index = -1 
    i = -1
    for s in raw_list:
        i += 1
        if ('-' in s): 
            heeder_index = i
            break

    raw_list = raw_list[heeder_index+1:] 
    output = []
    for x in raw_list:
        output.append(x.split())

    return output


def install_package():
    name = PackageInput.get()
    outputCode = os.system(f"pip install {name}")
    if outputCode == 0:
        messagebox.showinfo("installed package",f"{name} was install successfully")
        lsit_packages()
    else:
        messagebox.showerror("package installation failed",f"failed to install {name} successfully")


def lsit_packages():
    packageListData = get_pip_list()
    
    for i in range(len(packageListData)):
        PackageList.insert(i,f"{packageListData[i][0]} -- {packageListData[i][1]}")

TitleFrame = ttk.Frame(root,width=100)
TitleFrame.pack()

TitleIconImage = Image.open("easy pip.png").resize((40,40), Image.ANTIALIAS)
TitleIcon = ImageTk.PhotoImage(TitleIconImage)
TitleIconLable = ttk.Label(TitleFrame,image=TitleIcon)
TitleIconLable.pack(side="left")

LoadingIconImage = ImageTk.PhotoImage(Image.open("loading.png").resize((40,40),Image.ANTIALIAS))
LoadingIcon = ttk.Label(TitleFrame,image=LoadingIconImage)


TitleFont = font.Font(family='Helvetica', size=20, weight='bold')
titleText = ttk.Label(TitleFrame,text="easy pip",font=TitleFont,width=500)
titleText.pack()

PackageInputFrame = ttk.Frame(root,width=500,height=10)
PackageInputFrame.pack()

InputFont = font.Font(family="Helvetica",size=15)
PackageInput = ttk.Entry(PackageInputFrame,font=InputFont,width=38)
PackageInput.focus_set()
PackageInput.pack(side='left')

InstallButton = ttk.Button(PackageInputFrame,text="install",width=10,command=install_package)
InstallButton.pack(side='right')

PackageListFrame = ttk.Frame(root)
PackageListFrame.pack()
scroll = ttk.Scrollbar(PackageInputFrame, orient=VERTICAL)
PackageList = Listbox(PackageListFrame,yscrollcommand=scroll.set,height=30,width=100,font=font.Font(family="Helvetica",size=15))
PackageList.configure(background="#464646",foreground="#798585",border=0)
scroll.config(command=PackageList.yview)
scroll.pack(side=LEFT,fill=Y)
PackageList.pack(side=LEFT)
lsit_packages()

BottomButtonTray = ttk.Frame(root,width=100)
BottomButtonTray.pack(side=LEFT)

root.mainloop()