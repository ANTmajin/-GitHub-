import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox,
                             QHBoxLayout, QDialog, QMenuBar, QMenu, QStatusBar, QAction,
                             QColorDialog, QSpinBox, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt, QTimer, QSettings, QMimeData, QUrl
from PyQt5.QtGui import QColor, QPalette, QDragEnterEvent, QDropEvent
from git import Repo, GitCommandError
from github import Github, GithubException

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setGeometry(300, 300, 500, 400)
        
        self.parent = parent
        self.settings = QSettings("GitHubUploader", "AppSettings")
        
        self.initUI()
        self.load_settings()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # 主题设置组
        theme_group = QGroupBox("主题设置")
        theme_layout = QFormLayout()
        
        self.primary_color_btn = QPushButton("选择主颜色")
        self.primary_color_btn.clicked.connect(lambda: self.choose_color("primary"))
        self.secondary_color_btn = QPushButton("选择次颜色")
        self.secondary_color_btn.clicked.connect(lambda: self.choose_color("secondary"))
        self.text_color_btn = QPushButton("选择文本颜色")
        self.text_color_btn.clicked.connect(lambda: self.choose_color("text"))
        self.menubar_color_btn = QPushButton("选择导航栏颜色")
        self.menubar_color_btn.clicked.connect(lambda: self.choose_color("menubar"))
        
        theme_layout.addRow("主颜色:", self.primary_color_btn)
        theme_layout.addRow("次颜色:", self.secondary_color_btn)
        theme_layout.addRow("文本颜色:", self.text_color_btn)
        theme_layout.addRow("导航栏颜色:", self.menubar_color_btn)
        
        self.reset_theme_btn = QPushButton("重置为默认主题")
        self.reset_theme_btn.clicked.connect(self.reset_theme)
        theme_layout.addRow(self.reset_theme_btn)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # 自动保存组
        save_group = QGroupBox("自动保存设置")
        save_layout = QFormLayout()
        
        self.auto_save_checkbox = QPushButton("启用自动保存")
        self.auto_save_checkbox.setCheckable(True)
        self.auto_save_checkbox.clicked.connect(self.toggle_auto_save)
        
        self.save_interval_spin = QSpinBox()
        self.save_interval_spin.setRange(1, 60)
        self.save_interval_spin.setSuffix(" 分钟")
        self.save_interval_spin.valueChanged.connect(self.update_save_interval)
        
        save_layout.addRow("自动保存:", self.auto_save_checkbox)
        save_layout.addRow("保存间隔:", self.save_interval_spin)
        
        save_group.setLayout(save_layout)
        layout.addWidget(save_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_settings(self):
        # 加载颜色设置
        self.primary_color = self.settings.value("theme/primary", QColor(48, 167, 69))
        self.secondary_color = self.settings.value("theme/secondary", QColor(3, 102, 214))
        self.text_color = self.settings.value("theme/text", QColor(0, 0, 0))
        self.menubar_color = self.settings.value("theme/menubar", QColor(0, 0, 0))  # 默认黑色
        
        # 加载自动保存设置
        auto_save = self.settings.value("auto_save/enabled", False, type=bool)
        self.auto_save_checkbox.setChecked(auto_save)
        self.auto_save_checkbox.setText("启用自动保存" if auto_save else "禁用自动保存")
        
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
        self.auto_save_checkbox.setText("启用自动保存" if checked else "禁用自动保存")
    
    def update_save_interval(self, value):
        pass  # 值改变时自动处理
    
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
        
        QMessageBox.information(self, "成功", "设置已保存")
        self.close()

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("使用帮助")
        self.setGeometry(300, 300, 800, 600)
        
        layout = QVBoxLayout()
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
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
        
        <div style="margin-top: 30px; padding: 15px; background-color: #f6f8fa; border-radius: 5px;">
            <h3 style="color: #0366d6;">常见问题</h3>
            <p><strong>Q: 为什么我的上传失败了？</strong></p>
            <p>A: 请检查您的令牌是否有效、仓库名称是否正确，以及网络连接是否正常。</p>
            
            <p><strong>Q: 我可以上传多大的文件？</strong></p>
            <p>A: GitHub 限制单个文件不超过 100MB，仓库总大小不超过 1GB（免费账户）。</p>
        </div>
        
        <p style="color: #586069; font-style: italic; margin-top: 20px;">版本 0.5 | 如有问题，请联系开发者。</p>
        """)
        
        close_button = QPushButton("关闭帮助")
        close_button.setStyleSheet("""
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
        close_button.clicked.connect(self.close)
        
        layout.addWidget(help_text)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

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
        self.label = QLabel("拖拽文件或文件夹到这里")
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
                self.parent.statusBar().showMessage(f"已选择文件夹: {path}", 3000)
            else:
                folder = os.path.dirname(path)
                self.parent.folder_path.setText(folder)
                self.parent.statusBar().showMessage(f"已选择文件所在文件夹: {folder}", 3000)
        event.acceptProposedAction()

class GitHubUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub 自动上传工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化设置
        self.settings = QSettings("GitHubUploader", "AppSettings")
        self.auto_save_timer = QTimer()
        self.last_save_time = None
        
        # 初始化UI组件
        self.token_input = QLineEdit()
        self.repo_input = QLineEdit()
        self.folder_path = QLineEdit()
        self.commit_input = QLineEdit()
        self.log_output = QTextEdit()
        
        self.initUI()
        self.load_settings()
        self.setup_auto_save()
        
        self.repo = None
        self.gh = None
    
    def initUI(self):
        # 创建菜单栏
        self.createMenuBar()
        
        # 创建状态栏
        self.statusBar().showMessage("准备就绪")
        
        # 主窗口部件
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # 拖拽区域
        self.drop_area = DropArea(self)
        main_layout.addWidget(self.drop_area)
        
        # GitHub 令牌输入
        self.token_label = QLabel("GitHub 个人访问令牌:")
        self.token_input.setPlaceholderText("输入您的 GitHub 个人访问令牌")
        self.token_input.setMinimumHeight(35)
        main_layout.addWidget(self.token_label)
        main_layout.addWidget(self.token_input)
        
        # 仓库信息
        self.repo_label = QLabel("GitHub 仓库 (格式: 用户名/仓库名):")
        self.repo_input.setPlaceholderText("例如: yourusername/yourrepo")
        self.repo_input.setMinimumHeight(35)
        main_layout.addWidget(self.repo_label)
        main_layout.addWidget(self.repo_input)
        
        # 本地文件夹选择
        self.folder_label = QLabel("本地文件夹:")
        self.folder_path.setReadOnly(True)
        self.folder_path.setMinimumHeight(35)
        
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path)
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.setMinimumHeight(35)
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_button)
        
        main_layout.addWidget(self.folder_label)
        main_layout.addLayout(folder_layout)
        
        # 提交信息
        self.commit_label = QLabel("提交信息:")
        self.commit_input.setPlaceholderText("输入提交信息")
        self.commit_input.setMinimumHeight(35)
        main_layout.addWidget(self.commit_label)
        main_layout.addWidget(self.commit_input)
        
        # 操作按钮
        self.upload_button = QPushButton("上传到 GitHub")
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
        main_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        
        # 日志输出
        self.log_label = QLabel("操作日志:")
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(300)
        main_layout.addWidget(self.log_label)
        main_layout.addWidget(self.log_output)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def createMenuBar(self):
        self.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #000000;
                color: white;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #555;
            }
            QMenuBar::item:pressed {
                background-color: #777;
            }
        """)
        
        menuBar = self.menuBar()
        
        # 文件菜单
        fileMenu = menuBar.addMenu("文件")
        
        saveAction = QAction("保存设置", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("保存当前设置")
        saveAction.triggered.connect(self.save_settings)
        fileMenu.addAction(saveAction)
        
        exitAction = QAction("退出", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("退出程序")
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        # 工具菜单
        toolMenu = menuBar.addMenu("工具")
        
        settingsAction = QAction("设置", self)
        settingsAction.setStatusTip("更改应用程序设置")
        settingsAction.triggered.connect(self.show_settings)
        toolMenu.addAction(settingsAction)
        
        clearLogAction = QAction("清除日志", self)
        clearLogAction.setStatusTip("清除操作日志")
        clearLogAction.triggered.connect(self.clear_log)
        toolMenu.addAction(clearLogAction)
        
        # 帮助菜单
        helpMenu = menuBar.addMenu("帮助")
        
        helpAction = QAction("使用帮助", self)
        helpAction.setShortcut("F1")
        helpAction.setStatusTip("显示使用帮助")
        helpAction.triggered.connect(self.show_help)
        helpMenu.addAction(helpAction)
        
        aboutAction = QAction("关于", self)
        aboutAction.setStatusTip("关于此程序")
        aboutAction.triggered.connect(self.show_about)
        helpMenu.addAction(aboutAction)
    
    def save_settings(self):
        """保存当前设置"""
        try:
            # 保存当前状态 (令牌、仓库路径等)
            settings_to_save = {
                "token": self.token_input.text(),
                "repo_path": self.repo_input.text(),
                "local_path": self.folder_path.text(),
                "last_updated": datetime.now().isoformat()
            }
            
            self.settings.setValue("app_state", json.dumps(settings_to_save))
            self.statusBar().showMessage("设置已保存", 3000)
            return True
        except Exception as e:
            self.log_message(f"保存设置时出错: {str(e)}")
            return False
    
    def clear_log(self):
        """清除日志内容"""
        self.log_output.clear()
        self.statusBar().showMessage("日志已清除", 3000)
    
    def show_about(self):
        QMessageBox.about(self, "关于 GitHub 自动上传工具",
                         "<b>GitHub 自动上传工具 v0.5</b><br><br>"
                         "一个简单的图形界面工具，用于将本地文件上传到 GitHub 仓库。<br><br>"
                         "使用 Python 和 PyQt5 开发<br>"
                         "© 2023 开发者")
    
    def show_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()
    
    def show_help(self):
        help_dialog = HelpDialog()
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
        # 应用主题颜色到UI
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
        # 停止现有定时器
        self.auto_save_timer.stop()
        
        # 检查是否启用自动保存
        auto_save_enabled = self.settings.value("auto_save/enabled", False, type=bool)
        if auto_save_enabled:
            interval_minutes = self.settings.value("auto_save/interval", 5, type=int)
            interval_ms = interval_minutes * 60 * 1000  # 转换为毫秒
            
            self.auto_save_timer.timeout.connect(self.auto_save)
            self.auto_save_timer.start(interval_ms)
            self.statusBar().showMessage(f"自动保存已启用，每 {interval_minutes} 分钟保存一次", 5000)
    
    def auto_save(self):
        """自动保存设置"""
        self.save_settings()
        self.last_save_time = datetime.now()
        self.statusBar().showMessage(f"设置已自动保存 - {self.last_save_time.strftime('%H:%M:%S')}", 3000)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.folder_path.setText(folder)
            self.statusBar().showMessage(f"已选择文件夹: {folder}", 3000)
    
    def log_message(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()  # 自动滚动到底部
    
    def upload_to_github(self):
        # 获取输入值
        token = self.token_input.text().strip()
        repo_path = self.repo_input.text().strip()
        local_path = self.folder_path.text().strip()
        commit_msg = self.commit_input.text().strip()
        
        if not all([token, repo_path, local_path, commit_msg]):
            QMessageBox.warning(self, "警告", "请填写所有字段")
            self.statusBar().showMessage("错误: 请填写所有字段", 5000)
            return
        
        try:
            self.statusBar().showMessage("开始上传过程...")
            self.log_message("开始上传过程...")
            
            # 初始化 GitHub 连接
            self.gh = Github(token)
            self.log_message("已连接到 GitHub")
            
            # 检查本地仓库是否存在
            git_folder = os.path.join(local_path, '.git')
            if os.path.exists(git_folder):
                self.log_message("找到现有的 Git 仓库")
                repo = Repo(local_path)
            else:
                self.log_message("初始化新的 Git 仓库")
                repo = Repo.init(local_path)
                self.log_message("Git 仓库初始化完成")
            
            # 添加所有文件
            repo.git.add('--all')
            self.log_message("已添加所有文件到暂存区")
            
            # 提交更改
            repo.index.commit(commit_msg)
            self.log_message(f"已提交更改: {commit_msg}")
            
            # 获取远程仓库
            remote_name = 'origin'
            remote_url = f"https://{token}@github.com/{repo_path}.git"
            
            if remote_name in repo.remotes:
                remote = repo.remotes[remote_name]
                remote.set_url(remote_url)
                self.log_message("更新了远程仓库 URL")
            else:
                remote = repo.create_remote(remote_name, remote_url)
                self.log_message("创建了新的远程仓库")
            
            # 推送更改
            self.log_message("正在推送更改到 GitHub...")
            self.statusBar().showMessage("正在推送更改到 GitHub...")
            remote.push().raise_if_error()
            self.log_message("推送成功完成!")
            
            QMessageBox.information(self, "成功", "文件已成功上传到 GitHub 仓库")
            self.statusBar().showMessage("上传成功完成!", 5000)
            
        except GitCommandError as e:
            error_msg = f"Git 错误: {str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
            self.statusBar().showMessage("上传失败: Git 错误", 5000)
        except GithubException as e:
            error_msg = f"GitHub API 错误: {str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
            self.statusBar().showMessage("上传失败: GitHub 错误", 5000)
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            self.log_message(error_msg)
            QMessageBox.critical(self, "错误", error_msg)
            self.statusBar().showMessage("上传失败: 未知错误", 5000)
    
    def closeEvent(self, event):
        # 关闭前自动保存
        if self.settings.value("auto_save/enabled", False, type=bool):
            self.save_settings()
        
        # 保存窗口大小和位置
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
