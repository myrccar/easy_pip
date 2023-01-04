from tkinter import *
from tkinter import ttk,messagebox,END
import subprocess
from ttkthemes import ThemedTk
import tkinter.font as font
import os
from PIL import ImageTk, Image 
import webbrowser


'''
commands needed:
-pip show <package>-
-pip list-
-pip install <package>-
-pip uninstall <ackage>-
'''

root = ThemedTk(theme='equilux',background="#464646")
root.geometry("500x500")
root.resizable(0,0)
icon = PhotoImage(file="img/easy pip.png")
root.iconphoto(False, icon)
root.title("easy pip")
root.config(cursor="arrow")

MainWindow = ttk.Frame(root)
PackageInfoWindow = ttk.Frame(root)

pip_list = []
PackageInfo = ["none" for i in range(9)]

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

pip_list = get_pip_list()

def install_package():
    loading(True)
    root.update()
    name = PackageInput.get()
    outputCode = os.system(f"pip install {name}")
    loading(False)
    root.update()
    if outputCode == 0:
        messagebox.showinfo("installed package",f"{name} was install successfully")
        lsit_packages()
    else:
        messagebox.showerror("package installation failed",f"failed to install {name} successfully")


def lsit_packages():
    packageListData = get_pip_list()
    PackageList.delete(0,END)
    for i in range(len(packageListData)):
        PackageList.insert(i,f"{packageListData[i][0]} -- {packageListData[i][1]}")
    pip_list = packageListData

def remove_package():
    PackageName = PackageList.get(PackageList.curselection()[0]).split()[0]
    if messagebox.askokcancel("package removal ahead",f"are you sure you want to remove {PackageName}"):
        loading(True)
        root.update()
        ExitCode = os.system(f"pip uninstall -y {PackageName}")
        loading(False)
        root.update()
        if not ExitCode:
            messagebox.showinfo(f"successfully removed {PackageName}",f"the package: {PackageName} has been removed from your system")
        else:
            messagebox.showerror("package uninstalling failed",f"failed to uninstall {PackageName} successfully")
        lsit_packages()

def loading(Loading):
    if Loading:
        LoadingIcon.place(x=200,y=200)
    else:
        LoadingIcon.place_forget()
    return

def update_package():
    loading(True)
    root.update()
    PackageName = PackageList.get(PackageList.curselection()[0]).split()[0]
    ExitCode = os.system(f"pip install {PackageName} -U --user")
    loading(False)
    root.update()
    if not ExitCode:
        messagebox.showinfo("updated package",f"{PackageName} was updated successfully")
    else:
        messagebox.showerror("package update failed",f"failed to update {PackageName} successfully")
    lsit_packages()


def search_list(event):
    Value = PackageInput.get().lower()

    if not Value == "":
        PackageList.delete(0,END)


        for x in pip_list:
            if Value in x[0].lower()[0:len(Value)]:
                PackageList.insert(END,f"{x[0]} -- {x[1]}")
    else:
        PackageList.delete(0,END)
        for x in pip_list:
            PackageList.insert(END,f"{x[0]} -- {x[1]}")

def get_info():
    loading(True)
    root.update()
    PackageName = PackageList.get(PackageList.curselection()[0]).split()[0]

    output = subprocess.run(['pip', 'show',PackageName], stdout=subprocess.PIPE, text=True).stdout.splitlines(False)
    #error check\/
    if output == []:
        messagebox.showerror("package info faild",f"failed to get info on {PackageName} successfully")
    else:
        global PackageInfo 
        PackageInfo = []
        PackageInfo.append(output[0].split("Name: ")[1])
        PackageInfo.append(output[1].split("Version: ")[1])
        PackageInfo.append(output[2].split("Summary: ")[1])
        PackageInfo.append(output[3].split("Home-page: ")[1])
        PackageInfo.append(output[4].split("Author: ")[1])
        PackageInfo.append(output[5].split("Author-email: ")[1])
        PackageInfo.append(output[6].split("License: ")[1])
        PackageInfo.append(output[7].split("Location: ")[1])
        PackageInfo.append(output[8].split("Requires: ")[1].replace(",",""))
        PackageInfo.append(output[9].split("Required-by: ")[1].replace(",",""))

        #show info window
        PackageInfoWindow.pack(side=BOTTOM,fill=BOTH,expand=True)
        #update text
        PackageNameLable.config(text=PackageInfo[0])
        PackageDscription.config(text=PackageInfo[2])
        PackageVersion.config(text=PackageInfo[1])
        PackageUrl.config(text=PackageInfo[3])
        AuthorName.config(text=f'Author: {PackageInfo[4]} - {PackageInfo[5]}')
        PackageLicense.config(text=f'License: {PackageInfo[6]}')
        PackageLocation.config(text=f'Location: {PackageInfo[7]}')
        #hide main window
        MainWindow.pack_forget()
        loading(False)
        root.update()

def hide_info():
    PackageInfoWindow.pack_forget()
    MainWindow.pack(side=BOTTOM,fill=BOTH,expand=True)

TitleFrame = ttk.Frame(root,width=100)
TitleFrame.pack()

TitleIconImage = Image.open("img/easy pip.png").resize((40,40), Image.ANTIALIAS)
TitleIcon = ImageTk.PhotoImage(TitleIconImage)
TitleIconLable = ttk.Label(TitleFrame,image=TitleIcon)
TitleIconLable.pack(side=LEFT)

LoadingIconImage = ImageTk.PhotoImage(Image.open("img/loading.png").resize((100,100),Image.ANTIALIAS))
LoadingIcon = ttk.Label(root,image=LoadingIconImage)


TitleFont = font.Font(family='Helvetica', size=20, weight='bold')
titleText = ttk.Label(TitleFrame,text="easy pip",font=TitleFont,width=500)
titleText.pack()

PackageInputFrame = ttk.Frame(MainWindow,width=500,height=10)
PackageInputFrame.pack()

InputFont = font.Font(family="Helvetica",size=15)
PackageInput = ttk.Entry(PackageInputFrame,font=InputFont,width=38)
PackageInput.focus_set()
PackageInput.pack(side='left')
PackageInput.bind('<KeyRelease>',search_list)
PackageInput.bind('<Return>',lambda event: install_package())

InstallButton = ttk.Button(PackageInputFrame,text="install",width=10,command=install_package)
InstallButton.pack(side='right')

PackageListFrame = ttk.Frame(MainWindow)
PackageListFrame.pack()
scroll = ttk.Scrollbar(PackageInputFrame, orient=VERTICAL)
PackageList = Listbox(PackageListFrame,yscrollcommand=scroll.set,height=16,width=100,font=font.Font(family="Helvetica",size=15))
PackageList.configure(background="#464646",foreground="#798585",border=0)
scroll.config(command=PackageList.yview)
scroll.pack(side=LEFT,fill=Y)
PackageList.pack(side=LEFT)
lsit_packages()

BottomButtonTray = ttk.Frame(MainWindow,width=1000,height=200)
BottomButtonTray.pack(fill="both", expand=True)

for i in range(3):
    BottomButtonTray.columnconfigure(i, weight=1)
BottomButtonTray.rowconfigure(0, weight=1)

InfoButton = ttk.Button(BottomButtonTray,width=10,text="info",command=get_info)
InfoButton.grid(row=0,column=0, sticky="nsew")

UpdateButton = ttk.Button(BottomButtonTray,width=10,text="update",command=update_package)
UpdateButton.grid(row=0,column=1, sticky="nsew")

RemoveButton = ttk.Button(BottomButtonTray,width=10,text="remove",command=remove_package)
RemoveButton.grid(row=0,column=2, sticky="nsew")

#package info window

PackageInfoWindow.columnconfigure(0,weight=1)


PackageNameFrame = ttk.Frame(PackageInfoWindow,width=100)
PackageNameFrame.grid(column=0,row=0,sticky="w")

PackageNameLable = ttk.Label(PackageNameFrame,text=PackageInfo[0],font=font.Font(size=30))
PackageNameLable.grid(column=0,row=0,sticky="wns")

PackageVersion = ttk.Label(PackageNameFrame,text="2.2.2",font=font.Font(size=13))
PackageVersion.grid(column=1,row=0,sticky="wsn")

PackageInfoClose = ttk.Button(PackageInfoWindow,text="X",width=3,command=hide_info)
PackageInfoClose.grid(column=1,row=0,sticky="esn",padx=(0,5))

PackageInputFrame.pack(side=TOP)

PackageDscription = ttk.Label(PackageInfoWindow,text="A simple framework for building complex web applications.",wraplength=400,font=font.Font(size=13))
PackageDscription.grid(column=0,row=1,sticky="w",pady=(5,0))

PackageUrl = ttk.Label(PackageInfoWindow,text="blabla",wraplength=500,font=font.Font(size=10),foreground="darkblue")
PackageUrl.grid(column=0,row=2,sticky="w",pady=(10,0))
PackageUrl.bind("<Button-1>",lambda x: webbrowser.open(PackageInfo[3]))
PackageUrl.bind("<Enter>", lambda x: PackageUrl.config(font=font.Font(size=10,family="Helvetica",underline=True)))
PackageUrl.bind("<Leave>", lambda x: PackageUrl.config(font=font.Font(size=10,family="Helvetica",underline=False)))

AuthorName = ttk.Label(PackageInfoWindow,text="myrccar - idk@gmail.com",font=font.Font(size=10))
AuthorName.grid(column=0,row=3,sticky="w",pady=(1,0))

PackageLicense = ttk.Label(PackageInfoWindow,text="",font=font.Font(size=10))
PackageLicense.grid(column=0,row=4,sticky="w",pady=(1,0))

PackageLocation = ttk.Label(PackageInfoWindow,text="C:/idk",font=font.Font(size=10))
PackageLocation.grid(column=0,row=5,sticky="w",pady=(1,0))
PackageLocation.bind("<Button-1>",lambda x: os.system(f"start {PackageInfo[7]}"))
PackageLocation.bind("<Enter>", lambda x: PackageLocation.config(font=font.Font(size=10,family="Helvetica",underline=True)))
PackageLocation.bind("<Leave>", lambda x: PackageLocation.config(font=font.Font(size=10,family="Helvetica",underline=False)))

MainWindow.pack(side=BOTTOM,fill=BOTH,expand=True)
#PackageInfoWindow.pack(side=BOTTOM,fill=BOTH,expand=True)
root.mainloop()