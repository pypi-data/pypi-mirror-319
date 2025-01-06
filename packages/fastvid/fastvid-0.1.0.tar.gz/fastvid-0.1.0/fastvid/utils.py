import customtkinter as ctk
from tkinter import filedialog
import subprocess
import os
from datetime import datetime


# 定义颜色常量
class Colors:
    GREEN = "\033[92m"  # 绿色
    YELLOW = "\033[93m"  # 黄色
    RED = "\033[91m"  # 红色
    RESET = "\033[0m"  # 重置颜色


# 获取当前时间戳
def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# 视频加速转换
def accelerate_video(input_path, output_path, speed_factor):
    try:
        command = [
            "ffmpeg",
            "-i",
            input_path,
            "-vf",
            f"setpts=PTS/{speed_factor}",
            "-af",
            (
                f"atempo={speed_factor}"
                if speed_factor <= 2.0
                else "atempo=2.0,atempo={}".format(speed_factor / 2.0)
            ),
            "-strict",
            "-2",
            output_path,
        ]
        subprocess.run(command, check=True)
        print(
            f"{Colors.GREEN}加速转换完成！输出文件已保存到 {output_path}{Colors.RESET}"
        )
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}加速转换失败：{e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}发生错误：{e}{Colors.RESET}")


# 视频转换为 GIF 动图（提高分辨率）
def convert_to_gif(input_path, output_path, fps=10, scale=1080):
    try:
        command = [
            "ffmpeg",
            "-i",
            input_path,
            "-vf",
            f"fps={fps},scale={scale}:-1:flags=lanczos",  # 使用 lanczos 缩放算法提高质量
            "-c:v",
            "gif",
            output_path,
        ]
        subprocess.run(command, check=True)
        print(
            f"{Colors.GREEN}GIF 转换完成！输出文件已保存到 {output_path}{Colors.RESET}"
        )
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}GIF 转换失败：{e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}发生错误：{e}{Colors.RESET}")


# 视频压缩
def compress_video(input_path, output_path, crf=28):
    try:
        command = [
            "ffmpeg",
            "-i",
            input_path,
            "-vcodec",
            "libx264",
            "-crf",
            str(crf),
            output_path,
        ]
        subprocess.run(command, check=True)
        print(
            f"{Colors.GREEN}视频压缩完成！输出文件已保存到 {output_path}{Colors.RESET}"
        )
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}视频压缩失败：{e}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}发生错误：{e}{Colors.RESET}")


# 获取文件夹中的视频文件
def get_video_files(folder_path):
    video_extensions = [".mp4", ".mkv", ".avi", ".mov"]
    video_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in video_extensions:
                video_files.append(os.path.join(root, file))
    return video_files


# GUI 界面
class VideoToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频处理工具")
        self.root.geometry("800x250")  # 调整窗口尺寸

        # 设置主题
        ctk.set_appearance_mode("System")  # 系统主题
        ctk.set_default_color_theme("blue")  # 蓝色主题

        # 设置窗口图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets/app_icon.ico")
            self.root.iconbitmap(icon_path)  # 设置窗口图标
        except Exception as e:
            print(f"{Colors.YELLOW}未能加载图标文件：{e}{Colors.RESET}")

        # 输入文件选择
        self.input_file_label = ctk.CTkLabel(root, text="选择视频文件或文件夹：")
        self.input_file_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.input_file_entry = ctk.CTkEntry(root, width=400)
        self.input_file_entry.grid(row=0, column=1, padx=10, pady=10)

        self.input_file_button = ctk.CTkButton(
            root, text="浏览", width=100, command=self.select_input
        )
        self.input_file_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # 加速转换
        self.speed_label = ctk.CTkLabel(root, text="加速倍数：")
        self.speed_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.speed_entry = ctk.CTkEntry(root, width=100)
        self.speed_entry.insert(0, "4.0")  # 默认加速倍数
        self.speed_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.accelerate_button = ctk.CTkButton(
            root, text="加速转换", width=100, command=self.start_accelerate
        )
        self.accelerate_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # 转换为 GIF
        self.gif_label = ctk.CTkLabel(root, text="GIF 分辨率（宽度）：")
        self.gif_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.gif_entry = ctk.CTkEntry(root, width=100)
        self.gif_entry.insert(0, "1080")  # 默认分辨率宽度
        self.gif_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.gif_button = ctk.CTkButton(
            root, text="转换为 GIF", width=100, command=self.start_gif_conversion
        )
        self.gif_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # 视频压缩
        self.compress_label = ctk.CTkLabel(
            root, text="压缩质量（CRF，0-51，越小质量越高）："
        )
        self.compress_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.compress_entry = ctk.CTkEntry(root, width=100)
        self.compress_entry.insert(0, "28")
        self.compress_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.compress_button = ctk.CTkButton(
            root, text="压缩视频", width=100, command=self.start_compression
        )
        self.compress_button.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        # 输出路径选择
        self.output_folder_label = ctk.CTkLabel(root, text="选择输出文件夹（可选）：")
        self.output_folder_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.output_folder_entry = ctk.CTkEntry(root, width=400)
        self.output_folder_entry.grid(row=4, column=1, padx=10, pady=10)

        self.output_folder_button = ctk.CTkButton(
            root, text="浏览", width=100, command=self.select_output_folder
        )
        self.output_folder_button.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    def select_input(self):
        path = filedialog.askopenfilename(
            title="选择视频文件或文件夹",
            filetypes=[("视频文件", "*.mp4 *.mkv *.avi *.mov")],
        )
        if not path:
            path = filedialog.askdirectory(title="选择视频文件夹")
        if path:
            # 去除路径末尾的 *（如果有）
            path = path.rstrip("*").strip()
            self.input_file_entry.delete(0, "end")
            self.input_file_entry.insert(0, path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="选择输出文件夹")
        if folder_path:
            self.output_folder_entry.delete(0, "end")
            self.output_folder_entry.insert(0, folder_path)

    def get_output_folder(self):
        # 如果用户未选择输出文件夹，则使用当前目录
        output_folder = self.output_folder_entry.get()
        if not output_folder:
            output_folder = os.getcwd()  # 当前工作目录
        return output_folder

    def start_accelerate(self):
        input_path = self.input_file_entry.get()
        output_folder = self.get_output_folder()
        speed_factor = float(self.speed_entry.get())

        if not input_path:
            print(f"{Colors.YELLOW}错误：请选择输入文件或文件夹！{Colors.RESET}")
            return

        if os.path.isfile(input_path):
            # 单个文件处理
            output_path = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(input_path))[0]}_{get_timestamp()}_x{speed_factor}_accelerate.mp4",
            )
            accelerate_video(input_path, output_path, speed_factor)
        else:
            # 文件夹批量处理
            video_files = get_video_files(input_path)
            for video_file in video_files:
                output_path = os.path.join(
                    output_folder,
                    f"{os.path.splitext(os.path.basename(video_file))[0]}_{get_timestamp()}_x{speed_factor}_accelerate.mp4",
                )
                accelerate_video(video_file, output_path, speed_factor)

    def start_gif_conversion(self):
        input_path = self.input_file_entry.get()
        output_folder = self.get_output_folder()
        scale = int(self.gif_entry.get())

        if not input_path:
            print(f"{Colors.YELLOW}错误：请选择输入文件或文件夹！{Colors.RESET}")
            return

        if os.path.isfile(input_path):
            # 单个文件处理
            output_path = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(input_path))[0]}_{get_timestamp()}_{scale}_gif.gif",
            )
            convert_to_gif(input_path, output_path, scale=scale)
        else:
            # 文件夹批量处理
            video_files = get_video_files(input_path)
            for video_file in video_files:
                output_path = os.path.join(
                    output_folder,
                    f"{os.path.splitext(os.path.basename(video_file))[0]}_{get_timestamp()}_{scale}_gif.gif",
                )
                convert_to_gif(video_file, output_path, scale=scale)

    def start_compression(self):
        input_path = self.input_file_entry.get()
        output_folder = self.get_output_folder()
        crf = int(self.compress_entry.get())

        if not input_path:
            print(f"{Colors.YELLOW}错误：请选择输入文件或文件夹！{Colors.RESET}")
            return

        if os.path.isfile(input_path):
            # 单个文件处理
            output_path = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(input_path))[0]}_{get_timestamp()}_crf{crf}_compress.mp4",
            )
            compress_video(input_path, output_path, crf)
        else:
            # 文件夹批量处理
            video_files = get_video_files(input_path)
            for video_file in video_files:
                output_path = os.path.join(
                    output_folder,
                    f"{os.path.splitext(os.path.basename(video_file))[0]}_{get_timestamp()}_crf{crf}_compress.mp4",
                )
                compress_video(video_file, output_path, crf)
