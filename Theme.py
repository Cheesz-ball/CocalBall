class Theme:
    def __init__(self, mode):
        self.spinbox_color = "#e3e4e2"
        self.title_bar_color = "#fcfcfc"
        self.bottom_bar_color = "#f6f6f6"
        self.main_color = "#ffffff"
        self.sidebar_color = "#f6f6f6"
        self.main_font = "#222222"
        self.button_sidebar_color = "#f6f6f6"
        self.button_sidebar_hover_color = "#d9d9d9"
        self.button_highlight_color = "#8a5cf5"
        self.button_highlight_hover_color = "#a68af9"
        self.button_theme_hover_color = "#a68af9"
        self.button_common_color = "#363636"
        self.button_common_hover_color = "#3f3f3f"
        self.button_border_color = "#e8e8e8"
        self.processbar_color = "#6e4ac4"
        self.title_bar_close_color = "#982B1C"
        self.spinbox_border_color = "#a68af9"
        self.spinbox_border_hover_color = "#8a5cf5"
        self.combobox_boder_color = "#a68af9"
        self.combobox_font = "#000000"
        self.combobox_color = "#e3e4e2"
        # 根据 mode 设置主题
        if mode:
            self.darkMode()
        else:
            self.lightMode()

    def darkMode(self):
        self.title_bar_color = "#262626"
        self.bottom_bar_color = "#262626"
        self.main_color = "#161616"
        self.sidebar_color = "#1b1b1b"
        self.main_font = "#ffffff"
        self.button_sidebar_color = "#1b1b1b"
        self.button_sidebar_hover_color = "#3f3f3f"
        self.button_highlight_color = "#8a5cf5"
        self.button_highlight_hover_color = "#a68af9"
        self.button_theme_hover_color = "#fcfcfc"
        self.button_common_color = "#363636"
        self.button_common_hover_color = "#3f3f3f"
        self.button_border_color = "#1b1b1b"
        self.processbar_color = "#6e4ac4"
        self.title_bar_close_color = "#982B1C"
        self.spinbox_color = "#363636"
        self.spinbox_border_color = "#a68af9"
        self.spinbox_border_hover_color = "#8a5cf5"
        self.combobox_boder_color = "#a68af9"
        self.combobox_font = "#ffffff"
        self.combobox_color = "#363636"

    def lightMode(self):
        self.title_bar_color = "#fcfcfc"
        self.bottom_bar_color = "#f6f6f6"
        self.main_color = "#ffffff"
        self.sidebar_color = "#f6f6f6"
        self.main_font = "#222222"
        self.button_sidebar_color = "#f6f6f6"
        self.button_sidebar_hover_color = "#d9d9d9"
        self.button_highlight_color = "#8a5cf5"
        self.button_highlight_hover_color = "#a68af9"
        self.button_theme_hover_color = "#a68af9"
        self.button_common_color = "#ffffff"
        self.button_common_hover_color = "#fafafa"
        self.button_border_color = "#d7d7d7"
        self.processbar_color = "#6e4ac4"
        self.title_bar_close_color = "#982B1C"
        self.spinbox_color = "#e3e4e2"
        self.spinbox_border_color = "#a68af9"
        self.spinbox_border_hover_color = "#8a5cf5"
        self.combobox_boder_color = "#a68af9"
        self.combobox_font = "#000000"
        self.combobox_color = "#e3e4e2"
