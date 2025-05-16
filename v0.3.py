import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox,
                             QHBoxLayout, QDialog, QMenuBar, QMenu, QStatusBar, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from git import Repo, GitCommandError
from github import Github, GithubException

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("使用帮助")
        self.setGeometry(300, 300, 800, 600)  # 增大帮助窗口尺寸
        
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
            <li>建议定期更新您的访问令牌</li>
        </ul>
        
        <div style="margin-top: 30px; padding: 15px; background-color: #f6f8fa; border-radius: 5px;">
            <h3 style="color: #0366d6;">常见问题</h3>
            <p><strong>Q: 为什么我的上传失败了？</strong></p>
            <p>A: 请检查您的令牌是否有效、仓库名称是否正确，以及网络连接是否正常。</p>
            
            <p><strong>Q: 我可以上传多大的文件？</strong></p>
            <p>A: GitHub 限制单个文件不超过 100MB，仓库总大小不超过 1GB（免费账户）。</p>
        </div>
        
        <p style="color: #586069; font-style: italic; margin-top: 20px;">版本 1.0 | 如有问题，请联系开发者。</p>
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

class GitHubUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub 自动上传工具")
        self.setGeometry(100, 100, 1200, 800)  # 增大主窗口尺寸
        
        self.initUI()
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
        
        # GitHub 令牌输入
        self.token_label = QLabel("GitHub 个人访问令牌:")
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("输入您的 GitHub 个人访问令牌")
        self.token_input.setMinimumHeight(35)
        main_layout.addWidget(self.token_label)
        main_layout.addWidget(self.token_input)
        
        # 仓库信息
        self.repo_label = QLabel("GitHub 仓库 (格式: 用户名/仓库名):")
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("例如: yourusername/yourrepo")
        self.repo_input.setMinimumHeight(35)
        main_layout.addWidget(self.repo_label)
        main_layout.addWidget(self.repo_input)
        
        # 本地文件夹选择
        self.folder_label = QLabel("本地文件夹:")
        self.folder_path = QLineEdit()
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
        self.commit_input = QLineEdit()
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
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(300)  # 增大日志区域高度
        main_layout.addWidget(self.log_label)
        main_layout.addWidget(self.log_output)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def createMenuBar(self):
        menuBar = self.menuBar()
        
        # 文件菜单
        fileMenu = menuBar.addMenu("文件")
        
        exitAction = QAction("退出", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("退出程序")
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        
        # 工具菜单
        toolMenu = menuBar.addMenu("工具")
        
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
    
    def show_about(self):
        QMessageBox.about(self, "关于 GitHub 自动上传工具",
                         "<b>GitHub 自动上传工具 v1.0</b><br><br>"
                         "一个简单的图形界面工具，用于将本地文件上传到 GitHub 仓库。<br><br>"
                         "使用 Python 和 PyQt5 开发<br>"
                         "© 2023 开发者")
    
    def clear_log(self):
        self.log_output.clear()
        self.statusBar().showMessage("日志已清除", 3000)
    
    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用 Fusion 样式，看起来更现代
    
    # 设置应用程序图标 (如果有的话)
    # app.setWindowIcon(QIcon('icon.png'))
    
    window = GitHubUploader()
    window.show()
    sys.exit(app.exec_())
