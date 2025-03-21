import requests
from bs4 import BeautifulSoup
import re
import csv

def load_urls(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def find_google_analytics_tags(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all("script")
        analytics_tags = []

        patterns = {
            "GA4": re.compile(r'G-[A-Z0-9]+'),
            "GTM": re.compile(r'GTM-[A-Z0-9]+'),
            "UA": re.compile(r'UA-[0-9]+-[0-9]+')
        }

        for script in scripts:
            script_text = script.text
            for tag_type, pattern in patterns.items():
                matches = pattern.findall(script_text)
                if matches:
                    analytics_tags.append((tag_type, matches[0]))

        return analytics_tags if analytics_tags else "Nenhuma tag encontrada"

    except Exception as e:
        return f"Erro: {str(e)}"

def save_results(results, file_path="output/analytics_results.csv"):
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Tag Tipo", "Tag Encontrada"])
        for url, tags in results.items():
            if isinstance(tags, list):
                for tag_type, tag_value in tags:
                    writer.writerow([url, tag_type, tag_value])
            else:
                writer.writerow([url, "Erro", tags])

if __name__ == "__main__":
    urls = load_urls("urls.txt")
    results = {url: find_google_analytics_tags(url) for url in urls}
    
    save_results(results)

    print("Análise concluída! em'output/analytics_results.csv'")
