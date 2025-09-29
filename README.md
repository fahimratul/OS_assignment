# Installation Guide for Flowbit

Follow these steps to install Flowbit on your system by downloading the ZIP file from GitHub:

## For Windows Users

## 1. Download the ZIP File
- Go to the [Flowbit GitHub repository](https://github.com/fahimratul/OS_assignment).
- Click the green **Code** button.
- Select **Download ZIP**.

## 2. Unzip the Downloaded File
- Locate the downloaded ZIP file (usually in your Downloads folder).
- Right-click the ZIP file and select **Extract All**.
- Choose a destination folder and click **Extract**.

## 3. Build the Executable
- Open the extracted folder.
- Double-click `build_exe.bat` to run the batch file.
- Wait for the process to complete; this will create the executable in the `dist` folder.

## 4. Run the Application
- ✅ Open the `dist` folder inside the extracted directory.
- ✅ Double-click `flowbit.exe` to start the application.

## For Linux Users

### 1. Download the ZIP File
- Go to the [Flowbit GitHub repository](https://github.com/fahimratul/OS_assignment).
- Click the green **Code** button.
- Select **Download ZIP**.

### 2. Extract the Downloaded File
Open a terminal and navigate to your Downloads folder:
```bash
cd ~/Downloads
unzip OS_assignment-main.zip
cd OS_assignment-main
```

### 3. Make Scripts Executable
Make the shell scripts executable:
```bash
chmod +x run_app.sh
chmod +x build_binary.sh
```

### 4. Install Prerequisites (if needed)
Ensure you have Python 3 and pip installed:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip python3-venv
# or for older versions: sudo yum install python3 python3-pip python3-venv
```

### 5. Build the Binary
Run the build script:
```bash
./build_binary.sh
```
This will create the executable in the `dist` folder.

### 6. Run the Application
- ✅ Navigate to the `dist` folder: `cd dist`
- ✅ Run the binary: `./flowbit`

### Alternative: Run Python Script Directly
If you prefer to run the Python script directly:
```bash
./run_app.sh
```

## Happy Coding. Thanks for using our app. ❤️😊 

## Additional Notes
- **Windows users**: If you encounter issues, ensure you have Python installed and added to your PATH.
- **Linux users**: Make sure you have Python 3.6+ installed. Most modern Linux distributions include it by default.
- Refer to the documentation for further usage instructions.
- For help, visit the Issues page on GitHub. 

