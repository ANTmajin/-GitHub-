import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox,
                             QHBoxLayout, QDialog)
from PyQt5.QtCore import Qt
from git import Repo, GitCommandError
from github import Github, GithubException

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("使用帮助")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h1>GitHub 自动上传工具使用指南</h1>
        
        <h2>1. 准备工作</h2>
        <p>在使用本工具前，您需要:</p>
        <ul>
            <li>拥有一个 GitHub 账号</li>
            <li>在 GitHub 上创建好仓库</li>
            <li>生成个人访问令牌 (PAT)</li>
        </ul>
        
        <h2>2. 获取个人访问令牌</h2>
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
        
        <h2>3. 使用本工具</h2>
        <p>操作步骤:</p>
        <ol>
            <li>在 "GitHub 个人访问令牌" 字段粘贴您的令牌</li>
            <li>在 "GitHub 仓库" 字段输入仓库名称 (格式: 用户名/仓库名)</li>
            <li>点击 "浏览..." 按钮选择本地文件夹</li>
            <li>在 "提交信息" 字段输入有意义的描述</li>
            <li>点击 "上传到 GitHub" 按钮</li>
        </ol>
        
        <h2>4. 注意事项</h2>
        <ul>
            <li>令牌相当于密码，请妥善保管</li>
            <li>如果文件夹不是 Git 仓库，工具会自动初始化</li>
            <li>上传大量文件可能需要较长时间</li>
            <li>确保网络连接正常</li>
        </ul>
        
        <p style="color: #666; font-style: italic;">如有问题，请联系开发者。</p>
        """)
        
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        
        layout.addWidget(help_text)
        layout.addWidget(close_button)
        self.setLayout(layout)

class GitHubUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub 自动上传工具")
        self.setGeometry(100, 100, 600, 400)
        
        self.initUI()
        self.repo = None
        self.gh = None
        
    def initUI(self):
        # 主窗口部件
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # 顶部工具栏布局
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addStretch()
        
        # 帮助按钮
        self.help_button = QPushButton("帮助")
        self.help_button.setFixedWidth(80)
        self.help_button.clicked.connect(self.show_help)
        toolbar_layout.addWidget(self.help_button)
        
        main_layout.addLayout(toolbar_layout)
        
        # GitHub 令牌输入
        self.token_label = QLabel("GitHub 个人访问令牌:")
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("输入您的 GitHub 个人访问令牌")
        main_layout.addWidget(self.token_label)
        main_layout.addWidget(self.token_input)
        
        # 仓库信息
        self.repo_label = QLabel("GitHub 仓库 (格式: 用户名/仓库名):")
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("例如: yourusername/yourrepo")
        main_layout.addWidget(self.repo_label)
        main_layout.addWidget(self.repo_input)
        
        # 本地文件夹选择
        self.folder_label = QLabel("本地文件夹:")
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self.browse_folder)
        main_layout.addWidget(self.folder_label)
        main_layout.addWidget(self.folder_path)
        main_layout.addWidget(self.browse_button)
        
        # 提交信息
        self.commit_label = QLabel("提交信息:")
        self.commit_input = QLineEdit()
        self.commit_input.setPlaceholderText("输入提交信息")
        main_layout.addWidget(self.commit_label)
        main_layout.addWidget(self.commit_input)
        
        # 操作按钮
        self.upload_button = QPushButton("上传到 GitHub")
        self.upload_button.clicked.connect(self.upload_to_github)
        main_layout.addWidget(self.upload_button)
        
        # 日志输出
        self.log_label = QLabel("操作日志:")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_label)
        main_layout.addWidget(self.log_output)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.folder_path.setText(folder)
    
    def log_message(self, message):
        self.log_output.append(message)
    
    def upload_to_github(self):
        # 获取输入值
        token = self.token_input.text().strip()
        repo_path = self.repo_input.text().strip()
        local_path = self.folder_path.text().strip()
        commit_msg = self.commit_input.text().strip()
        
        if not all([token, repo_path, local_path, commit_msg]):
            QMessageBox.warning(self, "警告", "请填写所有字段")
            return
        
        try:
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
            remote.push().raise_if_error()
            self.log_message("推送成功完成!")
            
            QMessageBox.information(self, "成功", "文件已成功上传到 GitHub 仓库")
            
        except GitCommandError as e:
            self.log_message(f"Git 错误: {str(e)}")
            QMessageBox.critical(self, "错误", f"Git 操作出错: {str(e)}")
        except GithubException as e:
            self.log_message(f"GitHub API 错误: {str(e)}")
            QMessageBox.critical(self, "错误", f"GitHub 连接出错: {str(e)}")
        except Exception as e:
            self.log_message(f"未知错误: {str(e)}")
            QMessageBox.critical(self, "错误", f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitHubUploader()
    window.show()
    sys.exit(app.exec_())
