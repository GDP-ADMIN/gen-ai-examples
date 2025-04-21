# Setting Python Interpreter Path in VSCode IDE

This guide explains how to configure the correct Python interpreter path in Visual Studio Code when working with the GenAI examples repository.


## Step-by-Step Instructions

1. **Run the setup script first**
   
   Before configuring your interpreter, ensure you've run the appropriate setup script for your project:
   ```bash
   ./local-start.sh  # For Linux, macOS, or Windows WSL
   ```
   or
   ```powershell
   .\local-start.bat  # For Windows
   ```

2. **Identify the Python interpreter path**
   
   After running the setup script, look for the log message that shows the Python interpreter path:
   ```
   Getting python interpreter path for use in IDE...
   /path/to/your/virtualenv/bin/python
   ```
   Copy this path. It will look similar to:
   - Linux/macOS: `/home/<username>/.cache/pypoetry/virtualenvs/example-ob4i36ef-py3.12/bin/python`
   - Windows: `C:\Users\<username>\AppData\Local\pypoetry\Cache\virtualenvs\example-ob4i36ef-py3.12\Scripts\python.exe`

3. **Open your project in VSCode**

   You might notice import errors (squiggly lines) when opening Python files before setting up the interpreter:

   <img width="579" alt="image" src="https://github.com/user-attachments/assets/72979f2b-16b1-4265-8d30-dfab96cd6a61" />

4. **Open VSCode Command Palette**
   
   - On macOS: Press `⌘+Shift+P`
   - On Linux/Windows: Press `Ctrl+Shift+P`

   <img width="493" alt="image" src="https://github.com/user-attachments/assets/2e463386-3424-45b0-8e2e-b9b7adab21b0" />

5. Select `Enter interpreter path...`

6. Paste the previously copied path from the console and press enter.



   <img width="501" alt="image" src="https://github.com/user-attachments/assets/3fc2db14-d8e5-45fd-9f74-e7f59cf84abc" />


8. **Verify the configuration**
   
   Once set, you should see the selected interpreter displayed in the bottom status bar of VSCode. It should show something like `Python 3.11.x ('.venv')` or similar.

    <img width="203" alt="image" src="https://github.com/user-attachments/assets/3dffba0d-8cd7-4577-880b-ea74d0080b7c" />

   The squiggly lines under import statements should disappear. You can hover over import statements to see that they are correctly resolved.

    <img width="497" alt="image" src="https://github.com/user-attachments/assets/342841b3-0205-4b0b-869f-ea7d959ad1cd" />

## Common Issues and Troubleshooting

- **Import errors persist**: Try reloading the VSCode window (Command Palette > `Developer: Reload Window`)
- **Path not found**: Ensure you've copied the exact path from the console output
 