import os
import subprocess
import sys
from flask import Flask, Response

app = Flask(__name__)

# Determine the project root directory dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@app.route("/dynasty_data")
def get_dynasty_data():
    """
    Fetches the latest dynasty market data and returns it as a CSV string.
    """
    # Construct the path to the virtual environment activation script
    if sys.platform == "win32":
        activate_script = os.path.join(PROJECT_ROOT, "venv", "Scripts", "activate.bat")
        command_prefix = f'call "{activate_script}" &&'
    else:
        activate_script = os.path.join(PROJECT_ROOT, "venv", "bin", "activate")
        command_prefix = f'source "{activate_script}" &&'

    # Construct the command to run the data fetcher script
    data_fetcher_script = os.path.join(PROJECT_ROOT, "scripts", "data_fetcher_for_gem.py")
    full_command = f'{command_prefix} python "{data_fetcher_script}"'

    try:
        # Execute the command and capture stdout
        process = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            cwd=PROJECT_ROOT # Run the command from the project root
        )
        return Response(process.stdout, mimetype="text/csv")
    except subprocess.CalledProcessError as e:
        return Response(f"Error fetching data: {e.stderr}", status=500, mimetype="text/plain")
    except Exception as e:
        return Response(f"An unexpected error occurred: {str(e)}", status=500, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)