<div align="center">
  <img src="https://raw.githubusercontent.com/diced/zipline/trunk/public/zipline_small.png"/>
  
A friendly virtual assistant, in purpose to helping Windows user automate their task

![Stars](https://img.shields.io/github/stars/TofuAI/MaryAssist?logo=github&style=flat)
![Version](https://img.shields.io/github/package-json/v/TofuAI/MaryAssist?logo=git&logoColor=white&style=flat)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/TofuAI/MaryAssist/trunk?logo=git&logoColor=white&style=flat)
![Build](https://img.shields.io/github/actions/workflow/status/TofuAI/MaryAssist/build.yml?logo=github&style=flat&branch=trunk)

</div>

***

## What is MaryAssistant?
MaryAssistant is a user-friendly virtual assistant designed to help Windows users automate their daily tasks with just a simple voice command. Developed in Python by [TofuAI](https://github.com/TofuAI) and [akk1to.dev](https://github.com/akk1to), this innovative project integrates various Python libraries and dependencies to create a seamless, efficient, and intelligent assistant capable of enhancing productivity and simplifying routine operations.

With MaryAssistant, users can expect a hands-free experience in managing their system functions, running applications, searching the web, setting reminders, and much more—all through intuitive voice commands. Whether you're looking to streamline your workflow, improve accessibility, or simply enjoy the convenience of voice-controlled automation, MaryAssistant is built to cater to your needs.

Currently, the project is still under active development, with continuous improvements, new features, and optimizations being added. The developers are committed to refining and expanding the assistant’s capabilities to ensure it delivers the best possible experience.

To stay updated with the latest features, enhancements, and official releases, consider following the project on GitHub. Your support means a lot! Simply click on the "Star this repository" button to show appreciation and receive notifications about updates. Your feedback and engagement will help shape the future of MaryAssistant, making it even more powerful and efficient. Stay tuned for exciting developments! 

> [!WARNING]
> Currently this project is still in working, so please let us know any bug that you found through "Issues" section! It will be a great help to us!

## Features
Since the project is still in development, we currently offer only a few basic features, such as:
- Open all applications on the Windows operating system, such as Google Chrome, Microsoft Word, Microsoft Excel, Microsoft PowerPoint, Zalo, YouTube, and more.
- Perform searches using Google.
- Play, pause, and enable subtitles on YouTube.
- Close open browser tabs one by one.
- Display the current system date and time.
- Perform basic mathematical calculations, including addition, subtraction, multiplication, and division.
- Put the computer into hibernation mode.
- Shut down or restart the computer.

> [!Note]
> Refer to the [Development Roadmap](https://github.com/TofuAI) for upcoming feature updates and enhancements.

## Future enhancement

- [ ] Integrating an advanced LLM model, such as ChatGPT 2.0, as the core assistant in future updates.
- [ ] Enable users to automate tasks in their web browser.
- [ ] Improve response speed for a smoother and more efficient user experience.
- [ ] Redesign the UX/UI for a more user-friendly and intuitive interface.

## Installation Guide
### Option 1: Install from Releases
Go to the [releases](https://gitthub.com) page and download the latest version to your computer. Once the download is complete, run the .exe file to install the application.

When launching MaryAssistant for the first time, please allow 1-2 minutes for it to set up the necessary environment on your computer. Once the assistant window appears, it means that MaryAssistant is ready to use!

To activate the assistant, simply say "Mary Mary" or click on the Microphone icon.

> [!WARNING]
> Our assistant's executable file is completely safe and does not contain any malware or harmful scripts that could affect your system. For more details, check the latest security scan results in this [VirusTotal scan report - Newest release (11/2/2025)](https://google.com).
### Option 2: Build from source
#### Prerequisities
- Python 3.11 or higher
- Git (for cloning the repository)
- An application to manage Python environment (we recommend using [uv](https://docs.astral.sh/uv) for managing the Python environments.
#### Step 1: Clone the repository
```bash
git clone https://github.com/TofuAI/MaryAssit.git
cd MaryAssit
```
#### Step 2: Set up the environment
Using uv (recommended):
```bash
uv venv --python 3.11
```

Active the virtual environment:
- Windows (Command Prompt):
```cmd
.venv\Scripts\activate
```
- Windows (Powershell):
```powershell
.\.venv\Scripts\Activate.ps1
```
- MacOS/Linux:
```bash
source .venv/bin/activate
```
#### Step 3: Install all necessary dependencies and libraries
Install Python packages:
```bash
uv pip install -r requirements.txt
```

Install Playwright (optional, for debug "Browser Automate" feature):
```bash
playwright install
```

#### Step 4: Configure environment
1. Create a copy of the example environment file:
- Windows (Command Prompt):
```cmd
copy .env.example .env
```
- MacOS/Linux/Windows (Powershell):
```bash
cp .env.example .env
```
2. Open `.env` in your preferred text editor and add your API keys and other settings

#### Step 5: Build source code & Run
Just power up the assistant through this command:
```bash
python MaryAssist.py
```
