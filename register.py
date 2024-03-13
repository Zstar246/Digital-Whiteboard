from tkinter import *
import customtkinter
from tkinter import messagebox
from PIL import Image
import pymysql


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

Register = customtkinter.CTk()
Register.geometry("1000x500")
Register.title('Login')
Register.resizable(False,False)

#FUNCTION
def GoToLogin():
    Register.destroy()
    import login

def clear():
    UserNameIp.delete(0,END)
    EmailIp.delete(0,END)
    PassWordIp.delete(0,END)
    ConfirmPassIp.delete(0,END)

def ConnectDatabase():
    
    if UserNameIp.get()=='' or EmailIp.get()=='' or PassWordIp.get()=='' or ConfirmPassIp.get()=='':
        messagebox.showerror('Error','Please Enter all field')
    elif PassWordIp.get() != ConfirmPassIp.get():
        messagebox.showerror('Error','Password Mismatched')
    elif Check.get()==0:
        messagebox.showerror('Error','Please Accept the Terms & Condition')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='Zstar246')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Cant reach localhost at the moment, Please try later')
            return
        try:
            query='create database userregistration'
            mycursor.execute(query)
            query='use userregistration'
            mycursor.execute(query)
            query='create table userinfo(id int auto_increment primary key not null, username varchar(100), email varchar(50), password varchar(10))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userregistration')
            
        
        query='select * from userinfo where username=%s'
        mycursor.execute(query,(UserNameIp.get()))

        row = mycursor.fetchone()
        if row != None:
            messagebox.showerror('Error','UserName Already Exists')
        

        query='insert into userinfo(username,email,password) values(%s,%s,%s)'
        mycursor.execute(query,(UserNameIp.get(),EmailIp.get(),PassWordIp.get()))
        con.commit()
        con.close()
        messagebox.showinfo('Success','Registration Successful')

        clear()


    


LoginFrame=customtkinter.CTkFrame(master=Register,
                                  width=800,
                                  height=500,
                                  fg_color="lightblue",
                                  corner_radius=10)
LoginFrame.pack(padx=25,pady=20)


Img=customtkinter.CTkImage(light_image=Image.open("Register.png"),size=(400,400))
ImgBox=customtkinter.CTkLabel(master=LoginFrame,image=Img,text="")
ImgBox.place(x=50,y=10)
RegisterTxt=customtkinter.CTkLabel(master=LoginFrame,text="Let's Register",font=('Century Gothic',24,'bold'),text_color="grey")
RegisterTxt.place(x=525,y=65)
UserName=customtkinter.CTkLabel(master=LoginFrame,text="Username*",font=('Century Gothic',15))
UserName.place(x=450, y=98)

UserNameIp=customtkinter.CTkEntry(master=LoginFrame,width=300,bg_color="transparent",placeholder_text="Username",border_width=0)
UserNameIp.place(x=450, y=120)

Email=customtkinter.CTkLabel(master=LoginFrame,text="Email Id*",font=('Century Gothic',15))
Email.place(x=450, y=148)

EmailIp=customtkinter.CTkEntry(master=LoginFrame,width=300,bg_color="transparent",placeholder_text="Email Id",border_width=0)
EmailIp.place(x=450, y=170)

PassWord=customtkinter.CTkLabel(master=LoginFrame,text="Password*",font=('Century Gothic',15))
PassWord.place(x=450, y=198)

PassWordIp=customtkinter.CTkEntry(master=LoginFrame,width=300,bg_color="transparent",placeholder_text="Password",border_width=0)
PassWordIp.place(x=450, y=220)

ConfirmPass=customtkinter.CTkLabel(master=LoginFrame,text="Confirm Password*",font=('Century Gothic',15))
ConfirmPass.place(x=450, y=250)

ConfirmPassIp=customtkinter.CTkEntry(master=LoginFrame,width=300,bg_color="transparent",placeholder_text="Confirm your Password",border_width=0)
ConfirmPassIp.place(x=450, y=272)

#Checking Whether clicked the checkBox or not
Check=IntVar()
CheckBox=Checkbutton(master=LoginFrame,text="I agree to the Term & Condition",font=('Century Gothic',9,'bold'),foreground="green",border=0,background="lightblue",activebackground="lightblue",cursor='hand2',activeforeground='green',variable=Check)
CheckBox.place(x=495, y=310)

RegisterBtn= customtkinter.CTkButton(master=LoginFrame, text="REGISTER",font=('Century Gothic',15,'bold'), width=250, command=ConnectDatabase )
RegisterBtn.place(x=475, y=340)

LoginTxt=customtkinter.CTkLabel(master=LoginFrame, text="Already registered? then,",font=('Century Gothic',13),text_color="black")
LoginTxt.place(x=445, y=375)

LoginAc=Button(master=LoginFrame,text="Login to your account",border=0,activebackground="lightblue",cursor='hand2',font=('Century Gothic',11,'bold'),activeforeground="blue",fg='blue',bg="lightblue",command=GoToLogin)
LoginAc.place(x=605, y=375)


Register.mainloop()