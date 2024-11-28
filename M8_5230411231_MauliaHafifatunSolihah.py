import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import threading
import winsound

class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Frame utama
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Judul
        self.title_label = tk.Label(self.main_frame, text="Timer Sederhana", font=("Times New Roman", 20, 'bold'), bg='#f0f0f0')
        self.title_label.pack(pady=20)

        # Frame untuk tombol
        self.button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.button_frame.pack(pady=10)
        
        # Tombol tambah timer
        self.add_timer_btn = tk.Button(self.button_frame, text=" Tambah Timer", command=self.add_new_timer, bg='#E7CCCC', fg='black')
        self.add_timer_btn.pack(side=tk.LEFT, padx=10)

        # Tombol reset semua timer
        self.reset_all_btn = tk.Button(self.button_frame, text="Reset Semua", command=self.reset_all_timers, bg='#F5EEE6', fg='black')
        self.reset_all_btn.pack(side=tk.LEFT, padx=10)

        # Tombol hapus semua timer
        self.clear_btn = tk.Button(self.button_frame, text="Hapus Semua", command=self.clear_semua, bg='#F0C1E1', fg='black')
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        # Scrollable frame untuk timer
        self.canvas = tk.Canvas(self.main_frame, bg='#F9F9F9')
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#F9F9F9')
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # List untuk menyimpan timer aktif
        self.timers = []

    def add_new_timer(self):
        # Memilih durasi timer
        duration = simpledialog.askinteger("Tambah Timer", "Masukkan durasi timer (dalam detik):", minvalue=1, maxvalue=3600)
        
        if duration:
            timer_frame = tk.Frame(self.scrollable_frame, bg='#ffffff', bd=1, relief=tk.RAISED)
            timer_frame.pack(fill=tk.X, pady=5, padx=5)

            # Membuat label durasi timer
            duration_label = tk.Label(timer_frame, text=self.format_time(duration), font=("Times", 15), bg='#ffffff')
            duration_label.pack(side=tk.LEFT, pady=10)

            # Tombol kontrol
            control_frame = tk.Frame(timer_frame, bg='#ffffff')
            control_frame.pack(side=tk.RIGHT, pady=10)

            start_btn = tk.Button(control_frame, text="Start", command=lambda: self.start_timer(duration_label, duration, start_btn, pause_btn, reset_btn), bg='#E6A4B4', fg='black')
            start_btn.pack(side=tk.LEFT, padx=2)

            pause_btn = tk.Button(control_frame, text="Pause", command=lambda: self.pause_timer(duration_label, start_btn, pause_btn), bg='#FFCCD2',fg='black',state=tk.DISABLED)
            pause_btn.pack(side=tk.LEFT, padx=2 )

            reset_btn = tk.Button(control_frame, text="Reset", command=lambda: self.reset_timer(duration_label, duration, start_btn, pause_btn, reset_btn),bg='#EBD8C3',fg='black')
            reset_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = tk.Button(control_frame, text="Clear", command=lambda: self.delete_timer(timer_frame, duration_label), bg='#C1A3A3', fg='black')
            delete_btn.pack(side=tk.LEFT, padx=2)

            # Simpan timer
            timer_info = {
                'frame': timer_frame,
                'label': duration_label,
                'start_btn': start_btn,
                'pause_btn': pause_btn,
                'reset_btn': reset_btn,
                'duration': duration,
                'remaining': duration,
                'running': False,
                'paused': False
            }
            self.timers.append(timer_info)

    def format_time(self, seconds):
        # Konversi detik ke format menit:detik
        minutes, secs = divmod(seconds, 60)
        return f"{minutes:02d}:{secs:02d}"

    def start_timer(self, label, duration, start_btn, pause_btn, reset_btn):
        timer_info = next(t for t in self.timers if t['label'] == label)
        
        if not timer_info['running']:
            timer_info['running'] = True
            timer_info['paused'] = False
            start_btn.config(state=tk.DISABLED)
            pause_btn.config(state=tk.NORMAL)
            reset_btn.config(state=tk.DISABLED)

            def countdown():
                while timer_info['remaining'] > 0 and timer_info['running']:
                    if not timer_info['paused']:
                        timer_info['remaining'] -= 1
                        label.config(text=self.format_time(timer_info['remaining']))
                        
                        if timer_info['remaining'] == 0:
                            # Notifikasi saat timer selesai
                            winsound.Beep(1000, 500)
                            messagebox.showinfo("Timer Selesai", "Waktu anda habis!")
                            
                            # Reset tombol
                            start_btn.config(state=tk.NORMAL)
                            pause_btn.config(state=tk.DISABLED)
                            reset_btn.config(state=tk.NORMAL)
                            timer_info['running'] = False
                            break
                    
                    time.sleep(1)

            threading.Thread(target=countdown, daemon=True).start()

    def pause_timer(self, label, start_btn, pause_btn):
        timer_info = next(t for t in self.timers if t['label'] == label)
        
        if timer_info['running']:
            if not timer_info['paused']:
                timer_info['paused'] = True
                pause_btn.config(text="continue", bg='#F8EDFF')
                start_btn.config(state=tk.NORMAL)
            else:
                timer_info['paused'] = False
                pause_btn.config(text="Pause", bg='#F3D7CA')
                start_btn.config(state=tk.DISABLED)

    def reset_timer(self, label, duration, start_btn, pause_btn, reset_btn):
        timer_info = next(t for t in self.timers if t['label'] == label)
        
        timer_info['running'] = False
        timer_info['paused'] = False
        timer_info['remaining'] = duration
        
        label.config(text=self.format_time(duration))
        start_btn.config(state=tk.NORMAL)
        pause_btn.config(state=tk.DISABLED)
        reset_btn.config(state=tk.NORMAL)

    def reset_all_timers(self):
        for timer in self.timers:
            self.reset_timer(
                timer['label'], 
                timer['duration'], 
                timer['start_btn'], 
                timer['pause_btn'], 
                timer['reset_btn']
            )

    def delete_timer(self, frame, label):
        timer_info = next((t for t in self.timers if t['label'] == label), None)
        
        if timer_info:
            timer_info['running'] = False
            frame.destroy()
            self.timers.remove(timer_info)

    def clear_semua(self):
        confirm = messagebox.askquestion("Konfirmasi", "Yakin ingin menghapus semua timer?")
    
        if confirm == "yes":
            for timer in self.timers:
                timer['frame'].destroy()
                self.timers.clear()

        messagebox.showinfo("Informasi", "Semua timer berhasil dihapus!")

if __name__ == "__main__":
    root = tk.Tk()
    App = Timer(root)
    root.mainloop()