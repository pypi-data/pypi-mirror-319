import subprocess
import os

def run():
    # Launch the Streamlit app.
    import os 
    os.environ["STREAMLIT_EMAIL_ADDRESS"] = ""

    # Streamlit theme settings
    os.environ["STREAMLIT_THEME_PRIMARY_COLOR"] = "#6ac1cb"
    os.environ["STREAMLIT_THEME_BACKGROUND_COLOR"] = "#FFFFFF"
    os.environ["STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR"] = "#e8e8e8"
    os.environ["STREAMLIT_THEME_TEXT_COLOR"] = "#31333F"
    os.environ["STREAMLIT_THEME_FONT"] = "sans serif"

    # Streamlit server settings
    os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "2000"  # Max upload size in MB

    # Streamlit client settings
    os.environ["STREAMLIT_CLIENT_TOOLBAR_MODE"] = "minimal"

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    print(app_path)
    
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}")
    except FileNotFoundError:
        print("Streamlit is not installed or not available in the current environment.")

