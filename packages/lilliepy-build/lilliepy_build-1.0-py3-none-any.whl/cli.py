import os
import time
import typer
import shutil
import requests
import threading
import subprocess
from bs4 import BeautifulSoup
from colorama import Fore, Style

app = typer.Typer()

def _get():
    try:
        html = requests.get("http://127.0.0.1:8000").text
        js = requests.get(f"http://127.0.0.1:8000/_reactpy/assets/index.a1f87a11.js").text
        soup = BeautifulSoup(html, "html.parser")

        script = soup.find("script", src=True)
        if script:
            script["src"] = "./assets/index.a1f87a11.js"

        return soup.prettify(), js, "index.a1f87a11.js"
    
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED + f"Connection Error: {e}" + Style.DIM)
        print(Fore.WHITE + Style.NORMAL)
        raise SystemExit(1)

def _make(output_pathway, static_pathway):
    time.sleep(2)
    html, js, js_name = _get()

    os.makedirs(output_pathway, exist_ok=True)
    os.makedirs(f"{output_pathway}/assets", exist_ok=True)

    with open(f"{output_pathway}/index.html", "w") as file:
        file.write(html)

    shutil.copytree(static_pathway, f"{output_pathway}/assets", dirs_exist_ok=True)

    with open(f"{output_pathway}/assets/{js_name}", "w") as file:
        file.write(js)

    print(Fore.GREEN + "Build completed successfully." + Style.BRIGHT)
    print(Fore.WHITE + Style.NORMAL)

@app.command()
def build(path_to_output: str, path_to_static: str):
    global output_pathway
    output_pathway = os.path.join(os.getcwd(), path_to_output)
    static_pathway = os.path.join(os.getcwd(), path_to_static)

    def start_server():
        dev_run = subprocess.Popen(["python", "lillie.config.py"])
        time.sleep(3)
        dev_run.terminate()

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    _make(output_pathway, static_pathway)

    server_thread.join()

@app.command()
def clean():
    if os.path.exists(output_pathway):
        shutil.rmtree(output_pathway)
        print(Fore.GREEN + "Cleaned the output directory." + Style.BRIGHT)
        print(Fore.WHITE + Style.NORMAL)
    else:
        print(Fore.RED + "Output directory does not exist." + Style.DIM)
        print(Fore.WHITE + Style.NORMAL)

if __name__ == "__main__":
    app()
