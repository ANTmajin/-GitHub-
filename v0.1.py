import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox)
from git import Repo, GitCommandError
from github import Github, GithubException

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
        layout = QVBoxLayout()
        
        # GitHub 令牌输入
        self.token_label = QLabel("GitHub 个人访问令牌:")
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("输入您的 GitHub 个人访问令牌")
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_input)
        
        # 仓库信息
        self.repo_label = QLabel("GitHub 仓库 (格式: 用户名/仓库名):")
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("例如: yourusername/yourrepo")
        layout.addWidget(self.repo_label)
        layout.addWidget(self.repo_input)
        
        # 本地文件夹选择
        self.folder_label = QLabel("本地文件夹:")
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_path)
        layout.addWidget(self.browse_button)
        
        # 提交信息
        self.commit_label = QLabel("提交信息:")
        self.commit_input = QLineEdit()
        self.commit_input.setPlaceholderText("输入提交信息")
        layout.addWidget(self.commit_label)
        layout.addWidget(self.commit_input)
        
        # 操作按钮
        self.upload_button = QPushButton("上传到 GitHub")
        self.upload_button.clicked.connect(self.upload_to_github)
        layout.addWidget(self.upload_button)
        
        # 日志输出
        self.log_label = QLabel("操作日志:")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_label)
        layout.addWidget(self.log_output)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
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
