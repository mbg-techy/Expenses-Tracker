import tkinter as tk
import customtkinter as ctk
import psycopg2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from tkinter import messagebox
from datetime import datetime
import csv
from tkinter import ttk

app = ctk.CTk()
app.geometry("1200x700")
app.title("Expense Tracker")
ctk.set_appearance_mode("dark")

bg_image = ctk.CTkImage(
    light_image=Image.open("D:\\expense_tracker\\background.jpg"),
    dark_image=Image.open("D:\\expense_tracker\\background.jpg"),
    size=(1200, 700),
)

bg_label = ctk.CTkLabel(app, image=bg_image, text="Expense Tracker")
bg_label.place(x=0, y=0)

frame = ctk.CTkFrame(master=app, width=1200, height=700, corner_radius=0, fg_color="transparent")
frame.place(x=0, y=0)

frame2 = ctk.CTkFrame(master=app, width=1200, height=700, corner_radius=0)
frame3 = ctk.CTkFrame(master=app, width=1200, height=700, corner_radius=0)
frame6 = ctk.CTkFrame(master=app, width=1200, height=700, corner_radius=0)
frame7 = ctk.CTkFrame(master=app, width=1200, height=700, corner_radius=0)

conn = psycopg2.connect(database="Expense Tracker", user="tracker_user", password="tracker123", host="localhost", port="5432")
userid = None

logo_image = ctk.CTkImage(Image.open("side.png"), size=(50, 50))

def add_header(frame):
    logo_label = ctk.CTkLabel(frame, image=logo_image, text="")
    logo_label.place(x=20, y=20)

    app_name_label = ctk.CTkLabel(frame, text="My Expense Tracker", font=("Arial", 24, "bold"))
    app_name_label.place(x=80, y=28)

def clear_frame_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def signUp_page():
    frame3.place_forget()
    frame2.place(x=0, y=0)
    add_header(frame)

    def submit():
        get_userid = userid_entry.get()
        get_password = password_entry.get()
        get_name = name_entry.get()

        if not get_userid or not get_password or not get_name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        cur = conn.cursor()
        cur.execute("SELECT * FROM userinfo WHERE userid = %s", (get_userid,))
        if cur.fetchone():
            messagebox.showerror("Error", "User already exists.")
            cur.close()
        else:
            cur.execute(
                "INSERT INTO userinfo (userid, password, user_name) VALUES (%s, %s, %s)",
                (get_userid, get_password, get_name),
            )
            conn.commit()
            cur.close()
            messagebox.showinfo("Success", "User Registered")
            frame2.place_forget()
            login_page()

    label = ctk.CTkLabel(master=frame2, text="Sign Up", font=("Arial", 30))
    label.place(x=520, y=100)

    userid_entry = ctk.CTkEntry(master=frame2, placeholder_text="User ID")
    userid_entry.place(x=480, y=180)

    password_entry = ctk.CTkEntry(master=frame2, placeholder_text="Password", show="*")
    password_entry.place(x=480, y=240)

    name_entry = ctk.CTkEntry(master=frame2, placeholder_text="Name")
    name_entry.place(x=480, y=300)

    signUp_button = ctk.CTkButton(master=frame2, text="Submit", command=submit)
    signUp_button.place(x=530, y=360)

    login_button = ctk.CTkButton(master=frame2, text="Back to Login", command=login_page)
    login_button.place(x=515, y=420)


def login_page():
    frame2.place_forget()
    frame.place_forget()
    frame6.place_forget()
    frame7.place_forget()
    frame3.place(x=0, y=0)
    clear_frame_widgets(frame3)
    add_header(frame)

    def login():
        global userid
        entered_userid = userid_entry.get().strip()
        entered_password = password_entry.get().strip()

        if not entered_userid or not entered_password:
            messagebox.showerror("Error", "Please enter both User ID and Password.")
            return

        cur = conn.cursor()
        cur.execute("SELECT * FROM userinfo WHERE userid = %s AND password = %s", (entered_userid, entered_password))
        result = cur.fetchone()
        cur.close()

        if result:
            userid = entered_userid
            messagebox.showinfo("Success", f"Welcome, {result[2]}!")  # assuming user_name is 3rd col
            frame3.place_forget()
            home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Try again.")

    # GUI
    label = ctk.CTkLabel(master=frame3, text="Login", font=("Arial", 30))
    label.place(x=480, y=150)

    userid_entry = ctk.CTkEntry(master=frame3, placeholder_text="User ID")
    userid_entry.place(x=480, y=230)

    password_entry = ctk.CTkEntry(master=frame3, placeholder_text="Password", show="*")
    password_entry.place(x=480, y=290)

    login_button = ctk.CTkButton(master=frame3, text="Login", command=login)
    login_button.place(x=480, y=350)

    signUp_button = ctk.CTkButton(master=frame3, text="Create Account", command=signUp_page)
    signUp_button.place(x=480, y=410)


def home_page():
    frame6.place_forget()
    frame7.place_forget()
    clear_frame_widgets(frame)
    frame.place(x=0, y=0)
    add_header(frame)


    def set_budget():
        frame.place_forget()
        frame6.place(x=0, y=0)
        clear_frame_widgets(frame6)

        ctk.CTkLabel(master=frame6, text="Set Monthly Budget", font=("Arial", 24)).place(x=480, y=120)

        # Month selector
        ctk.CTkLabel(master=frame6, text="Select Month:").place(x=360, y=180)
        month_combobox = ttk.Combobox(frame6,width=20, values=[
            "01 - January", "02 - February", "03 - March", "04 - April", "05 - May", "06 - June",
            "07 - July", "08 - August", "09 - September", "10 - October", "11 - November", "12 - December"
        ])
        month_combobox.place(x=530, y=180)
        month_combobox.set(datetime.now().strftime("%m - %B"))

        # Year selector
        ctk.CTkLabel(master=frame6, text="Select Year:").place(x=360, y=230)
        current_year = datetime.now().year
        year_combobox = ttk.Combobox(frame6,width=20, values=[str(y) for y in range(current_year - 10, current_year + 34)])
        year_combobox.place(x=530, y=230)
        year_combobox.set(str(current_year))

        # Budget entry
        amount_entry = ctk.CTkEntry(master=frame6, placeholder_text="Budget Amount")
        amount_entry.place(x=530, y=280)

        def submit_budget():
            month_selected = month_combobox.get().strip()
            year_selected = year_combobox.get().strip()
            amount = amount_entry.get().strip()

            if not month_selected or not year_selected or not amount:
                messagebox.showerror("Error", "Fill all fields")
                return

            try:
                float(amount)
            except:
                messagebox.showerror("Error", "Amount must be a number")
                return

            # Format month in YYYY-MM
            month_number = month_selected.split(" - ")[0]
            month = f"{year_selected}-{month_number}"

            cur = conn.cursor()
            cur.execute("""
                INSERT INTO monthly_budget (userid, month, budget)
                VALUES (%s, %s, %s)
                ON CONFLICT (userid, month) DO UPDATE SET budget = EXCLUDED.budget
            """, (userid, month, amount))
            conn.commit()
            cur.close()

            messagebox.showinfo("Success", f"Budget of ₹{amount} set for {month}")
            home_page()

        ctk.CTkButton(master=frame6, text="Save Budget", command=submit_budget).place(x=530, y=340)
        ctk.CTkButton(master=frame6, text="Back", command=home_page).place(x=530, y=400)

    
    
    def Add_Expenses():
        frame.place_forget()
        frame6.place(x=0, y=0)
        clear_frame_widgets(frame6) 
        def check_budget():
            today = datetime.now()
            this_month = today.strftime("%Y-%m")
            cur = conn.cursor()

            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM expense 
                WHERE userid = %s AND TO_CHAR(date, 'YYYY-MM') = %s
            """, (userid, this_month))
            total_spent = cur.fetchone()[0]

            cur.execute("SELECT budget FROM monthly_budget WHERE userid = %s AND month = %s", (userid, this_month))
            row = cur.fetchone()
            cur.close()

            if row:
                budget = row[0]
                percent = (total_spent / budget) * 100
                if percent > 100:
                    messagebox.showwarning("Over Budget!", f"⚠️ You have exceeded your monthly budget of ₹{budget}")
                elif percent >= 80:
                    messagebox.showinfo("Budget Alert", f"You're at {percent:.1f}% of your ₹{budget} budget.")

        def submit():
            get_amount = amount.get()
            get_expense_type = expense_type.get()
            get_date_raw = date.get()
            get_comment = comment.get()

            if not get_amount or not get_expense_type or not get_date:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            try:
                float(get_amount)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
                return
            try:
                get_date_obj = datetime.strptime(get_date_raw, "%Y-%m-%d")
                get_date = get_date_obj.date()
            except ValueError:
                messagebox.showerror("Invalid Date Format", "Please enter the date in YYYY-MM-DD format.")
                return

            cur = conn.cursor()
            cur.execute(
                "INSERT INTO expense (userid, amount, expense_type, date, comment) VALUES (%s, %s, %s, %s, %s)",
                (userid, get_amount, get_expense_type, get_date, get_comment)
            )
            conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Expense added")
            frame6.place_forget()
            check_budget()
            home_page()

        label = ctk.CTkLabel(master=frame6, text="Add Expense", font=("Arial", 30))
        label.place(x=510, y=100)

        amount = ctk.CTkEntry(master=frame6, placeholder_text="Enter Amount")
        amount.place(x=480, y=180)

        expense_type = ctk.CTkOptionMenu(master=frame6, values=["Food", "Travel", "Shopping", "Rent", "Other"])
        expense_type.place(x=480, y=240)

        date = ctk.CTkEntry(master=frame6, placeholder_text="Enter Date (YYYY-MM-DD)")
        date.place(x=480, y=300)

        comment = ctk.CTkEntry(master=frame6, placeholder_text="Add Comment (optional)")
        comment.place(x=480, y=360)

        submit_button = ctk.CTkButton(master=frame6, text="Submit", command=submit)
        submit_button.place(x=530, y=420)

        back_button = ctk.CTkButton(master=frame6, text="Back", command=home_page)
        back_button.place(x=530, y=480)



    def Data():
        frame.place_forget()
        frame7.place(x=0, y=0)
        clear_frame_widgets(frame7)

        cur = conn.cursor()
        cur.execute("SELECT expense_type, SUM(amount) FROM expense WHERE userid = %s GROUP BY expense_type", (userid,))
        data = cur.fetchall()
        cur.close()

        if data:
            types = [row[0] for row in data]
            amounts = [row[1] for row in data]

            fig, ax = plt.subplots()
            ax.pie(amounts, labels=types, autopct='%1.1f%%')
            ax.set_title("Expense Distribution")

            Data.canvas = FigureCanvasTkAgg(fig, master=frame7)
            Data.canvas.draw()
            Data.canvas.get_tk_widget().place(x=100,y=100)
    
            def export_csv():
                    cur = conn.cursor()
                    cur.execute("SELECT amount, expense_type, date, comment FROM expense WHERE userid = %s", (userid,))
                    records = cur.fetchall()
                    cur.close()

                    if not records:
                        messagebox.showinfo("No Data", "No expenses to export.")
                        return

                    filename = f"{userid}_expenses.csv"
                    with open(filename, "w", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Amount", "Type", "Date", "Comment"])
                        writer.writerows(records)

                    messagebox.showinfo("Exported", f"Data exported to {filename}")

        back_button = ctk.CTkButton(master=frame7, text="Back", command=home_page)
        back_button.place(x=500, y=550)
        ctk.CTkButton(master=frame7, text="Export to CSV", command=export_csv).place(x=500, y=500)
        

    add_button = ctk.CTkButton(master=frame, text="Add Expenses", command=Add_Expenses)
    add_button.place(x=500, y=300)

    ctk.CTkButton(master=frame, text="Set Monthly Budget", command=set_budget).place(x=500, y=480)

    data_button = ctk.CTkButton(master=frame, text="View Overall Expenses", command=Data)
    data_button.place(x=500, y=360)

    logout_button = ctk.CTkButton(master=frame, text="Logout", command=login_page)
    logout_button.place(x=500, y=420)




# Start the app at login
login_page()
def on_closing():
    try:
        conn.close()  # close the DB connection
    except:
        pass
    try:
        app.destroy()
    except:
        pass

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
