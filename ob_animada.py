import subprocess
import sys
from PIL import Image
import imageio
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# Função para instalar pacotes
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Função para instalar pacotes necessários
def install_packages():
    required_packages = ["Pillow", "imageio", "moviepy"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            install(package)

# Funções principais do programa
def gif_to_frames(gif_path):
    frames = []
    with imageio.get_reader(gif_path) as reader:
        for frame in reader:
            frames.append(frame)
    return frames

def video_to_gif(video_path):
    from moviepy.editor import VideoFileClip
    gif_path = video_path.rsplit('.', 1)[0] + '.gif'
    clip = VideoFileClip(video_path)
    clip.write_gif(gif_path)
    return gif_path

def resize_frame(frame, size):
    image = Image.fromarray(frame)
    return image.resize(size, Image.LANCZOS)

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

def convert_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov"), ("All files", "*.*")])
    if not video_path:
        return

    gif_path = video_to_gif(video_path)
    convert_gif_from_video(gif_path)

def convert_gif_from_video(gif_path):
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

# Criação da janela principal
def initialize_app():
    global root, resolution_var
    root = tk.Tk()
    root.title("GIF to Animated Block Converter")
    root.geometry("500x600")
    root.configure(bg="#1E1E1E")
    root.resizable(False, False)

    # Configuração de estilo
    style = ttk.Style()
    style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.theme_use('clam')

    # Cabeçalho
    header = tk.Frame(root, bg="#4A90E2", height=60)
    header.pack(fill="x")

    title_label = tk.Label(header, text="OBSIDIAN ANIMADA", bg="#4A90E2", fg="#FFFFFF", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Corpo principal
    main_frame = tk.Frame(root, bg="#1E1E1E")
    main_frame.pack(pady=20)

    # Descrição
    description = tk.Label(main_frame, text="Transforme GIFs em blocos animados para Minecraft", bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 10), wraplength=400)
    description.pack(pady=10)

    # Seletor de resolução
    resolution_label = tk.Label(main_frame, text="Escolha a resolução:", bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 12))
    resolution_label.pack(pady=5)

    resolution_var = tk.StringVar(value='64x64')
    resolution_combobox = ttk.Combobox(main_frame, textvariable=resolution_var, values=['16x16', '32x32', '64x64', '128x128', '256x256'], state='readonly', width=12)
    resolution_combobox.pack(pady=5)

    # Botão para converter GIF
    convert_gif_button = tk.Button(main_frame, text="Converter GIF", command=convert_gif, bg="#76c7c0", fg="#FFFFFF", font=("Arial", 12), width=20)
    convert_gif_button.pack(pady=10)

    # Botão para converter vídeo em GIF
    convert_video_button = tk.Button(main_frame, text="Converter Vídeo para GIF", command=convert_video, bg="#76c7c0", fg="#FFFFFF", font=("Arial", 12), width=20)
    convert_video_button.pack(pady=10)

    # Rodapé com redes sociais
    footer = tk.Frame(root, bg="#4A90E2", height=100)
    footer.pack(fill="x", side="bottom")

    footer_label = tk.Label(footer, text="Links:", bg="#4A90E2", fg="#FFFFFF", font=("Arial", 12))
    footer_label.pack(pady=5)

    # Links centralizados
    links_frame = tk.Frame(footer, bg="#4A90E2")
    links_frame.pack(pady=5)

    github_link = "https://github.com/GustvCodes"
    twitch_link = "https://www.twitch.tv/gustvst"
    discord_link = "https://discord.gg/SuTKhjyu2F"

    twitch_button = tk.Button(links_frame, text="Twitch", command=lambda: webbrowser.open(twitch_link), bg="#8A3FFC", fg="#FFFFFF", font=("Arial", 10), width=10)
    twitch_button.pack(side="left", padx=5)

    github_button = tk.Button(links_frame, text="GitHub", command=lambda: webbrowser.open(github_link), bg="#FF0000", fg="#FFFFFF", font=("Arial", 10), width=10)
    github_button.pack(side="left", padx=5)

    discord_button = tk.Button(links_frame, text="Discord", command=lambda: webbrowser.open(discord_link), bg="#3C87E0", fg="#FFFFFF", font=("Arial", 10), width=10)
    discord_button.pack(side="left", padx=5)

# Inicializa o aplicativo
install_packages()  # Instala pacotes necessários
initialize_app()     # Inicia a interface do usuário
root.mainloop()
