##PasswordManager
Desktop and portable Password Manager for Linux, Windows, and OS X
##Version :
1.0
##Features:
1.AES-encryption protects you from hacking</br>
2.Friendly interface
##Requirements:
Python >= 3.3</br>
PyQt4</br>
PyCrypto
##Instalations:
|1. Clone the git repository from GitHub:

    For all users

        git clone https://github.com/YorickPoor/PasswordManager_reinc.git

|2. Open the working directory:

        cd PasswordManager_reinc

|3 ||a.)For testers and developers:
        
        cd "Full Version" or cd Minimal
        python3 Main.py

   ||b.)For end users:
        
        # WARNING : Tested only on Windows XP and Ubuntu 14.04
        #For windows users
            cd Executables/Windows
            Main.exe
        #For linux/unix users
            cd Executables/Unix
            chmod +x Main
            ./Main
        #For OSX users (is that the executable file is compiled)
            cd "Full Version" or cd Minimal
            python3 Main.py
        