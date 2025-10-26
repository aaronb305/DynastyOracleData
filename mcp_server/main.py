import os
import subprocess
import sys
from fastapi import FastAPI, Response

app = FastAPI()

# Determine the project root directory dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@app.get("/dynasty_data", response_class=Response)
async def get_dynasty_data():
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
        return Response(content=process.stdout, media_type="text/csv")
    except subprocess.CalledProcessError as e:
        return Response(content=f"Error fetching data: {e.stderr}", status_code=500, media_type="text/plain")
    except Exception as e:
        return Response(content=f"An unexpected error occurred: {str(e)}", status_code=500, media_type="text/plain")

