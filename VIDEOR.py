import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
from moviepy.editor import VideoFileClip
import pygame

class VideoRockola:
    def __init__(self, root):
        self.root = root
        self.root.title("🎶 Video Rockola 🎶")
        self.root.geometry("500x400")
        self.playlist = []

        # Interfaz gráfica
        self.listbox = Listbox(root, width=60, height=15)
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Agregar Video", command=self.add_video).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="▶️ Reproducir", command=self.play_video).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="⏹️ Detener", command=self.stop_video).grid(row=0, column=2, padx=5)

        self.current_clip = None
        pygame.init()

    def add_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_path:
            self.playlist.append(file_path)
            self.listbox.insert(tk.END, os.path.basename(file_path))

    def play_video(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Selecciona un video", "Por favor selecciona un video de la lista.")
            return

        video_path = self.playlist[selected[0]]
        self.stop_video()

        # Preparar la ventana de reproducción
        clip = VideoFileClip(video_path)
        self.current_clip = clip
        clip.preview()  # Abre una ventana para reproducir el video

    def stop_video(self):
        if self.current_clip:
            self.current_clip.close()
            self.current_clip = None

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoRockola(root)
    root.mainloop()
