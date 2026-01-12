import tkinter as tk
from tkinter import messagebox
import datetime
import threading

# குரல் வசதி பிளக்-இன் (pyttsx3)
try:
    import pyttsx3
    voice_enabled = True
except ImportError:
    voice_enabled = False

# பாஸ்வேர்டு விவரங்கள்
ADMIN_KEY = "admintest@123"
MEMBER_KEY = "membertest@123"

class GangBoysApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GANG BOYS 🥷")
        self.root.geometry("500x750")
        self.root.configure(bg="#000000")
        
        # டேட்டா மேலாண்மை
        self.income = 0.0
        self.expense = 0.0
        self.news = "குழு உறுப்பினர்களுக்கு இனிய வணக்கம்!"
        
        self.login_screen()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # 1. லாகின் பக்கம்
    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="GANG BOYS 🥷", font=("Arial", 32, "bold"), fg="#FFD700", bg="#000000").pack(pady=50)
        
        self.input_data = {}
        fields = [("பெயர்", ""), ("தொலைபேசி", ""), ("பிறந்தநாள் (DD-MM)", ""), ("பாஸ்வேர்டு", "*")]
        
        for label, mask in fields:
            tk.Label(self.root, text=label, fg="white", bg="#000000", font=("Arial", 11)).pack()
            e = tk.Entry(self.root, width=30, show=mask, font=("Arial", 12), justify='center')
            e.pack(pady=5)
            self.input_data[label] = e

        tk.Button(self.root, text="LOGIN", font=("Arial", 12, "bold"), bg="#FFD700", fg="black", 
                  width=15, command=self.handle_login).pack(pady=40)

    # 2. லாகின் சரிபார்ப்பு (38-வது வரி சிக்கல் சரி செய்யப்பட்டது)
    def handle_login(self):
        user_name = self.input_data["பெயர்"].get().strip()
        user_pwd = self.input_data["பாஸ்வேர்டு"].get().strip()
        user_dob = self.input_data["பிறந்தநாள் (DD-MM)"].get().strip()
        
        if not user_name or not user_pwd:
            messagebox.showwarning("Warning", "பெயர் மற்றும் பாஸ்வேர்டு கட்டாயம்!")
            return

        today = datetime.datetime.now().strftime("%d-%m")

        if user_pwd == ADMIN_KEY or user_pwd == MEMBER_KEY:
            is_admin = (user_pwd == ADMIN_KEY)
            if user_dob == today:
                self.wish_user(user_name, is_admin)
            else:
                self.main_menu(user_name, is_admin)
        else:
            messagebox.showerror("Error", "தவறான பாஸ்வேர்டு!")

    # 3. பிறந்தநாள் வாழ்த்து (குரல் + அனிமேஷன்)
    def wish_user(self, name, admin_status):
        self.clear()
        tk.Label(self.root, text="🎉✨🎊", font=("Arial", 40), bg="#000000").pack(pady=20)
        tk.Label(self.root, text=f"இனிய பிறந்தநாள் வாழ்த்துக்கள்\n{name}!", 
                 font=("Helvetica", 22, "bold"), fg="#FFD700", bg="#000000").pack(pady=40)

        def voice_wish():
            if voice_enabled:
                try:
                    eng = pyttsx3.init()
                    eng.say(f"Happy Birthday {name}")
                    eng.runAndWait()
                except: pass

        threading.Thread(target=voice_wish).start()
        self.root.after(5000, lambda: self.main_menu(name, admin_status))

    # 4. மெயின் மெனு (லோகோவுடன்)
    def main_menu(self, name, is_admin):
        self.clear()
        # லோகோ மார்க்கர் (Right Top Corner)
        tk.Label(self.root, text="🥷 GB", fg="#FFD700", bg="#000000", font=("bold", 14)).place(x=440, y=10)
        
        header = tk.Frame(self.root, bg="#FFD700", pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"வணக்கம் {name}! 🥷", bg="#FFD700", fg="black", font=("Arial", 12, "bold")).pack()

        tk.Label(self.root, text=f"📢 {self.news}", fg="white", bg="#333", font=("Arial", 10), wraplength=480).pack(fill="x", pady=5)

        btn_area = tk.Frame(self.root, bg="#000000")
        btn_area.pack(pady=30)

        nav = [
            ("👗 ஆடை அளவுகள்", lambda: self.show_sizes(name, is_admin)),
            ("💰 வரவு செலவு", lambda: self.show_finance(name, is_admin)),
            ("📦 புகார் பெட்டி", lambda: self.show_complaints(name, is_admin))
        ]

        for txt, act in nav:
            tk.Button(btn_area, text=txt, width=28, pady=10, bg="#222", fg="white", font=("Arial", 11), command=act).pack(pady=8)

        if is_admin:
            tk.Button(btn_area, text="🛡️ தலைவர் அறை", width=28, pady=10, bg="#8B0000", fg="white", 
                      font=("Arial", 11, "bold"), command=lambda: self.admin_panel(name)).pack(pady=15)

    # 5. ஆடை அளவுகள் சேமிப்பு
    def show_sizes(self, name, admin):
        self.clear()
        tk.Label(self.root, text="ஆடை அளவுகள்", font=("bold", 18), bg="#FFD700", fg="black").pack(fill="x", pady=10)
        
        for part in ["சட்டை அளவு", "மார்பளவு", "கை நீளம்"]:
            tk.Label(self.root, text=part, fg="white", bg="#000000").pack(pady=5)
            tk.Entry(self.root, width=20, font=("Arial", 12)).pack()
            
        tk.Button(self.root, text="பதிவு செய்", bg="green", fg="white", font=("bold", 10),
                  command=lambda: messagebox.showinfo("Success", "அளவுகள் சேமிக்கப்பட்டன!")).pack(pady=30)
        tk.Button(self.root, text="Back", command=lambda: self.main_menu(name, admin)).pack()

    # 6. வரவு செலவு - நேரத்துடன் (Auto calculation)
    def show_finance(self, name, admin):
        self.clear()
        tk.Label(self.root, text="வரவு செலவு", font=("bold", 18), bg="#FFD700", fg="black").pack(fill="x", pady=10)
        
        bal = self.income - self.expense
        tk.Label(self.root, text=f"கையிருப்பு: ₹{bal}", font=("Arial", 28, "bold"), fg="#00FF00", bg="#000000").pack(pady=30)
        
        val_ent = tk.Entry(self.root, font=("Arial", 14), justify='center')
        val_ent.pack(pady=10)

        def update(plus):
            try:
                amt = float(val_ent.get())
                tm = datetime.datetime.now().strftime("%I:%M %p")
                if plus: self.income += amt
                else: self.expense += amt
                messagebox.showinfo("Done", f"நேரம்: {tm}\nகணக்கு புதுப்பிக்கப்பட்டது!")
                self.show_finance(name, admin)
            except:
                messagebox.showerror("Error", "எண்களை மட்டும் உள்ளிடவும்!")

        tk.Button(self.root, text="வரவு (+)", bg="blue", fg="white", width=12, command=lambda: update(True)).pack(pady=5)
        tk.Button(self.root, text="செலவு (-)", bg="red", fg="white", width=12, command=lambda: update(False)).pack(pady=5)
        tk.Button(self.root, text="Back", command=lambda: self.main_menu(name, admin)).pack(pady=20)

    # 7. அட்மின் கண்ட்ரோல்
    def admin_panel(self, name):
        self.clear()
        tk.Label(self.root, text="தலைவர் அறை", font=("bold", 18), bg="#8B0000", fg="white").pack(fill="x", pady=10)
        tk.Label(self.root, text="புதிய அறிவிப்பை இங்கே எழுதுக:", fg="white", bg="#000000").pack(pady=20)
        msg = tk.Entry(self.root, width=40, font=("Arial", 12))
        msg.pack(pady=10)
        
        def publish():
            self.news = msg.get()
            messagebox.showinfo("Admin", "அறிவிப்பு வெளியிடப்பட்டது!")

        tk.Button(self.root, text="Update Status", bg="white", fg="black", command=publish).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.main_menu(name, True)).pack()

    def show_complaints(self, name, admin):
        self.clear()
        tk.Label(self.root, text="புகார் பெட்டி", font=("bold", 18), bg="white", fg="black").pack(fill="x", pady=10)
        tk.Text(self.root, height=8, width=45).pack(pady=20)
        tk.Button(self.root, text="அனுப்பு", bg="#333", fg="white", command=lambda: messagebox.showinfo("Sent", "தலைவருக்கு அனுப்பப்பட்டது")).pack()
        tk.Button(self.root, text="Back", command=lambda: self.main_menu(name, admin)).pack(pady=20)

if __name__ == "__main__":
    app_root = tk.Tk()
    GangBoysApp(app_root)
    app_root.mainloop()
