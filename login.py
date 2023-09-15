from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import mysql.connector
from tkinter import ttk
import cv2
import os
from deepface import DeepFace as df
from PIL import Image
from mtcnn.mtcnn import MTCNN
from datetime import date, datetime
import time
import csv


def return_recognisedfaces():
    detector = MTCNN()
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Web Camera not available")

    img_dir="C:/Users/arunt/Documents/images"
    start_time = datetime.strptime(time.strftime("%H:%M:%S", (time.localtime())), "%H:%M:%S")
    res_list=[]

    while (True):

        ret, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2Lab)
        clahe = cv2.createCLAHE(clipLimit=5)
        frame[:, :, 0] = clahe.apply(frame[:, :, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_Lab2RGB)
        if ret == True:
            face_location = detector.detect_faces(frame)
            if face_location:
                for face in face_location:
                    x_start, y_start, width, height = face['box']
                    x_end, y_end = x_start + width, y_start + height
                    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (255, 255, 255), 4)
                    face_img = (frame[y_start:y_end, x_start:x_end])
                    # imgs.append(face_img)
                    for j in os.listdir(img_dir):
                        path=os.path.join(img_dir,j)
                        check=False
                        for k in os.listdir(path):
                         img2=os.path.join(path,k)
                         print(img2)
                         res=df.verify(face_img[:,:,::-1],img2_path=img2,model_name="ArcFace",enforce_detection=False)
                         if res["verified"] and res['distance']<0.55:
                             cv2.putText(frame,j,(x_start,y_start-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
                             res_list.append(j)
                             check=True
                             break
                        if check:
                         break

        cv2.imshow("Output", frame)
        curr_time = datetime.strptime(time.strftime("%H:%M:%S", (time.localtime())), "%H:%M:%S")
        delta = curr_time - start_time
        if delta.total_seconds() > 30:
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    return list(set(res_list))


def attendance():
    present_list = return_recognisedfaces()
    print(present_list)
    tvar = time.localtime()
    tvar = time.strftime("%H:%M", tvar)
    with open("C:/Users/arunt/Documents/attendance.csv", "a+") as f:
        writer = csv.writer(f)
        for i in present_list:
            writer.writerow([i, date.today(), tvar])


def admin():
    def ins_t():
        db = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
        print("connected successfully")
        dbcursor = db.cursor()
        user = tun.get()
        password = tpw.get()
        query = "insert into teacher values(%s,%s)"
        dbcursor.execute(query, [(user), (password)])
        db.commit()
        messagebox.showinfo("status", "Registration sucess")

    def ins_s():
        db = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
        print("connected successfully")
        dbcursor = db.cursor()
        user = sun.get()
        password = spw.get()
        query = "insert into student values(%s,%s)"
        dbcursor.execute(query, [(user), (password)])
        db.commit()
        messagebox.showinfo("status", "Registration sucess")

    root = Tk()
    root.geometry("1560x868")
    lg = Label(root, text="Attendance System", fg="white", bg="black", font=('times', 30, ' bold '))
    lg.place(relx=0.39, rely=0.05)
    frame1 = Frame(root, bg="white")
    frame1.place(relx=0.11, rely=0.15, relwidth=0.39, relheight=0.80)

    frame2 = Frame(root, bg="white")
    frame2.place(relx=0.51, rely=0.15, relwidth=0.39, relheight=0.80)

    fr_head1 = Label(frame1, text="Register New Teacher", fg="white", bg="black", font=('times', 17, ' bold '))
    fr_head1.place(x=0, y=0, relwidth=1)

    fr_head2 = Label(frame2, text="Register New Student", fg="white", bg="black", font=('times', 17, ' bold '))
    fr_head2.place(x=0, y=0, relwidth=1)

    lbl = Label(frame1, text="Enter Email Id :", width=20, height=1, fg="black", bg="white", font=('times', 17))
    lbl.place(x=0, y=55)

    tun = Entry(frame1, width=32, fg="black", bg="#e1f2f2", highlightcolor="#00aeff", highlightthickness=3,
                font=('times', 15))
    tun.place(x=55, y=88, relwidth=0.75)

    lbl2 = Label(frame1, text="Enter Password", width=20, fg="black", bg="white", font=('times', 17))
    lbl2.place(x=0, y=140)

    tpw = Entry(frame1, width=32, fg="black", bg="#e1f2f2", highlightcolor="#00aeff", highlightthickness=3,
                font=('times', 15))
    tpw.place(x=55, y=173, relwidth=0.75)

    lbl = Label(frame2, text="Enter RegisterNo :", width=20, height=1, fg="black", bg="white", font=('times', 17))
    lbl.place(x=0, y=55)

    sun = Entry(frame2, width=32, fg="black", bg="#e1f2f2", highlightcolor="#00aeff", highlightthickness=3,
                font=('times', 15))
    sun.place(x=55, y=88, relwidth=0.75)

    lbl2 = Label(frame2, text="Enter Password", width=20, fg="black", bg="white", font=('times', 17))
    lbl2.place(x=0, y=140)

    spw = Entry(frame2, width=32, fg="black", bg="#e1f2f2", highlightcolor="#00aeff", highlightthickness=3,
                font=('times', 15))
    spw.place(x=55, y=173, relwidth=0.75)
    b1 = Button(frame1, text="Create", padx=20, pady=5, command=ins_t)
    b1.place(relx=0.45, rely=0.75)
    b2 = Button(frame2, text="Create", padx=20, pady=5, command=ins_s)
    b2.place(relx=0.45, rely=0.75)
    root.mainloop()


def student():
    top = Tk()
    top.title("Attendance Management System")
    top.geometry("800x800")
    myFont = tkFont.Font(family='Times')
    tree = ttk.Treeview(top, column=("c1", "c2", "c3"), show='headings')
    label = Label(top, text="Attendance table", font=('Times', 20)).place(relx=0.4, rely=0.2)

    tree.column("#1", anchor=CENTER)

    tree.heading("#1", text="REGD NO.")

    tree.column("#2", anchor=CENTER)

    tree.heading("#2", text="DATE")

    tree.column("#3", anchor=CENTER)

    tree.heading("#3", text="TIME")

    tree.place(relx=0.3, rely=0.3)

    style = ttk.Style()

    style.theme_use("clam")
    style.configure("Treeview",
                    background="silver",
                    foreground="black",
                    rowheight=55,
                    fieldbackground="silver")
    with open("C:/Users/arunt/Documents/attendance.csv") as f:
        reader = csv.DictReader(f, delimiter=',')
        myFont = tkFont.Font(family='Times')
        for row in reader:
            name = row['Name']
            date_today = row['Date']
            time_now = row['Time']
            if name == user:
                tree.insert("", 0, values=(name, date_today, time_now))


def teacher():
    def show():
        tree = ttk.Treeview(top, column=("c1", "c2", "c3"), show='headings')

        tree.column("#1", anchor=CENTER)

        tree.heading("#1", text="REGD NO.")

        tree.column("#2", anchor=CENTER)

        tree.heading("#2", text="DATE")

        tree.column("#3", anchor=CENTER)

        tree.heading("#3", text="TIME")

        tree.place(relx=0.3, rely=0.3)
        style = ttk.Style()

        style.theme_use("clam")
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=55,
                        fieldbackground="silver")
        with open("C:/Users/arunt/Documents/attendance.csv") as f:
            reader = csv.DictReader(f, delimiter=',')
            myFont = tkFont.Font(family='Times')
            for row in reader:
                name = row['Name']
                date_today = row['Date']
                time_now = row['Time']
                if str(date_today) == str(date.today()):
                    tree.insert("", 0, values=(name, date_today, time_now))

    top = Tk()
    top.title("Attendance Management System")
    top.geometry("800x800")
    myFont = tkFont.Font(family='Times')
    b1 = Button(top, text="Take Attendance", bg="skyblue", width=30, height=2, font=myFont, command=attendance).place(
        relx=0.2, rely=0.1)
    b2 = Button(top, text="show attendance", bg="skyblue", width=30, height=2, font=myFont, command=show).place(
        relx=0.5, rely=0.1)
    label = Label(top, text="Attendance table", font=('Times', 20)).place(relx=0.4, rely=0.2)


user = ""


def log():
    global user
    print("login")
    db = mysql.connector.connect(host="localhost", user="root", password="", database="attendance_system")
    print("connected successfully")
    dbcursor = db.cursor()
    user = un.get()
    password = pw.get()
    role = clicked.get()
    if role == "Admin":
        query = "select * from admin where username = %s and password= %s"
        dbcursor.execute(query, [(user), (password)])
        result = dbcursor.fetchall()
        if result:
            messagebox.showinfo("status", "Login sucess")
            root.destroy()
            admin()
        else:
            messagebox.showinfo("status", "invalid credentials")
    if role == "Teacher":
        query = "select * from teacher where username = %s and password= %s"
        dbcursor.execute(query, [(user), (password)])
        result = dbcursor.fetchall()
        if result:
            messagebox.showinfo("status", "Login sucess")
            root.destroy()
            teacher()
        else:
            messagebox.showinfo("status", "invalid credentials")
    if role == "Student":
        query = "select * from student where username = %s and password= %s"
        dbcursor.execute(query, [(user), (password)])
        result = dbcursor.fetchall()
        if result:
            messagebox.showinfo("status", "Login sucess")
            root.destroy()
            student()
        else:
            messagebox.showinfo("status", "invalid credentials")


root = Tk()
root.title("Login")
label1 = Label(root, text="Login", font=('Times', 30))
label1.place(relx=0.45, rely=0.35)
lab1 = Label(root, text="Username :", font=('Times', 15))
lab1.place(relx=0.4, rely=0.45)
un = Entry(root, width=30, borderwidth=5)
un.place(relx=0.5, rely=0.45)
label3 = Label(root, text="Password :", font=('Times', 15))
label3.place(relx=0.4, rely=0.55)
pw = Entry(root, width=30, borderwidth=5)
pw.place(relx=0.5, rely=0.55)
label4 = Label(root, text="Select user type", font=('Times', 15))
label4.place(relx=0.4, rely=0.65)
clicked = StringVar()
clicked.set("Admin")
drop = OptionMenu(root, clicked, "Admin", "Teacher", "Student")
drop.config(bg="lightBlue")
drop.place(relx=0.5, rely=0.65)
button1 = Button(root, text="Login", padx=20, pady=5, command=log)
button1.place(relx=0.5, rely=0.75)
root.mainloop()