"""
Project: ak_video_analyser Azure Kinect Video Analyser
Github repository: https://github.com/juancarlosmiranda/ak_video_analyser

Author: Juan Carlos Miranda
* https://juancarlosmiranda.github.io/
* https://github.com/juancarlosmiranda

Date: February 2021
Description:

Use:

"""
import os
import tkinter as tk
import webbrowser
from gui_analyser.gui_video_analyser_config import GUIAKVideoAnalyserConfig


class VideoAnalyserAboutWindow(tk.Toplevel):
    author_str = 'Juan Carlos Miranda'
    author_site_str = 'https://github.com/juancarlosmiranda'
    title_str = 'AK Video Analyser \n(ak_video_analyser)'
    version_number_str = '1.0'
    release_date = 'February 2022'

    def __init__(self, parent):
        super().__init__(parent)
        # self.geometry(GUIAKVideoAnalyserConfig.geometry_about)
        self.title('About...')
        self.resizable(width=False, height=False)  # do not change the size
        self.attributes('-topmost', True)
        # -----------------------
        assets_path = os.path.dirname(os.path.abspath(__file__))
        img_path_01 = os.path.join(assets_path, 'assets', 'icon_app.png')
        self.iconphoto(False, tk.PhotoImage(file=img_path_01))
        # -----------------------
        about_label = tk.Label(self, text=self.title_str + ' ' + self.version_number_str)
        about_label.config(font=("Verdana", 12))
        about_label.pack(anchor=tk.CENTER)
        text_info = tk.Label(self)

        about_text_info = f' \n' \
                          f'Developed by: {self.author_str}\n' \
                          f'{self.release_date} \n' \
                          f' Advisors: Jaume Arno, Eduard Gregorio\n' \
                          f' Collaborators: Jordi Gene-Mola, Spyros Fountas\n'

        project_text_info = f' \n' \
                            f'PAgFRUIT project RTI2018-094222-B-I00\n' \
                            f'http://www.pagfruit.udl.cat/'

        group_text_info = f' \n' \
                          f'Research Group on\n' \
                          f'AgroICT & Precision Agriculture\n' \
                          f'GRAP Universitat de Lleida\n' \
                          f'Agrotecnio - CERCA Center\n' \
                          f'https://www.grap.udl.cat/\n' \
                          f'Smart Farming Technology Group - Agricultural University of Athens\n' \
                          f'https://www.aua.gr/'

        text_info['text'] = about_text_info
        text_info.pack(anchor=tk.CENTER)

        author_link = tk.Label(self, text=self.author_site_str, font=("Verdana", 9), fg="blue", cursor="hand2")
        author_link.pack()
        author_link.bind("<Button-1>", lambda e: self.callback(self.author_site_str))

        project_link = tk.Label(self, text=project_text_info, font=("Verdana", 9), fg="blue", cursor="hand2")
        project_link.pack()
        project_link.bind("<Button-1>", lambda e: self.callback("http://www.pagfruit.udl.cat/"))

        group_link = tk.Label(self, text=group_text_info, font=("Verdana", 9), fg="blue", cursor="hand2")
        group_link.pack()
        group_link.bind("<Button-1>", lambda e: self.callback("https://www.grap.udl.cat/"))

        img_label_01 = tk.Label(self)
        assets_path = os.path.dirname(os.path.abspath(__file__))
        img_path_01 = os.path.join(assets_path, 'assets', 'logo_grap.png')
        img_label_01.image = tk.PhotoImage(file=img_path_01)
        img_label_01['image'] = img_label_01.image
        img_label_01.pack()
        # -----------------------

        # img_label_02 = tk.Label(self)
        # assets_path = os.path.dirname(os.path.abspath(__file__))
        # img_path_02 = os.path.join(assets_path, 'assets', 'logo_collaborators.png')
        # img_label_02.image = tk.PhotoImage(file=img_path_02)
        # img_label_02['image'] = img_label_02.image
        # img_label_02.pack()
        # -----------------------

        buttonClose = tk.Button(self, text='Close', command=self.destroy)
        buttonClose.pack(expand=True)

    def callback(self, url):
        webbrowser.open_new_tab(url)