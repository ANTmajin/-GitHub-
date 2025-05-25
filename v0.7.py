import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox,
                             QHBoxLayout, QDialog, QMenuBar, QMenu, QStatusBar, QAction,
                             QColorDialog, QSpinBox, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, QSettings, QMimeData, QUrl, QTranslator, QLocale
from PyQt5.QtGui import QColor, QPalette, QDragEnterEvent, QDropEvent
from git import Repo, GitCommandError
from github import Github, GithubException

class Translator:
    translations = {
        "zh_CN": {
            "app_title": "GitHub 自动上传工具",
            "menu_file": "文件",
            "menu_tools": "工具",
            "menu_help": "帮助",
            "menu_language": "语言",
            "action_save": "保存设置",
            "action_exit": "退出",
            "action_settings": "设置",
            "action_clear_log": "清除日志",
            "action_help": "使用帮助",
            "action_about": "关于",
            "action_lang_zh": "中文",
            "action_lang_en": "英文",
            "settings_title": "设置",
            "theme_group": "主题设置",
            "primary_color": "主颜色",
            "secondary_color": "次颜色",
            "text_color": "文本颜色",
            "menubar_color": "导航栏颜色",
            "reset_theme": "重置为默认主题",
            "save_group": "自动保存设置",
            "auto_save": "自动保存",
            "save_interval": "保存间隔",
            "minutes": "分钟",
            "save_btn": "保存设置",
            "cancel_btn": "取消",
            "language_group": "语言设置",
            "language_label": "界面语言",
            "help_title": "使用帮助",
            "close_help": "关闭帮助",
            "about_title": "关于",
            "about_text": "GitHub 自动上传工具 v0.7\n\n一个简单的图形界面工具，用于将本地文件上传到 GitHub 仓库。\n\n使用 Python 和 PyQt5 开发\n© 2025 开发者",
            "success": "成功",
            "settings_saved": "设置已保存",
            "ready": "准备就绪",
            "log_cleared": "日志已清除",
            "select_folder": "选择文件夹",
            "drag_drop": "拖拽文件或文件夹到这里",
            "token_label": "GitHub 个人访问令牌:",
            "repo_label": "GitHub 仓库 (格式: 用户名/仓库名):",
            "folder_label": "本地文件夹:",
            "commit_label": "提交信息:",
            "upload_btn": "上传到 GitHub",
            "log_label": "操作日志:",
            "warning": "警告",
            "fill_all_fields": "请填写所有字段",
            "error": "错误",
            "unknown_error": "未知错误",
            "upload_start": "开始上传过程...",
            "connected_to_github": "已连接到 GitHub",
            "found_existing_repo": "找到现有的 Git 仓库",
            "initializing_new_repo": "初始化新的 Git 仓库",
            "repo_initialized": "Git 仓库初始化完成",
            "files_staged": "已添加所有文件到暂存区",
            "changes_committed": "已提交更改",
            "remote_url_updated": "更新了远程仓库 URL",
            "new_remote_created": "创建了新的远程仓库",
            "pushing_changes": "正在推送更改到 GitHub...",
            "push_successful": "推送成功完成!",
            "upload_successful": "文件已成功上传到 GitHub 仓库",
            "upload_complete": "上传成功完成!",
            "git_error": "Git 错误",
            "github_error": "GitHub 错误",
            "upload_failed": "上传失败",
            "github_api_error": "GitHub API 错误",
            "auto_save_enabled": "自动保存已启用",
            "auto_save_disabled": "自动保存已禁用",
            "every": "每"
        },
        "en_US": {
            "app_title": "GitHub Auto Uploader",
            "menu_file": "File",
            "menu_tools": "Tools",
            "menu_help": "Help",
            "menu_language": "Language",
            "action_save": "Save Settings",
            "action_exit": "Exit",
            "action_settings": "Settings",
            "action_clear_log": "Clear Log",
            "action_help": "Help",
            "action_about": "About",
            "action_lang_zh": "Chinese",
            "action_lang_en": "English",
            "settings_title": "Settings",
            "theme_group": "Theme Settings",
            "primary_color": "Primary Color",
            "secondary_color": "Secondary Color",
            "text_color": "Text Color",
            "menubar_color": "Menu Bar Color",
            "reset_theme": "Reset to Default Theme",
            "save_group": "Auto Save Settings",
            "auto_save": "Auto Save",
            "save_interval": "Save Interval",
            "minutes": "minutes",
            "save_btn": "Save Settings",
            "cancel_btn": "Cancel",
            "language_group": "Language Settings",
            "language_label": "Interface Language",
            "help_title": "Help",
            "close_help": "Close Help",
            "about_title": "About",
            "about_text": "GitHub Auto Uploader v0.7\n\nA simple GUI tool for uploading files to GitHub repositories.\n\nBuilt with Python and PyQt5\n© 2025 Developer",
            "success": "Success",
            "settings_saved": "Settings saved",
            "ready": "Ready",
            "log_cleared": "Log cleared",
            "select_folder": "Select Folder",
            "drag_drop": "Drag and drop files or folders here",
            "token_label": "GitHub Personal Access Token:",
            "repo_label": "GitHub Repository (format: username/repo):",
            "folder_label": "Local Folder:",
            "commit_label": "Commit Message:",
            "upload_btn": "Upload to GitHub",
            "log_label": "Operation Log:",
            "warning": "Warning",
            "fill_all_fields": "Please fill in all fields",
            "error": "Error",
            "unknown_error": "Unknown error",
            "upload_start": "Starting upload process...",
            "connected_to_github": "Connected to GitHub",
            "found_existing_repo": "Found existing Git repository",
            "initializing_new_repo": "Initializing new Git repository",
            "repo_initialized": "Git repository initialized",
            "files_staged": "All files added to staging area",
            "changes_committed": "Changes committed",
            "remote_url_updated": "Remote repository URL updated",
            "new_remote_created": "New remote repository created",
            "pushing_changes": "Pushing changes to GitHub...",
            "push_successful": "Push successful!",
            "upload_successful": "Files successfully uploaded to GitHub repository",
            "upload_complete": "Upload completed successfully!",
            "git_error": "Git error",
            "github_error": "GitHub error",
            "upload_failed": "Upload failed",
            "github_api_error": "GitHub API error",
            "auto_save_enabled": "Auto save enabled",
            "auto_save_disabled": "Auto save disabled",
            "every": "Every"
        }
    }

    @classmethod
    def get_translation(cls, lang, key):
        return cls.translations.get(lang, {}).get(key, key)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = QSettings("GitHubUploader", "AppSettings")
        self.lang = self.settings.value("language", "zh_CN")
        
        self.initUI()
        self.load_settings()
        self.retranslate_ui()
    
    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        
        layout = QVBoxLayout()
        
        # 主题设置组
        self.theme_group = QGroupBox()
        theme_layout = QFormLayout()
        
        self.primary_color_btn = QPushButton()
        self.primary_color_btn.clicked.connect(lambda: self.choose_color("primary"))
        self.secondary_color_btn = QPushButton()
        self.secondary_color_btn.clicked.connect(lambda: self.choose_color("secondary"))
        self.text_color_btn = QPushButton()
        self.text_color_btn.clicked.connect(lambda: self.choose_color("text"))
        self.menubar_color_btn = QPushButton()
        self.menubar_color_btn.clicked.connect(lambda: self.choose_color("menubar"))
        
        theme_layout.addRow(QLabel(), self.primary_color_btn)
        theme_layout.addRow(QLabel(), self.secondary_color_btn)
        theme_layout.addRow(QLabel(), self.text_color_btn)
        theme_layout.addRow(QLabel(), self.menubar_color_btn)
        
        self.reset_theme_btn = QPushButton()
        self.reset_theme_btn.clicked.connect(self.reset_theme)
        theme_layout.addRow(self.reset_theme_btn)
        
        self.theme_group.setLayout(theme_layout)
        layout.addWidget(self.theme_group)
        
        # 自动保存组
        self.save_group = QGroupBox()
        save_layout = QFormLayout()
        
        self.auto_save_checkbox = QPushButton()
        self.auto_save_checkbox.setCheckable(True)
        self.auto_save_checkbox.clicked.connect(self.toggle_auto_save)
        
        self.save_interval_spin = QSpinBox()
        self.save_interval_spin.setRange(1, 60)
        self.minutes_label = QLabel()
        
        save_layout.addRow(QLabel(), self.auto_save_checkbox)
        save_layout.addRow(QLabel(), QHBoxLayout())
        save_layout.itemAt(save_layout.count()-1).layout().addWidget(self.save_interval_spin)
        save_layout.itemAt(save_layout.count()-1).layout().addWidget(self.minutes_label)
        
        self.save_group.setLayout(save_layout)
        layout.addWidget(self.save_group)
        
        # 语言设置组
        self.language_group = QGroupBox()
        language_layout = QFormLayout()
        
        self.lang_zh_radio = QAction("中文", self)
        self.lang_en_radio = QAction("English", self)
        
        language_layout.addRow(QLabel(), QLabel())
        
        self.language_group.setLayout(language_layout)
        layout.addWidget(self.language_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton()
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def retranslate_ui(self):
        self.setWindowTitle(Translator.get_translation(self.lang, "settings_title"))
        self.theme_group.setTitle(Translator.get_translation(self.lang, "theme_group"))
        self.primary_color_btn.setText(Translator.get_translation(self.lang, "primary_color"))
        self.secondary_color_btn.setText(Translator.get_translation(self.lang, "secondary_color"))
        self.text_color_btn.setText(Translator.get_translation(self.lang, "text_color"))
        self.menubar_color_btn.setText(Translator.get_translation(self.lang, "menubar_color"))
        self.reset_theme_btn.setText(Translator.get_translation(self.lang, "reset_theme"))
        self.save_group.setTitle(Translator.get_translation(self.lang, "save_group"))
        self.auto_save_checkbox.setText(Translator.get_translation(self.lang, "auto_save_enabled" if self.auto_save_checkbox.isChecked() else "auto_save_disabled"))
        self.minutes_label.setText(Translator.get_translation(self.lang, "minutes"))
        self.language_group.setTitle(Translator.get_translation(self.lang, "language_group"))
        self.save_btn.setText(Translator.get_translation(self.lang, "save_btn"))
        self.cancel_btn.setText(Translator.get_translation(self.lang, "cancel_btn"))
    
    def load_settings(self):
        # 加载颜色设置
        self.primary_color = self.settings.value("theme/primary", QColor(48, 167, 69))
        self.secondary_color = self.settings.value("theme/secondary", QColor(3, 102, 214))
        self.text_color = self.settings.value("theme/text", QColor(0, 0, 0))
        self.menubar_color = self.settings.value("theme/menubar", QColor(0, 0, 0))
        
        # 加载自动保存设置
        auto_save = self.settings.value("auto_save/enabled", False, type=bool)
        self.auto_save_checkbox.setChecked(auto_save)
        self.auto_save_checkbox.setText(Translator.get_translation(self.lang, "auto_save_enabled" if auto_save else "auto_save_disabled"))
        
        save_interval = self.settings.value("auto_save/interval", 5, type=int)
        self.save_interval_spin.setValue(save_interval)
    
    def choose_color(self, color_type):
        color = QColorDialog.getColor()
        if color.isValid():
            if color_type == "primary":
                self.primary_color = color
            elif color_type == "secondary":
                self.secondary_color = color
            elif color_type == "text":
                self.text_color = color
            elif color_type == "menubar":
                self.menubar_color = color
    
    def reset_theme(self):
        self.primary_color = QColor(48, 167, 69)  # GitHub 绿色
        self.secondary_color = QColor(3, 102, 214)  # GitHub 蓝色
        self.text_color = QColor(0, 0, 0)  # 黑色
        self.menubar_color = QColor(0, 0, 0)  # 黑色
    
    def toggle_auto_save(self):
        checked = self.auto_save_checkbox.isChecked()
        self.auto_save_checkbox.setText(Translator.get_translation(self.lang, "auto_save_enabled" if checked else "auto_save_disabled"))
    
    def save_settings(self):
        # 保存颜色设置
        self.settings.setValue("theme/primary", self.primary_color)
        self.settings.setValue("theme/secondary", self.secondary_color)
        self.settings.setValue("theme/text", self.text_color)
        self.settings.setValue("theme/menubar", self.menubar_color)
        
        # 保存自动保存设置
        self.settings.setValue("auto_save/enabled", self.auto_save_checkbox.isChecked())
        self.settings.setValue("auto_save/interval", self.save_interval_spin.value())
        
        # 应用新主题
        self.parent.apply_theme(
            self.primary_color,
            self.secondary_color,
            self.text_color,
            self.menubar_color
        )
        
        # 更新自动保存定时器
        self.parent.setup_auto_save()
        
        QMessageBox.information(self, 
                              Translator.get_translation(self.lang, "success"),
                              Translator.get_translation(self.lang, "settings_saved"))
        self.close()


class HelpDialog(QDialog):
    def __init__(self, lang="zh_CN"):
        super().__init__()
        self.lang = lang
        self.setGeometry(300, 300, 800, 600)
        
        self.initUI()
        self.update_help_content()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.help_text = QTextEdit()
        self.help_text.setReadOnly(True)
        
        self.close_button = QPushButton()
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #0366d6;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0356b6;
            }
        """)
        self.close_button.clicked.connect(self.close)
        
        layout.addWidget(self.help_text)
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
    
    def update_help_content(self):
        self.setWindowTitle(Translator.get_translation(self.lang, "help_title"))
        self.close_button.setText(Translator.get_translation(self.lang, "close_help"))
        
        if self.lang == "zh_CN":
            content = """
            <h1 style="color: #0366d6;">GitHub 自动上传工具使用指南</h1>
            <h2 style="color: #24292e;">1. 准备工作</h2>
            <p>在使用本工具前，您需要:</p>
            <ul>
                <li>拥有一个 GitHub 账号</li>
                <li>在 GitHub 上创建好仓库</li>
                <li>生成个人访问令牌 (PAT)</li>
            </ul>
            
            <h2 style="color: #24292e;">2. 获取个人访问令牌</h2>
            <p>按照以下步骤获取令牌:</p>
            <ol>
                <li>登录 GitHub 账户</li>
                <li>进入 Settings > Developer settings > Personal access tokens</li>
                <li>点击 "Generate new token"</li>
                <li>为令牌命名</li>
                <li>勾选 "repo" 权限</li>
                <li>点击 "Generate token" 按钮</li>
                <li>复制生成的令牌 (这是您唯一一次能看到它的机会)</li>
            </ol>
            
            <h2 style="color: #24292e;">3. 使用本工具</h2>
            <p>操作步骤:</p>
            <ol>
                <li>在 "GitHub 个人访问令牌" 字段粘贴您的令牌</li>
                <li>在 "GitHub 仓库" 字段输入仓库名称 (格式: 用户名/仓库名)</li>
                <li>点击 "浏览..." 按钮选择本地文件夹</li>
                <li>在 "提交信息" 字段输入有意义的描述</li>
                <li>点击 "上传到 GitHub" 按钮</li>
            </ol>
            
            <h2 style="color: #24292e;">4. 注意事项</h2>
            <ul>
                <li>令牌相当于密码，请妥善保管</li>
                <li>如果文件夹不是 Git 仓库，工具会自动初始化</li>
                <li>上传大量文件可能需要较长时间</li>
                <li>确保网络连接正常</li>
            </ul>
            """
        else:
            content = """
            <h1 style="color: #0366d6;">GitHub Auto Uploader Guide</h1>
            <h2 style="color: #24292e;">1. Prerequisites</h2>
            <p>Before using this tool, you need:</p>
            <ul>
                <li>A GitHub account</li>
                <li>A repository created on GitHub</li>
                <li>A personal access token (PAT)</li>
            </ul>
            
            <h2 style="color: #24292e;">2. Get Personal Access Token</h2>
            <p>Follow these steps to get a token:</p>
            <ol>
                <li>Log in to your GitHub account</li>
                <li>Go to Settings > Developer settings > Personal access tokens</li>
                <li>Click "Generate new token"</li>
                <li>Name your token</li>
                <li>Check the "repo" scope</li>
                <li>Click "Generate token" button</li>
                <li>Copy the generated token (this is the only time you'll see it)</li>
            </ol>
            
            <h2 style="color: #24292e;">3. Using This Tool</h2>
            <p>Steps to use:</p>
            <ol>
                <li>Paste your token in the "GitHub Personal Access Token" field</li>
                <li>Enter repository name (format: username/repo) in "GitHub Repository" field</li>
                <li>Click "Browse..." to select local folder</li>
                <li>Enter meaningful description in "Commit Message" field</li>
                <li>Click "Upload to GitHub" button</li>
            </ol>
            
            <h2 style="color: #24292e;">4. Notes</h2>
            <ul>
                <li>Treat your token like a password and keep it secure</li>
                <li>If folder is not a Git repo, tool will initialize it automatically</li>
                <li>Uploading many files may take some time</li>
                <li>Ensure you have stable internet connection</li>
            </ul>
            """
        
        self.help_text.setHtml(content)


class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.parent = parent
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 20px;
                background-color: #f9f9f9;
            }
            QWidget:hover {
                border-color: #0366d6;
                background-color: #f0f7ff;
            }
        """)
        
        layout = QVBoxLayout()
        self.label = QLabel(Translator.get_translation(self.parent.lang, "drag_drop"))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #555;")
        
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isdir(path):
                self.parent.folder_path.setText(path)
                self.parent.statusBar().showMessage(
                    f"{Translator.get_translation(self.parent.lang, 'folder_label')}: {path}", 
                    3000
                )
            else:
                folder = os.path.dirname(path)
                self.parent.folder_path.setText(folder)
                self.parent.statusBar().showMessage(
                    f"{Translator.get_translation(self.parent.lang, 'folder_label')}: {folder}", 
                    3000
                )
        event.acceptProposedAction()


class GitHubUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("GitHubUploader", "AppSettings")
        self.lang = self.settings.value("language", "zh_CN")
        self.translator = QTranslator()
        
        # 初始化UI组件
        self.token_input = QLineEdit()
        self.repo_input = QLineEdit()
        self.folder_path = QLineEdit()
        self.commit_input = QLineEdit()
        self.log_output = QTextEdit()
        
        self.initUI()
        self.load_settings()
        self.setup_auto_save()
        self.retranslate_ui()
        
        self.repo = None
        self.gh = None
    
    def initUI(self):
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建菜单栏
        self.createMenuBar()
        
        # 创建状态栏
        self.statusBar().showMessage(Translator.get_translation(self.lang, "ready"))
        
        # 主窗口部件
        main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        
        # 拖拽区域
        self.drop_area = DropArea(self)
        self.main_layout.addWidget(self.drop_area)
        
        # GitHub 令牌输入
        self.token_label = QLabel()
        self.token_input.setPlaceholderText(Translator.get_translation(self.lang, "token_label"))
        self.token_input.setMinimumHeight(35)
        self.main_layout.addWidget(self.token_label)
        self.main_layout.addWidget(self.token_input)
        
        # 仓库信息
        self.repo_label = QLabel()
        self.repo_input.setPlaceholderText(Translator.get_translation(self.lang, "repo_label"))
        self.repo_input.setMinimumHeight(35)
        self.main_layout.addWidget(self.repo_label)
        self.main_layout.addWidget(self.repo_input)
        
        # 本地文件夹选择
        self.folder_label = QLabel()
        self.folder_path.setReadOnly(True)
        self.folder_path.setMinimumHeight(35)
        
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path)
        
        self.browse_button = QPushButton()
        self.browse_button.setMinimumHeight(35)
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_button)
        
        self.main_layout.addWidget(self.folder_label)
        self.main_layout.addLayout(folder_layout)
        
        # 提交信息
        self.commit_label = QLabel()
        self.commit_input.setPlaceholderText(Translator.get_translation(self.lang, "commit_label"))
        self.commit_input.setMinimumHeight(35)
        self.main_layout.addWidget(self.commit_label)
        self.main_layout.addWidget(self.commit_input)
        
        # 操作按钮
        self.upload_button = QPushButton()
        self.upload_button.setMinimumHeight(40)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #22863a;
            }
        """)
        self.upload_button.clicked.connect(self.upload_to_github)
        self.main_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        
        # 日志输出
        self.log_label = QLabel()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(300)
        self.main_layout.addWidget(self.log_label)
        self.main_layout.addWidget(self.log_output)
        
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)
    
    def retranslate_ui(self):
        self.setWindowTitle(Translator.get_translation(self.lang, "app_title"))
        self.token_label.setText(Translator.get_translation(self.lang, "token_label"))
        self.repo_label.setText(Translator.get_translation(self.lang, "repo_label"))
        self.folder_label.setText(Translator.get_translation(self.lang, "folder_label"))
        self.browse_button.setText(Translator.get_translation(self.lang, "select_folder"))
        self.commit_label.setText(Translator.get_translation(self.lang, "commit_label"))
        self.upload_button.setText(Translator.get_translation(self.lang, "upload_btn"))
        self.log_label.setText(Translator.get_translation(self.lang, "log_label"))
        self.drop_area.label.setText(Translator.get_translation(self.lang, "drag_drop"))
    
    def createMenuBar(self):
        # 清除现有菜单栏
        self.menuBar().clear()
        
        menuBar = self.menuBar()
        menuBar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {self.settings.value("theme/menubar", QColor(0, 0, 0)).name()};
                color: white;
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 5px 10px;
            }}
            QMenuBar::item:selected {{
                background-color: #555;
            }}
            QMenuBar::item:pressed {{
                background-color: #777;
            }}
        """)
        
        # 文件菜单
        fileMenu = menuBar.addMenu(Translator.get_translation(self.lang, "menu_file"))
        
        saveAction = QAction(Translator.get_translation(self.lang, "action_save"), self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip(Translator.get_translation(self.lang, "action_save"))
        saveAction.triggered.connect(self.save_settings)
        fileMenu.addAction(saveAction)
        
        exitAction = QAction(Translator.get_translation(self.lang, "action_exit"), self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip(Translator.get_translation(self.lang, "action_exit"))
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        # 工具菜单
        toolMenu = menuBar.addMenu(Translator.get_translation(self.lang, "menu_tools"))
        
        settingsAction = QAction(Translator.get_translation(self.lang, "action_settings"), self)
        settingsAction.setStatusTip(Translator.get_translation(self.lang, "action_settings"))
        settingsAction.triggered.connect(self.show_settings)
        toolMenu.addAction(settingsAction)
        
        clearLogAction = QAction(Translator.get_translation(self.lang, "action_clear_log"), self)
        clearLogAction.setStatusTip(Translator.get_translation(self.lang, "action_clear_log"))
        clearLogAction.triggered.connect(self.clear_log)
        toolMenu.addAction(clearLogAction)
        
        # 语言菜单
        languageMenu = menuBar.addMenu(Translator.get_translation(self.lang, "menu_language"))
        
        langZhAction = QAction(Translator.get_translation("zh_CN", "action_lang_zh"), self)
        langZhAction.triggered.connect(lambda: self.change_language("zh_CN"))
        languageMenu.addAction(langZhAction)
        
        langEnAction = QAction(Translator.get_translation("en_US", "action_lang_en"), self)
        langEnAction.triggered.connect(lambda: self.change_language("en_US"))
        languageMenu.addAction(langEnAction)
        
        # 帮助菜单
        helpMenu = menuBar.addMenu(Translator.get_translation(self.lang, "menu_help"))
        
        helpAction = QAction(Translator.get_translation(self.lang, "action_help"), self)
        helpAction.setShortcut("F1")
        helpAction.setStatusTip(Translator.get_translation(self.lang, "action_help"))
        helpAction.triggered.connect(self.show_help)
        helpMenu.addAction(helpAction)
        
        aboutAction = QAction(Translator.get_translation(self.lang, "action_about"), self)
        aboutAction.setStatusTip(Translator.get_translation(self.lang, "action_about"))
        aboutAction.triggered.connect(self.show_about)
        helpMenu.addAction(aboutAction)
    
    def change_language(self, lang):
        self.lang = lang
        self.settings.setValue("language", lang)
        self.retranslate_ui()
        self.createMenuBar()  # 重新创建菜单栏以完全更新语言
        self.statusBar().showMessage(Translator.get_translation(self.lang, "ready"), 3000)
    
    def save_settings(self):
        try:
            settings_to_save = {
                "token": self.token_input.text(),
                "repo_path": self.repo_input.text(),
                "local_path": self.folder_path.text(),
                "last_updated": datetime.now().isoformat()
            }
            
            self.settings.setValue("app_state", json.dumps(settings_to_save))
            self.statusBar().showMessage(Translator.get_translation(self.lang, "settings_saved"), 3000)
            return True
        except Exception as e:
            self.log_message(f"{Translator.get_translation(self.lang, 'error')}: {str(e)}")
            return False
    
    def clear_log(self):
        self.log_output.clear()
        self.statusBar().showMessage(Translator.get_translation(self.lang, "log_cleared"), 3000)
    
    def show_about(self):
        QMessageBox.about(self, 
                         Translator.get_translation(self.lang, "about_title"),
                         Translator.get_translation(self.lang, "about_text"))
    
    def show_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()
    
    def show_help(self):
        help_dialog = HelpDialog(self.lang)
        help_dialog.exec_()
    
    def load_settings(self):
        # 加载主题
        primary_color = self.settings.value("theme/primary", QColor(48, 167, 69))
        secondary_color = self.settings.value("theme/secondary", QColor(3, 102, 214))
        text_color = self.settings.value("theme/text", QColor(0, 0, 0))
        menubar_color = self.settings.value("theme/menubar", QColor(0, 0, 0))
        self.apply_theme(primary_color, secondary_color, text_color, menubar_color)
        
        # 加载保存的状态
        app_state = self.settings.value("app_state")
        if app_state:
            try:
                state = json.loads(app_state)
                self.token_input.setText(state.get("token", ""))
                self.repo_input.setText(state.get("repo_path", ""))
                self.folder_path.setText(state.get("local_path", ""))
            except json.JSONDecodeError:
                pass
    
    def apply_theme(self, primary_color, secondary_color, text_color, menubar_color):
        palette = self.palette()
        
        # 设置主颜色 (按钮、强调元素)
        palette.setColor(QPalette.Button, primary_color)
        palette.setColor(QPalette.Highlight, primary_color)
        palette.setColor(QPalette.ButtonText, Qt.white)
        
        # 设置次颜色 (标题、边框等)
        palette.setColor(QPalette.WindowText, secondary_color)
        
        # 设置文本颜色
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.WindowText, text_color)
        
        self.setPalette(palette)
        
        # 设置导航栏颜色
        self.menuBar().setStyleSheet(f"""
            QMenuBar {{
                background-color: {menubar_color.name()};
                color: white;
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 5px 10px;
            }}
            QMenuBar::item:selected {{
                background-color: #555;
            }}
            QMenuBar::item:pressed {{
                background-color: #777;
            }}
        """)
        
        # 更新特定组件的样式
        self.style().unpolish(self)
        self.style().polish(self)
    
    def setup_auto_save(self):
        self.auto_save_timer = QTimer()
        self.auto_save_timer.stop()
        
        auto_save_enabled = self.settings.value("auto_save/enabled", False, type=bool)
        if auto_save_enabled:
            interval_minutes = self.settings.value("auto_save/interval", 5, type=int)
            interval_ms = interval_minutes * 60 * 1000
            
            self.auto_save_timer.timeout.connect(self.auto_save)
            self.auto_save_timer.start(interval_ms)
            self.statusBar().showMessage(
                f"{Translator.get_translation(self.lang, 'auto_save_enabled')} - {Translator.get_translation(self.lang, 'every')} {interval_minutes} {Translator.get_translation(self.lang, 'minutes')}", 
                5000
            )
    
    def auto_save(self):
        self.save_settings()
        self.last_save_time = datetime.now()
        self.statusBar().showMessage(
            f"{Translator.get_translation(self.lang, 'settings_saved')} - {self.last_save_time.strftime('%H:%M:%S')}", 
            3000
        )
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, Translator.get_translation(self.lang, "select_folder"))
        if folder:
            self.folder_path.setText(folder)
            self.statusBar().showMessage(
                f"{Translator.get_translation(self.lang, 'folder_label')}: {folder}", 
                3000
            )
    
    def log_message(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()
    
    def upload_to_github(self):
        token = self.token_input.text().strip()
        repo_path = self.repo_input.text().strip()
        local_path = self.folder_path.text().strip()
        commit_msg = self.commit_input.text().strip()
        
        if not all([token, repo_path, local_path, commit_msg]):
            QMessageBox.warning(self, 
                              Translator.get_translation(self.lang, "warning"),
                              Translator.get_translation(self.lang, "fill_all_fields"))
            self.statusBar().showMessage(
                f"{Translator.get_translation(self.lang, 'error')}: {Translator.get_translation(self.lang, 'fill_all_fields')}", 
                5000
            )
            return
        
        try:
            self.statusBar().showMessage(Translator.get_translation(self.lang, "upload_start"), 3000)
            self.log_message(Translator.get_translation(self.lang, "upload_start"))
            
            # 初始化 GitHub 连接
            self.gh = Github(token)
            self.log_message(Translator.get_translation(self.lang, "connected_to_github"))
            
            # 检查本地仓库是否存在
            git_folder = os.path.join(local_path, '.git')
            if os.path.exists(git_folder):
                self.log_message(Translator.get_translation(self.lang, "found_existing_repo"))
                repo = Repo(local_path)
            else:
                self.log_message(Translator.get_translation(self.lang, "initializing_new_repo"))
                repo = Repo.init(local_path)
                self.log_message(Translator.get_translation(self.lang, "repo_initialized"))
            
            # 添加所有文件
            repo.git.add('--all')
            self.log_message(Translator.get_translation(self.lang, "files_staged"))
            
            # 提交更改
            repo.index.commit(commit_msg)
            self.log_message(f"{Translator.get_translation(self.lang, 'changes_committed')}: {commit_msg}")
            
            # 获取远程仓库
            remote_name = 'origin'
            remote_url = f"https://{token}@github.com/{repo_path}.git"
            
            if remote_name in repo.remotes:
                remote = repo.remotes[remote_name]
                remote.set_url(remote_url)
                self.log_message(Translator.get_translation(self.lang, "remote_url_updated"))
            else:
                remote = repo.create_remote(remote_name, remote_url)
                self.log_message(Translator.get_translation(self.lang, "new_remote_created"))
            
            # 推送更改
            self.log_message(Translator.get_translation(self.lang, "pushing_changes"))
            self.statusBar().showMessage(Translator.get_translation(self.lang, "pushing_changes"), 3000)
            remote.push().raise_if_error()
            self.log_message(Translator.get_translation(self.lang, "push_successful"))
            
            QMessageBox.information(self, 
                                   Translator.get_translation(self.lang, "success"),
                                   Translator.get_translation(self.lang, "upload_successful"))
            self.statusBar().showMessage(Translator.get_translation(self.lang, "upload_complete"), 5000)
            
        except GitCommandError as e:
            error_msg = f"{Translator.get_translation(self.lang, 'git_error')}: {str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, 
                                Translator.get_translation(self.lang, "error"),
                                error_msg)
            self.statusBar().showMessage(
                f"{Translator.get_translation(self.lang, 'upload_failed')}: {Translator.get_translation(self.lang, 'git_error')}", 
                5000
            )
        except GithubException as e:
            error_msg = f"{Translator.get_translation(self.lang, 'github_api_error')}: {str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, 
                                Translator.get_translation(self.lang, "error"),
                                error_msg)
            self.statusBar().showMessage(
                f"{Translator.get_translation(self.lang, 'upload_failed')}: {Translator.get_translation(self.lang, 'github_error')}", 
                5000
            )
        except Exception as e:
            error_msg = f"{Translator.get_translation(self.lang, 'unknown_error')}: {str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, 
                                Translator.get_translation(self.lang, "error"),
                                error_msg)
            self.statusBar().showMessage(
                f"{Translator.get_translation(self.lang, 'upload_failed')}: {Translator.get_translation(self.lang, 'unknown_error')}", 
                5000
            )
    
    def closeEvent(self, event):
        if self.settings.value("auto_save/enabled", False, type=bool):
            self.save_settings()
        
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = GitHubUploader()
    
    # 恢复窗口大小和位置
    size = window.settings.value("window/size")
    position = window.settings.value("window/position")
    if size:
        window.resize(size)
    if position:
        window.move(position)
    
    window.show()
    sys.exit(app.exec_())
