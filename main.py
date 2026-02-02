import requests
import glob
from datetime import datetime
import os
from bs4 import BeautifulSoup
from colorama import init, Fore
from win10toast import ToastNotifier  # Windows notifications

# Initialize colorama
init(autoreset=True)
toaster = ToastNotifier()  # Create a toaster object

# Configuration
url = "https://www.atec.pt/cursos-formacao-profissional/calendario-dos-cursos.html"
snapshot_folder = "snapshots_ciberseguranca"

os.makedirs(snapshot_folder, exist_ok=True)

# Fetch page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the Cibersegurança table
def get_ciberseguranca_text(soup):
    tables = soup.find_all("table", class_="listagem_calendario")
    for table in tables:
        if "Cibersegurança" in table.get_text():
            lines = [line.strip() for line in table.get_text(separator="\n").splitlines() if line.strip()]
            return "\n".join(lines)
    return None

current_content = get_ciberseguranca_text(soup)
if not current_content:
    print(Fore.RED + "Cibersegurança course not found on the page.")
    toaster.show_toast("Cibersegurança Monitor", "Course not found on page!", duration=10)
    exit()

# Save snapshot with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
new_file_path = f"{snapshot_folder}/{timestamp}.txt"
with open(new_file_path, "w", encoding="utf-8") as f:
    f.write(current_content)

print(Fore.CYAN + f"Saved snapshot for Cibersegurança course: {new_file_path}")

# Compare with previous snapshot
files = sorted(glob.glob(f"{snapshot_folder}/*.txt"))
if len(files) > 1:
    with open(files[-2], "r", encoding="utf-8") as f:
        old_content = f.read()

    if old_content != current_content:
        print(Fore.YELLOW + "Cibersegurança course page has changed!\n")
        print(Fore.MAGENTA + "--- Previous snapshot ---")
        print(old_content)
        print(Fore.GREEN + "--- Current snapshot ---")
        print(current_content)
        # Show Windows notification
        toaster.show_toast(
            "Cibersegurança Monitor",
            "Cibersegurança course page has changed!",
            duration=10,  # seconds
            threaded=True
        )
    else:
        print(Fore.GREEN + "No changes detected for Cibersegurança course.")
else:
    print(Fore.BLUE + "No previous snapshot to compare with.")
