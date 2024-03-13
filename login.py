 
from tkinter import *
from tkinter import messagebox
import customtkinter
from PIL import Image
import pymysql

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

Login = customtkinter.CTk()
Login.geometry("1000x500")
Login.title('Login')
Login.resizable(False,False)

#FUNCTION
def GoToRegister():
    Login.destroy()
    import register

def GoToLogin():
    if UserNameIp.get()=='' or PassWordIp.get()=='':
        messagebox.showerror('Error','Please Enter all field')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='Zstar246')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Cant reach localhost at the moment, Please try later')
            return
        query='use userregistration'
        mycursor.execute(query)

        query='select * from userinfo where username=%s and password=%s'
        mycursor.execute(query,(UserNameIp.get(),PassWordIp.get()))

        row=mycursor.fetchone()

        if row==None:
            messagebox.showerror('Error','Invalid username or Password')
        else:
            messagebox.showinfo('Success','Successfully Logged In')
            import digiboard


LoginFrame=customtkinter.CTkFrame(master=Login,
                                  width=800,
                                  height=500,
                                  fg_color="turquoise",
                                  corner_radius=10)
LoginFrame.pack(padx=50,pady=45)


Img=customtkinter.CTkImage(light_image=Image.open("Backg2.png"),size=(400,400))
ImgBox=customtkinter.CTkLabel(master=LoginFrame,image=Img,text="")
ImgBox.place(x=50,y=10)

LoginImg=customtkinter.CTkImage(light_image=Image.open("loginIcon.png"),size=(100,100))
LoginImgBox=customtkinter.CTkLabel(master=LoginFrame,image=LoginImg,text="")
LoginImgBox.place(x=545,y=15)

LoginTxt=customtkinter.CTkLabel(master=LoginFrame,text="Welcome! User",font=('Century Gothic',24,'bold'))
LoginTxt.place(x=505,y=95)
UserName=customtkinter.CTkLabel(master=LoginFrame,text="Username",font=('Century Gothic',15))
UserName.place(x=450, y=145)

UserNameIp=customtkinter.CTkEntry(master=LoginFrame,width=220,bg_color="transparent",placeholder_text="Username",border_width=0)
UserNameIp.place(x=528, y=145)

PassWord=customtkinter.CTkLabel(master=LoginFrame,text="Password",font=('Century Gothic',15))
PassWord.place(x=450, y=195)

PassWordIp=customtkinter.CTkEntry(master=LoginFrame,width=220,bg_color="transparent",placeholder_text="Password",border_width=0)
PassWordIp.place(x=528, y=195)

LoginBtn= customtkinter.CTkButton(master=LoginFrame, text="LOGIN",font=('Century Gothic',15,'bold'), width=250,command=GoToLogin)
LoginBtn.place(x=475, y=255)

CreateAcTxt=customtkinter.CTkLabel(master=LoginFrame, text="Don't have any account?",font=('Century Gothic',13))
CreateAcTxt.place(x=465, y=295)

CreateAc=Button(master=LoginFrame,text="Create One!",border=0,activebackground="turquoise",cursor='hand2',font=('Century Gothic',11,'bold'),activeforeground="blue",fg='blue',bg="turquoise", command=GoToRegister)
CreateAc.place(x=635, y=293)
Login.mainloop()