### **README.md**

```markdown
# Mouse Click Recorder and Replayer

A Python application to record mouse clicks, save them to a script, and replay them. It includes a graphical user interface (GUI) built with `tkinter` and supports hotkey actions for convenience.

---

## **Features**

- **Record Mouse Clicks**: Save mouse click actions, including coordinates and button used, to a script file (`saved-script.txt`).
- **Replay Actions**: Replay recorded mouse clicks automatically.
- **Capture Screenshots**: Take screenshots of the screen when clicks are recorded.
- **Hotkey Support**: Use `CTRL+F2` to replay the recorded script without accessing the GUI.
- **Graphical Interface**: Start, stop, or replay actions through an easy-to-use GUI.

---

## **Project Structure**

```plaintext
src/
├── main.py                # Entry point of the application
├── ui/
│   └── gui.py             # Handles the graphical user interface
├── core/
│   ├── script.py          # Logic for recording and replaying mouse clicks
│   └── hotkey.py          # Manages hotkey actions
├── utils/
│   ├── logger.py          # Centralized logging functionality
│   └── config.py          # Configuration for paths and constants
data/
├── saved-script.txt       # File where recorded clicks are saved
└── temp-print/            # Directory for storing screenshots
log.txt                    # Logs application actions
requirements.txt           # Dependencies for the project
README.md                  # Project documentation
```

---

## **Installation**

### **Requirements**
- Python 3.8 or higher
- Pip (Python package installer)

### **Dependencies**
Install the required dependencies with:
```bash
pip install -r requirements.txt
```

---

## **Usage**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Run the Application**:
   Start the application using the `main.py` script:
   ```bash
   python src/main.py
   ```

3. **GUI Operations**:
   - **Iniciar Captura**: Start recording mouse clicks.
   - **Parar Captura**: Stop recording mouse clicks.
   - **Rodar Script**: Replay the recorded clicks.

4. **Hotkey**:
   - Press `CTRL+F2` to execute the recorded script without opening the GUI.

---

## **How It Works**

### **Recording Mouse Clicks**:
- Mouse clicks are recorded and saved in the file `data/saved-script.txt`.
- Each entry includes:
  - `x` and `y` coordinates of the click.
  - The button used (`left`, `right`, etc.).

### **Replaying Mouse Clicks**:
- Reads the recorded clicks from `data/saved-script.txt`.
- Automates the clicks using `pyautogui`.

### **Screenshots**:
- Each mouse click triggers a screenshot, saved in the `data/temp-print/` directory.

---

## **Customization**

- Modify paths or constants in `utils/config.py`:
  ```python
  BASE_DIR = ...
  LOG_FILE = ...
  SCRIPT_FILE = ...
  TEMP_FOLDER = ...
  ```

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## **Contributing**

Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

---

## **Author**

Developed by **notNilton**.
```
