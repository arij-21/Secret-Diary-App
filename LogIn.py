import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import tkinter as tk 
from tkcalendar import Calendar
from tkinter import StringVar
import mysql.connector
import hashlib
import os
from tkinter import filedialog

entry_container = None
scrollable_frame = None 
search_entry = None 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="datte123bayo.ne",  
    database="secret_diary"
)

cursor = conn.cursor()

# Function to open Sign-In window
def open_login_window():
    global window
    window = ctk.CTk()
    window.title("Secret Diary Login")

    # Get screen size dynamically
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set full-screen size
    window.state("zoomed")
    window.minsize(800, 600)
    window.configure(bg="#f0e0e0")

    # Load and Resize Image to Fit Left Frame
    image_path = r"C:\Users\Arij\Documents\Secret Diary\IMG.jpg"
    image = Image.open(image_path)
    image = image.resize((screen_width // 2, screen_height))  
    image = ImageTk.PhotoImage(image)

    # Left Frame
    left_frame = ctk.CTkFrame(window, width=screen_width // 2, height=screen_height, corner_radius=0, fg_color="white")
    left_frame.place(x=0, y=0, relwidth=0.5, relheight=1)

    # Display the image fully stretched in the left frame
    image_label = ctk.CTkLabel(left_frame, image=image, text="")
    image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Right Frame (Login Form)
    right_frame = ctk.CTkFrame(window, corner_radius=0, fg_color="white")
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    # Login Frame (Centered)
    login_frame = ctk.CTkFrame(right_frame, width=400, height=500, fg_color="#fff", corner_radius=15)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Heading
    ctk.CTkLabel(login_frame, text="Welcome to Your Secret Diary!", font=("Arial", 22, 'bold'), text_color="#fea6be").pack(pady=20)
    ctk.CTkLabel(login_frame, text="Please login to access your diary", font=("Arial", 14), text_color="#606060").pack(pady=5)

    # Username Entry
    user = ctk.CTkEntry(login_frame, placeholder_text="Username", font=("Microsoft YaHei UI Light", 16), width=300, height=40, corner_radius=10)
    user.pack(pady=15)

    # Password Entry
    code = ctk.CTkEntry(login_frame, placeholder_text="Password", font=("Microsoft YaHei UI Light", 16), width=300, height=40, corner_radius=10, show='*')
    code.pack(pady=15)
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    # Login button
    def connecter():
        username = user.get()
        password = code.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                hashed_input = hash_password(password)
                stored_password = result[0]

                if hashed_input == stored_password:
                    messagebox.showinfo("Success", "Logged in successfully!")  
                    window.destroy()
                    open_diary_interface()
                    return

            messagebox.showerror("Error", "Invalid username or password.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    ctk.CTkButton(login_frame, text="Login", font=("Microsoft YaHei UI Light", 16, 'bold'), width=200, height=50, 
                  command=connecter, corner_radius=10, fg_color="#fea6be").pack(pady=25)

    ctk.CTkLabel(login_frame, text="You don't have an account?", font=("Arial", 14), text_color="#606060").pack(pady=(10, 0))

    ctk.CTkButton(login_frame, text="Sign Up", font=("Microsoft YaHei UI Light", 14, 'bold'), width=150, height=40, 
                  corner_radius=10, fg_color="transparent", text_color="#fea6be", hover_color="#ff8fa3", 
                  command=lambda: [window.destroy(), open_signup_window()]).pack(pady=5)

    window.mainloop()

# Function to open Sign-Up window
def open_signup_window():
    signup_window = ctk.CTk()
    signup_window.title("Sign Up")
    
    # Get screen size dynamically
    screen_widthh = signup_window.winfo_screenwidth()
    screen_heightt = signup_window.winfo_screenheight()
    
    # Set full-screen size
    signup_window.state("zoomed")
    signup_window.minsize(800, 600)
    signup_window.configure(bg="#f0e0e0")

    # Load and Resize Image to Fit Left Frame
    image_path = r"C:\Users\Arij\Documents\Secret Diary\SIGNUPIMG.jpg"
    image = Image.open(image_path)
    image = image.resize((screen_widthh // 2, screen_heightt))  
    image = ImageTk.PhotoImage(image)
    
    # Left Frame
    left_frame = ctk.CTkFrame(signup_window, width=screen_widthh // 2, height=screen_heightt, corner_radius=0, fg_color="white")
    left_frame.place(x=0, y=0, relwidth=0.5, relheight=1)

    # Display the image fully stretched in the left frame
    image_label = ctk.CTkLabel(left_frame, image=image, text="")
    image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Right Frame (Login Form)
    right_frame = ctk.CTkFrame(signup_window, corner_radius=0, fg_color="white")
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    # Sign-Up Frame
    signup_frame = ctk.CTkFrame(right_frame, width=400, height=500, fg_color="#fff", corner_radius=15)
    signup_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Heading
    ctk.CTkLabel(signup_frame, text="Create Your Account", font=("Arial", 22, 'bold'), text_color="#fea6be").pack(pady=20)

    # Username Entry
    signup_user = ctk.CTkEntry(signup_frame, placeholder_text="Username", font=("Microsoft YaHei UI Light", 16), width=300, height=40, corner_radius=10)
    signup_user.pack(pady=15)

    # Password Entry
    signup_password = ctk.CTkEntry(signup_frame, placeholder_text="Password", font=("Microsoft YaHei UI Light", 16), width=300, height=40, corner_radius=10, show='*')
    signup_password.pack(pady=15)

    # Confirm Password Entry
    confirm_password = ctk.CTkEntry(signup_frame, placeholder_text="Confirm Password", font=("Microsoft YaHei UI Light", 16), width=300, height=40, corner_radius=10, show='*')
    confirm_password.pack(pady=15)
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Function to handle account creation
    def create_account():
        username = signup_user.get()
        password = signup_password.get()
        confirm = confirm_password.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "Please fill in all fields cutie ^-^.")
            return

        if password != confirm:
            messagebox.showerror("Error", "Oops, Passwords do not match!")
            return

        # Connect to MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Looks like Username already exists.")
                return

            # Hash the password
            hashed = hash_password(password)


            # Insert into DB
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account created successfully!")
            signup_window.destroy()
            open_login_window()  

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    ctk.CTkButton(signup_frame, text="Create Account", font=("Microsoft YaHei UI Light", 16, 'bold'),
                  width=200, height=50, command=create_account, corner_radius=10,
                  fg_color="#fea6be").pack(pady=25)

    signup_window.mainloop()
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

def open_diary_interface():
    # Create the main window
    window = ctk.CTk()
    window.title("Secret Diary")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.configure(bg="#ffffff")

    accent_color = "#f06292"  # pink

    # Load and slightly fade background image
    from customtkinter import CTkImage

    img_path = r"C:\Users\Arij\Documents\Secret Diary\583.jpg"
    img = Image.open(img_path).resize((screen_width, screen_height))
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 50))  
    img = Image.alpha_composite(img, overlay)
    bg_img = CTkImage(light_image=img, size=(screen_width, screen_height))

    bg_label = ctk.CTkLabel(window, image=bg_img, text="")
    bg_label.place(relx=0.5, rely=0.5, anchor="center")
    bg_label.lower()

    # Floating transparent + button
    def open_new_entry_window():
        entry_window = ctk.CTkToplevel(window)
        entry_window.title("New Diary Entry")
        entry_window.geometry("600x500")
        entry_window.configure(fg_color="#ffe4ec")
        entry_window.grab_set()

        entry_label = ctk.CTkLabel(
            entry_window,
            text="Write your heart out 💌",
            font=("Arial", 22, "bold"),
            text_color="#f06292"
        )
        entry_label.pack(pady=20)
        
        title_entry = ctk.CTkEntry(
        entry_window,
        placeholder_text="Give it a sweet little title 💖",
        width=500,
        height=35,
        font=("Arial", 16)
        )
        title_entry.pack(pady=(0, 10))

        diary_textbox = ctk.CTkTextbox(
            entry_window,
            width=500,
            height=300,
            corner_radius=12,
            font=("Arial", 16)
        )
        diary_textbox.pack(pady=10)

        def save_entry():
            title = title_entry.get().strip()
            content = diary_textbox.get("1.0", "end").strip()

            if not content:
                messagebox.showwarning("Empty Entry", "You didn't write anything, sweetheart 😔")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="datte123bayo.ne",
                    database="secret_diary"
                )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO entries (title, content) VALUES (%s, %s)", (title, content))
                conn.commit()
                conn.close()

                entry_window.destroy()
                display_all_entries()

            except Exception as e:
                messagebox.showerror("Error", f"Couldn't save, babe:\n{e}")


        save_btn = ctk.CTkButton(
            entry_window,
            text="Save Entry",
            command=save_entry,
            fg_color="#f06292",
            hover_color="#e91e63",
            width=120,
            height=40
        )
        save_btn.pack(pady=20)
    plus_button = ctk.CTkButton(
        window, text="+",
        fg_color="transparent",
        hover_color="#e91e63",
        text_color=accent_color,
        width=60, height=60,
        corner_radius=30,
        font=("Arial", 30, "bold"),
        command=open_new_entry_window
    )
    
    plus_button.place(relx=0.5, rely=0.9, anchor="center")
   

        
    def show_entry_banner(parent, date, content, entry_id, is_favorite):
        banner = tk.Frame(parent, bg="#ffe6f0", padx=10, pady=5)
        banner.pack(fill='x', pady=5)

        label_date = tk.Label(banner, text=str(date), fg="deeppink", bg="#ffe6f0", font=("Arial", 10, "bold"))
        label_date.pack(anchor='w')

        label_content = tk.Label(banner, text=content[:80] + ("..." if len(content) > 80 else ""), 
                             fg="black", bg="#ffe6f0", font=("Arial", 10))
        label_content.pack(anchor='w')
        
        # 💖 Heart toggle
        heart_icon = "❤️" if is_favorite else "🤍"
        heart_btn = tk.Button(banner, text=heart_icon, bg="#ffe6f0", bd=0, font=("Arial", 14))
        heart_btn.pack(anchor="e", padx=10)
        
        def toggle_favorite():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="datte123bayo.ne",
                    database="secret_diary"
                )
                cursor = conn.cursor()
                new_fav = not is_favorite
                cursor.execute("UPDATE entries SET is_favorite = %s WHERE id = %s", (new_fav, entry_id))
                conn.commit()
                conn.close()
                display_all_entries()
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't update favorite:\n{e}")

        heart_btn.config(command=toggle_favorite)
        
        def open_entry_editor(entry_id, date, content):
            editor_window = ctk.CTkToplevel()
            editor_window.geometry("600x500")
            editor_window.title("Edit Your Secret ✨")
            editor_window.configure(fg_color="#ffe4ec")
            editor_window.grab_set()

            entry_label = ctk.CTkLabel(
                editor_window,
                text="Update or say goodbye 💌",
                font=("Arial", 22, "bold"),
                text_color="#f06292"
            )
            entry_label.pack(pady=20)

            # You can fetch the title too if your DB has it
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM entries WHERE id = %s", (entry_id,))
            result = cursor.fetchone()
            conn.close()
            current_title = result[0] if result else ""

            title_entry = ctk.CTkEntry(
                editor_window,
                placeholder_text="Edit the title 💖",
                width=500,
                height=35,
                font=("Arial", 16)
            )
            title_entry.insert(0, current_title)
            title_entry.pack(pady=(0, 10))

            text_area = ctk.CTkTextbox(
                editor_window,
                width=500,
                height=300,
                corner_radius=12,
                font=("Arial", 16)
            )
            text_area.pack(pady=10)
            text_area.insert("1.0", content)

            def update_entry():
                new_title = title_entry.get().strip()
                new_content = text_area.get("1.0", "end-1c").strip()

                if new_content:
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="datte123bayo.ne",
                            database="secret_diary"
                        )
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE entries SET title=%s, content=%s WHERE id=%s",
                            (new_title, new_content, entry_id)
                        )
                        conn.commit()
                        conn.close()

                        messagebox.showinfo("Updated", "Entry updated successfully 💕")
                        editor_window.destroy()
                        display_all_entries()
                    except Exception as e:
                        messagebox.showerror("Error", f"Update failed: {e}")

            def delete_entry():
                confirm = messagebox.askyesno("Delete?", "Are you sure you want to delete this entry, baby?")
                if confirm:
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="datte123bayo.ne",
                            database="secret_diary"
                        )
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM entries WHERE id=%s", (entry_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Deleted", "Entry deleted 💔")
                        editor_window.destroy()
                        display_all_entries()
                    except Exception as e:
                        messagebox.showerror("Error", f"Delete failed: {e}")

            # Buttons
            btn_frame = ctk.CTkFrame(editor_window, fg_color="transparent")
            btn_frame.pack(pady=20)

            update_btn = ctk.CTkButton(
                btn_frame,
                text="💾 Update",
                command=update_entry,
                fg_color="#f06292",
                hover_color="#e91e63",
                width=120,
                height=40
            )
            update_btn.pack(side="left", padx=10)

            delete_btn = ctk.CTkButton(
                btn_frame,
                text="🗑 Delete",
                command=delete_entry,
                fg_color="#d32f2f",
                hover_color="#b71c1c",
                width=120,
                height=40
            )
            delete_btn.pack(side="left", padx=10)

        # Make the banner clickable 💅
        banner.bind("<Button-1>", lambda e: open_entry_editor(entry_id, date, content))
        label_date.bind("<Button-1>", lambda e: open_entry_editor(entry_id, date, content))
        label_content.bind("<Button-1>", lambda e: open_entry_editor(entry_id, date, content))



    
    def display_all_entries():
        for widget in entry_container.winfo_children():
            widget.destroy()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()

            # 💖 Fetch the ID too!
            cursor.execute("SELECT id, created_at, content, is_favorite FROM entries ORDER BY created_at DESC")
            entries = cursor.fetchall()
            conn.close()

            for entry_id, date, content, is_favorite in entries:
            # 💕 Pass the ID to make it clickable
                show_entry_banner(entry_container, date, content, entry_id, is_favorite)

        except Exception as e:
            messagebox.showerror("Error", f"Couldn't load entries, my love:\n{e}")


    
    def open_calendar():
        cal_window = ctk.CTkToplevel(window)
        cal_window.title("Pick a date, darling 🌸")
        cal_window.geometry("400x400")
        cal_window.configure(fg_color="#ffe4ec")

        # Make it stay on top
        cal_window.attributes("-topmost", True)

        # Disable interaction with the main window until this one is closed
        cal_window.grab_set()

        cal = Calendar(
            cal_window,
            selectmode='day',
            year=2025,
            month=4,
            day=6,
            background='pink',
            disabledbackground='white',
            bordercolor='lightgray',
            headersbackground='#f8b5d0',
            normalbackground='#fff0f5',
            weekendbackground='#ffe4ec',
            foreground='black',
            headersforeground='black'
        )
        cal.pack(pady=50)

        def date_selected():
            selected_date = cal.get_date()  # Format: MM/DD/YYYY
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="datte123bayo.ne",
                    database="secret_diary"
                )
                cursor = conn.cursor()

                # Convert to the format your DB uses, e.g., YYYY-MM-DD
                from datetime import datetime
                selected_date_db = datetime.strptime(selected_date, "%m/%d/%y").date()

                cursor.execute("SELECT id, created_at, content, is_favorite FROM entries WHERE DATE(created_at) = %s ORDER BY created_at DESC", (selected_date_db,))
                entries = cursor.fetchall()
                conn.close()

                # Clear current entries
                for widget in entry_container.winfo_children():
                    widget.destroy()

                if entries:
                    for entry_id, date, content, is_favorite in entries:
                        show_entry_banner(entry_container, date, content, entry_id, is_favorite)
                else:
                    messagebox.showinfo("No Entries", f"No entries for {selected_date_db}, sweetie 🌸")

                cal_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Couldn't fetch entries for selected date:\n{e}")
                cal_window.destroy()


        ctk.CTkButton(
            cal_window,
            text="Select",
            command=date_selected,
            fg_color="#f06292",
            hover_color="#e91e63"
        ).pack()

    
    # Calendar button 
    calendar_button = ctk.CTkButton(
    window, text="📅",  
    width=40, height=60,
    fg_color="#f8b5d0",
    hover_color="#f48fb1",
    text_color="white",
    font=("Arial", 28),
    corner_radius=30,
    command= open_calendar
    )
    calendar_button.place(relx=0.65, rely=0.9, anchor="center")
    
    def show_random_quote():
        import random
        quotes = [
            "🌞 Keep your face always toward the sunshine — and shadows will fall behind you - Walt Whitman 🌻",
            "🚀 Believe you can and you're halfway there - Theodore Roosevelt 🌟",
            "🛠️ Start where you are. Use what you have. Do what you can - Arthur Ashe 🔧",
            "🧠💡 The best way to predict the future is to create it - Peter Drucker 🔮",
            "🌱 Grow through what you go through - Anonymous 🌼"
        ]
        messagebox.showinfo("💬 Your Daily Whisper", random.choice(quotes))

    # Quote button to the LEFT of the plus button
    quote_button = ctk.CTkButton(
     window, text="💬",
     width=40, height=60,
     fg_color="#f8b5d0",
     hover_color="#f48fb1",
     text_color="white",
     font=("Arial", 28),
     corner_radius=30,
     command=show_random_quote
    )
    quote_button.place(relx=0.35, rely=0.9, anchor="center")

    
    
    # Search field hidden by default
    search_visible = [False]
    search_var = StringVar()

    search_entry = ctk.CTkEntry(
        window,
        textvariable=search_var,
        placeholder_text="Type to search...",
        width=280,
        height=35,
        corner_radius=12
    )
    search_label = ctk.CTkLabel(
        window,
        text="Search your entries 💭",
        text_color="#f06292",
        font=("Arial", 18)
    )

    def toggle_search():
        global search_entry, search_button_confirm

        if not hasattr(toggle_search, "visible") or not toggle_search.visible:
            search_entry = ctk.CTkEntry(window, width=200, placeholder_text="Type to search...")
            search_entry.place(relx=0.65, rely=0.02, anchor="ne")

            search_button_confirm = ctk.CTkButton(
                window,
                text="Go",
                width=40,
                height=28,
                fg_color="#f06292",
                text_color="white",
                hover_color="#ffe4ec",
                font=("Arial", 14),
                command=search_entries
            )
            search_button_confirm.place(relx=0.82, rely=0.02, anchor="ne")
            toggle_search.visible = True
        else:
            search_entry.destroy()
            search_button_confirm.destroy()
            toggle_search.visible = False
            
    
    def search_entries():
        global search_entry
        if "search_entry" not in globals():
            messagebox.showinfo("Search", "You need to open the search bar first, sweetheart 💋")
            return

        keyword = search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("Search", "You gotta type something first, sweetheart 😘")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()
            query = "SELECT created_at, content FROM entries WHERE content LIKE %s"
            values = (f"%{keyword}%",)
            cursor.execute(query, values)
            results = cursor.fetchall()
            conn.close()

            if results:
                result_text = "\n\n".join([f"{date}\n{content}" for date, content in results])
                messagebox.showinfo("Results", f"Found this for you, cutie pie:\n\n{result_text}")
            else:
                messagebox.showinfo("Results", "Nothin’ found, little bird 😢")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed, babe:\n{e}")
    # Search icon button
    search_button = ctk.CTkButton(
        window,
        text="🔍",
        width=35,
        height=35,
        font=("Arial", 18),
        fg_color="transparent",
        text_color="#f06292",
        hover_color="#ffe4ec",
        command=toggle_search
    )
    search_button.place(relx=0.95, rely=0.015, anchor="ne")
    
    



    # Menu frame setup (hidden by default)
    menu_frame = ctk.CTkFrame(window, width=180, fg_color="#e0c5d9", corner_radius=10, height=screen_height)
    menu_visible = [False]

    def export_entries():
        try:
        # Connect to the DB
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT title, content, created_at FROM entries")
            entries = cursor.fetchall()
            conn.close()

            if not entries:
                messagebox.showinfo("Export", "No entries to export.")
                return

            # Ask user where to save the file
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                title="Save Backup As"
            )
            if not file_path:
                return

            with open(file_path, "w", encoding="utf-8") as f:
                for title, content, created_at in entries:
                    f.write(f"Title: {title}\nDate: {created_at}\nContent:\n{content}\n")
                    f.write("-" * 40 + "\n\n")

            messagebox.showinfo("Export", "Entries exported successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    def display_favorite_entries():
        for widget in entry_container.winfo_children():
            widget.destroy()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="datte123bayo.ne",
                database="secret_diary"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, created_at, content, is_favorite FROM entries WHERE is_favorite = TRUE ORDER BY created_at DESC")
            entries = cursor.fetchall()
            conn.close()

            for entry_id, date, content, is_favorite in entries:
                show_entry_banner(entry_container, date, content, entry_id, is_favorite)

        except Exception as e:
            messagebox.showerror("Error", f"Couldn't load favorites:\n{e}")


    # Menu items
    menu_items = {
        "Home": lambda: [display_all_entries(), toggle_menu()],
        "Favorites": display_favorite_entries,
        "Export/Backup": export_entries,
        "Logout / Exit": lambda: [window.destroy(), open_login_window()]

    }
    
    

    for txt, cmd in menu_items.items():
        ctk.CTkButton(
            menu_frame, text=txt,
            command=cmd,
            fg_color="#2a2a2a",
            text_color="white",
            hover_color="#444",
            corner_radius=8,
            font=("Arial", 14)
        ).pack(pady=6, padx=10, fill="x")

    # Toggle menu visibility
    def toggle_menu():
        if menu_visible[0]:
            menu_frame.place_forget()
            menu_visible[0] = False
        else:
            menu_frame.place(x=10, y=50)  
            menu_visible[0] = True

    # ☰ Menu button
    menu_button = ctk.CTkButton(
        window, text="☰",
        fg_color=accent_color,
        hover_color="#e91e63",
        text_color="white",
        width=50, height=35,
        corner_radius=8,
        command=toggle_menu
    )
    menu_button.place(x=10, y=10)

    
    
    entry_container = ctk.CTkScrollableFrame(window, width=800, height=500, fg_color="transparent")
    entry_container.place(relx=0.5, rely=0.5, anchor="center")
    
    display_all_entries()

    window.mainloop() 

# Start with Login Window
open_login_window()

