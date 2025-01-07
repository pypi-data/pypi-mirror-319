import subprocess
import os

def run():
    # Launch the Streamlit app.
    
    os.environ["STREAMLIT_EMAIL_ADDRESS"] = ""

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    print(app_path)
    
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}")
    except FileNotFoundError:
        print("Streamlit is not installed or not available in the current environment.")

