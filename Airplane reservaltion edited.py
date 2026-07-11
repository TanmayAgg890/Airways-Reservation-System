import customtkinter as ctk
from PIL import Image
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Budget tracking

main = ctk.CTk()
main.title("Flight Reservation System")
main.configure(fg_color="#d8cfc4")

# login/register page
frame1 = ctk.CTkFrame(main, fg_color="white", width=350, height=400, border_width=6, border_color="#601E88")
frame1.pack_propagate(0)
frame1.pack(expand=True, side="right", padx=(0, 425))

# email logo
email_icon_data = Image.open("email-icon.png")
email_icon = ctk.CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))

pass_icon_data = Image.open("password-icon.png")
pass_icon = ctk.CTkImage(dark_image=pass_icon_data, light_image=pass_icon_data, size=(15, 15))

# side image
side_img_data = Image.open("side-img.png")
side_img = ctk.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(350, 400))
label_sideimage = ctk.CTkLabel(main, text="", image=side_img)
label_sideimage.pack(side="left", padx=(425, 0))



# setup the MySQL database for us
def db_setup():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="airplane_reservation1"
    )
    crsr = conn.cursor()

    crsr.execute('''CREATE TABLE IF NOT EXISTS passengers (
                        passenger_id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255) UNIQUE,
                        password VARCHAR(255),
                        name VARCHAR(255))''')

    conn.commit()
    conn.close()
    ctk.set_appearance_mode("Dark")
    current_total = 0
    BUDGET_LIMIT = 15000 # Your custom limit
def clear_window1():
    for widget in frame1.winfo_children():
        widget.destroy()

def clear_window2():
    for widget in main.winfo_children():
        if widget != frame1:
            widget.destroy()

def login_screen():
    global email_input1, pass_input1
    clear_window1()
    head_login = ctk.CTkLabel(frame1, text="LOGIN", font=("Arial", 24, "bold"), text_color="#601E88")
    head_login.pack(pady=(30, 0))

    email_label1 = ctk.CTkLabel(frame1, text="E-mail", text_color="Black", font=("Roboto", 13, "bold"), image=email_icon, compound="left")
    email_label1.pack(pady=(50, 0))
    email_input1 = ctk.CTkEntry(frame1, placeholder_text="Enter Your Email", width=255, text_color="black", fg_color="#EEEEEE", border_width=2, border_color="#601E88")
    email_input1.pack()

    pass_label1 = ctk.CTkLabel(frame1, text="Password", text_color="Black", font=("roboto", 13, "bold"), image=pass_icon, compound="left")
    pass_label1.pack(pady=(20, 0))
    pass_input1 = ctk.CTkEntry(frame1, placeholder_text="Enter Your Password", width=255, show="*", text_color="black", fg_color="#EEEEEE", border_width=2, border_color="#601E88")
    pass_input1.pack(pady=(0, 40))

    btn_login = ctk.CTkButton(frame1, text="Login", fg_color="#601E88", hover_color="#839ea8", command=login)
    btn_login.pack(pady=(0, 0))

    btn_register = ctk.CTkButton(frame1, text="Register", fg_color="Grey", hover_color="#839ea8", command=register_screen, corner_radius=4, height=50)
    btn_register.pack(pady=(20, 50))

def register_screen():
    global username_input, email_input2, pass_input2
    clear_window1()
    head_label1 = ctk.CTkLabel(frame1, text="Register", font=("Arial", 24, "bold"), text_color="#601E88")
    head_label1.pack(pady=(30, 0))

    username_label1 = ctk.CTkLabel(frame1, text="Username", text_color="Black", font=("roboto", 13, "bold"))
    username_label1.pack(pady=(25, 0))
    username_input = ctk.CTkEntry(frame1, placeholder_text="Enter your Username", width=255, text_color="black", fg_color="#EEEEEE", border_width=2, border_color="#601E88")
    username_input.pack()

    email_label2 = ctk.CTkLabel(frame1, text="E-mail", text_color="Black", font=("roboto", 13, "bold"), image=email_icon, compound="left")
    email_label2.pack(pady=(20, 0))
    email_input2 = ctk.CTkEntry(frame1, placeholder_text="Enter Your Email", width=255, text_color="black", fg_color="#EEEEEE", border_width=2, border_color="#601E88")
    email_input2.pack()

    pass_label2 = ctk.CTkLabel(frame1, text="Password", text_color="Black", font=("roboto", 13, "bold"), image=pass_icon, compound="left")
    pass_label2.pack(pady=(20, 0))
    pass_input2 = ctk.CTkEntry(frame1, placeholder_text="Enter Your Password", width=255, text_color="black", fg_color="#EEEEEE", border_width=2, border_color="#601E88")
    pass_input2.pack(pady=(0, 20))

    btn_reg1 = ctk.CTkButton(frame1, text="Register", command=register, fg_color="#601E88", hover_color="#839ea8", corner_radius=4)
    btn_reg1.pack()

    btn_back1 = ctk.CTkButton(frame1, text="BACK", command=login_screen, fg_color="#f52a4f", hover_color="#839ea8")
    btn_back1.pack(pady=(10, 20))

def register():
    email2 = email_input2.get()
    pass2 = pass_input2.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="airplane_reservation1"
    )
    crsr = conn.cursor()

    try:
        crsr.execute("INSERT INTO passengers (email, password) VALUES (%s, %s)", (email2, pass2))
        conn.commit()
        messagebox.showinfo("Registration", "Registration Successful !!")
        login_screen()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error occurred: {e}")

    conn.close()

def login():
    email1 = email_input1.get()
    pass1 = pass_input1.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="airplane_reservation1"
    )
    crsr = conn.cursor()

    crsr.execute("SELECT * FROM passengers WHERE email=%s AND password=%s", (email1, pass1))
    check_info = crsr.fetchone()

    if check_info:
        messagebox.showinfo("Login", "Login Successful")
        main_menu_screen()
    else:
        messagebox.showerror("LOGIN", "Invalid credentials or create an account first.")

    conn.close()

def clear_window1():
    # This clears the login/register frame
    for widget in frame1.winfo_children():
        widget.destroy()
    # Add this to hide the side image if needed
    label_sideimage.pack_forget() 

def clear_window2():
    # This clears everything in the main window
    for widget in main.winfo_children():
        widget.destroy()

def main_menu_screen():
    clear_window2()
    
    # Main container
    main_frame = ctk.CTkFrame(main, fg_color="#2b2b2b")
    main_frame.pack(fill="both", expand=True)
    
    # Left Column: Search & Flights
    left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    
    # Right Column: Booking Cart & Budget
    right_frame = ctk.CTkFrame(main_frame, fg_color="#1e1e1e", width=300)
    right_frame.pack(side="right", fill="y", padx=10, pady=20)
    
    # Add title for the cart
    ctk.CTkLabel(right_frame, text="Your Bookings", font=("Arial", 18, "bold"), text_color="white").pack(pady=10)
    
    # Booking Cart Textbox
    global booking_cart
    booking_cart = ctk.CTkTextbox(right_frame, width=280, height=300, fg_color="#333333", text_color="white")
    booking_cart.pack(pady=10)
    
    # Budget Display
    global budget_label
    budget_label = ctk.CTkLabel(right_frame, text="Total Budget Used: $0", font=("Arial", 14), text_color="white")
    budget_label.pack(pady=20)

    def create_database():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="airplane_reservation1"
        )
        crsr = conn.cursor()

        crsr.execute('''CREATE TABLE IF NOT EXISTS flights (
                            flight_id INT AUTO_INCREMENT PRIMARY KEY,
                            destination VARCHAR(255),
                            from_place VARCHAR(255),
                            flight_number VARCHAR(255),
                            departure_time VARCHAR(255),
                            price FLOAT)''')

        crsr.execute('''CREATE TABLE IF NOT EXISTS bookings (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            flight_id INT,
                            name VARCHAR(255),
                            email VARCHAR(255),
                            phone VARCHAR(255),
                            FOREIGN KEY (flight_id) REFERENCES flights (flight_id))''')

        conn.commit()
        conn.close()

    create_database()

    def search_flights():
        destination = destination_entry.get()
        from_place = from_place_entry.get()
        if not destination or not from_place:
            messagebox.showerror("Input Error", "Please enter both destination and departure location.")
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="airplane_reservation1"
        )
        crsr = conn.cursor()
        crsr.execute("SELECT * FROM flights WHERE destination = %s AND from_place = %s", (destination, from_place))
        rows = crsr.fetchall()
        conn.close()

        for row in f_table.get_children():
            f_table.delete(row)

        for row in rows:
            f_table.insert("", "end", values=row)

    def book_flight():
        global current_total
        selected_item = f_table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a flight first!")
            return
            
        # Get values: ID is 0, Dest is 1, From is 2, FlightNum is 3, Time is 4, Price is 5
        item_values = f_table.item(selected_item)['values']
        price = float(item_values[5])
        flight_number = item_values[3]
        
        # 1. Update the Booking Cart (Textbox)
        booking_cart.insert("end", f"{flight_number} | ${price}\n")
        
        # 2. Update the Budget
        current_total += price
        budget_label.configure(text=f"Total Budget Used: ${current_total}")
        
        # 3. Check for Budget Limit
        if current_total > 15000:
            messagebox.showwarning("Limit Exceeded", "Budget limit of $15,000 exceeded!")
        
        messagebox.showinfo("Success", "Flight booked successfully!")

    # Update these lines in your main_menu_screen() function:
    from_place_entry = ctk.CTkEntry(left_frame, placeholder_text="From", text_color="white", fg_color="#333333")
    from_place_entry.grid(row=0, column=1, padx=10, pady=10)

    destination_entry = ctk.CTkEntry(left_frame, placeholder_text="Destination", text_color="white", fg_color="#333333")
    destination_entry.grid(row=1, column=1, padx=10, pady=10)

    search_button = ctk.CTkButton(left_frame, text="Search Flights", command=search_flights)
    search_button.grid(row=1, column=2, padx=10, pady=10)

    f_table = ttk.Treeview(left_frame, columns=("ID", "Destination", "From", "Flight Number", "Departure Time", "Price"))
    f_table.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    name_entry = ctk.CTkEntry(left_frame, placeholder_text="Name", text_color="white", fg_color="#333333")
    name_entry.grid(row=3, column=1, padx=10, pady=10)

    email_entry = ctk.CTkEntry(left_frame, placeholder_text="Email", text_color="white", fg_color="#333333")
    email_entry.grid(row=4, column=1, padx=10, pady=10)

    phone_entry = ctk.CTkEntry(left_frame, placeholder_text="Phone", text_color="white", fg_color="#333333")
    phone_entry.grid(row=5, column=1, padx=10, pady=10)

    book_button = ctk.CTkButton(left_frame, text="Book Flight", command=book_flight)
    book_button.grid(row=6, column=1, pady=10)

db_setup()
login_screen()
main.after(0, lambda: main.state("zoomed"))
main.mainloop()
