# Para usar este programa, você precisa instalar as bibliotecas Pillow e imageio.
# Use os comandos: pip install Pillow imageio

from PIL import Image
import imageio
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import subprocess

def gif_to_frames(gif_path):
    frames = []
    with imageio.get_reader(gif_path) as reader:
        for frame in reader:
            frames.append(frame)
    return frames

def resize_frame(frame, size):
    image = Image.fromarray(frame)
    return image.resize(size, Image.ANTIALIAS)

def get_next_directory_name(base_name):
    i = 1
    while True:
        dir_name = f"{base_name}-{i}"
        if not os.path.exists(dir_name):
            return dir_name
        i += 1

def save_frames_as_stacked_png(frames, output_folder, resolution):
    os.makedirs(output_folder, exist_ok=True)
    total_height = len(frames) * resolution[1]
    stacked_image = Image.new("RGBA", (resolution[0], total_height), (0, 0, 0, 0))

    for i, frame in enumerate(frames):
        resized_frame = resize_frame(frame, resolution)
        stacked_image.paste(resized_frame, (0, i * resolution[1]))

    stacked_image.save(os.path.join(output_folder, 'obsidian.png'))

    mcmeta_content = '''{
    "animation": {}
}'''
    with open(os.path.join(output_folder, 'obsidian.png.mcmeta'), 'w') as mcmeta_file:
        mcmeta_file.write(mcmeta_content)

def convert_gif():
    gif_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if not gif_path:
        return

    selected_resolution = resolution_var.get()
    resolutions = {
        '16x16': (16, 16),
        '32x32': (32, 32),
        '64x64': (64, 64),
        '128x128': (128, 128),
        '256x256': (256, 256)
    }
    resolution = resolutions[selected_resolution]
    output_folder = get_next_directory_name('OBSIDIAN')

    try:
        frames = gif_to_frames(gif_path)
        save_frames_as_stacked_png(frames, output_folder, resolution)
        messagebox.showinfo("Sucesso", f'Frames salvos como obsidian.png e obsidian.png.mcmeta na pasta {output_folder}!')
    except Exception as e:
        messagebox.showerror("Erro", f'Ocorreu um erro: {e}')

def open_twitch():
    webbrowser.open("https://www.twitch.tv/gustvst")

def open_youtube():
    webbrowser.open("https://www.youtube.com/@Gustvst")

def open_discord():
    try:
        subprocess.run(["C:\\Users\\<SeuNomeDeUsuario>\\AppData\\Local\\Discord\\app-1.0.9005\\Discord.exe"])  # Atualize o caminho conforme necessário
    except Exception:
        webbrowser.open("https://discord.gg/SuTKhjyu2F")

root = tk.Tk()
root.title("Transformador de GIFs em Blocos Animados")
root.geometry("600x700")
root.configure(bg="#2C2C2C")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", background="#2C2C2C", foreground="#FFFFFF", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=5)

title_label = tk.Label(root, text="Transformador de GIFs em Blocos Animados", bg="#2C2C2C", fg="#4CAF50", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

info_label = tk.Label(root, text="Desenvolvido por Gustavo (gustvst)", wraplength=300, bg="#2C2C2C", fg="#AAAAAA", font=("Arial", 12))
info_label.pack(pady=5)

resolution_label = tk.Label(root, text="Escolha a resolução:", bg="#2C2C2C", fg="#FFFFFF", font=("Arial", 14))
resolution_label.pack(pady=15)

resolution_var = tk.StringVar(value='64x64')
resolution_options = ['16x16', '32x32', '64x64', '128x128', '256x256']
resolution_combobox = ttk.Combobox(root, textvariable=resolution_var, values=resolution_options, state='readonly', width=10)
resolution_combobox.pack(pady=10)

convert_button = tk.Button(root, text="Converter GIF", command=convert_gif, bg="#4CAF50", fg="#FFFFFF", width=20)
convert_button.pack(pady=30)

links_frame = tk.Frame(root, bg="#2C2C2C")
links_frame.pack(pady=20)

tk.Button(links_frame, text="Canal na Twitch", command=open_twitch, bg="#6441A4", fg="#FFFFFF", width=20).grid(row=0, column=0, padx=10, pady=5)
tk.Button(links_frame, text="Canal no YouTube", command=open_youtube, bg="#FF0000", fg="#FFFFFF", width=20).grid(row=0, column=1, padx=10, pady=5)
tk.Button(links_frame, text="Servidor no Discord", command=open_discord, bg="#7289DA", fg="#FFFFFF", width=20).grid(row=1, column=0, columnspan=2, pady=5)

root.mainloop()
