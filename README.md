# GitHub upload tool/GitHub自动保存工具

### 这是一个图形化界面操作自动上传GitHub程序，腐竹的好工具！
### (The English translation is at the back.)

------------
### 注意此协议为GNU General Public License v2.0
### 要求衍生作品也必须开源

------------
功能概述

1. 图形化界面操作

2. 连接 GitHub 账户

3. 选择/拖拽本地文件夹

4. 自动初始化 Git 仓库（如需要）

5. 提交更改并推送到 GitHub

6. 定时保存指定目录

------------
如何操作：
GitHub 自动上传工具使用指南 
1. 准备工作 
在使用本工具前，您需要: 
拥有一个 GitHub 账号 
在 GitHub 上创建好仓库 
生成个人访问令牌 (PAT) 
2. 获取个人访问令牌 
按照以下步骤获取令牌: 
登录 GitHub 账户 
进入 Settings > Developer settings > Personal access tokens 
点击 "Generate new token" 
为令牌命名 
勾选 "repo" 权限 
点击 "Generate token" 按钮 
复制生成的令牌 (这是您唯一一次能看到它的机会) 
3. 使用本工具 
操作步骤: 
在 "GitHub 个人访问令牌" 字段粘贴您的令牌 
在 "GitHub 仓库" 字段输入仓库名称 (格式: 用户名/仓库名) 
点击 "浏览..." 按钮选择本地文件夹 
在 "提交信息" 字段输入有意义的描述 
点击 "上传到 GitHub" 按钮 
4. 注意事项 
令牌相当于密码，请妥善保管 
如果文件夹不是 Git 仓库，工具会自动初始化 
上传大量文件可能需要较长时间 
确保网络连接正常 
如有问题，请联系开发者。

------------

### 给开发者的话:
1.该语言由python开发，这个程序将使用PyQt5作为界面框架，GitPython库来处理Git操作。
2.安装依赖:pip install PyQt5 GitPython PyGithub

------------

### Please note that the author used machine translation for English, and the English format has been manually edited and may contain errors.
### This is an automated GitHub upload program with a graphical interface, a great tool for enthusiasts!

------------
### Note that this agreement is under the GNU General Public License v2.0
### Derivative works must also be open source

------------
Function Overview

1. Graphical interface operation

2. Connect GitHub account

3. Select/drag and drop local folder
   
4. Automatically initialize Git repository (if needed)
   
5. Commit changes and push to GitHub
    
6. Scheduled save of specified directory
    
------------
How to operate:
GitHub Automatic Upload Tool User Guide 
1. Preparation  Before using this tool, you need:
A GitHub account
Create a repository on GitHub
Generate a personal access token (PAT)
2. Obtain a personal access token
Follow these steps to obtain the token:
Log in to your GitHub account
Go to Settings > Developer settings > Personal access tokens
Click "Generate new token"
Name the token
Check the "repo" permission
Click the "Generate token" button
Copy the generated token (this is the only time you'll see it)
Use this tool
Operation steps:
Paste your token in the "GitHub Personal Access Token" field
Enter the repository name in the "GitHub Repository" field (format: username/repository_name)
Click the "Browse..." button to select the local folder
Enter a meaningful description in the "Commit Message" field
Click the "Upload to GitHub" button
8. Notes
The token is like a password, please keep it safe
If the folder is not a Git repository, the tool will automatically initialize it
Uploading a large number of files may take a long time
Ensure the network connection is stable
If there are any issues, please contact the developer.

------------

### A word to developers:
1. This language is developed by python, and this program will use PyQt5 as the interface framework, and GitPython library handle Git operations.
2. Install dependencies: pip install PyQt5 GitPython PyGithub
