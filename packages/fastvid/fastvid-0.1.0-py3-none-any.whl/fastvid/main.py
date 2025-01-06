import utils
import customtkinter as ctk


def main():
    root = ctk.CTk()
    app = utils.VideoToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
