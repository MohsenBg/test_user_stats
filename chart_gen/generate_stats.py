import requests
import matplotlib.pyplot as plt
from typing import List
import json
import random
import argparse

def generate_random_color() -> str:
    return "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_language_color(name: str) -> str:
    file_path = "colors.json"
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data.get(name, generate_random_color())
    except FileNotFoundError:
        return generate_random_color()

class Language:
    def __init__(self, name: str, size: int, percentage: float, color: str):
        self.name = name
        self.size = size
        self.percentage = percentage
        self.color = color

    def __repr__(self):
        return f"Language(name={self.name}, size={self.size}, percentage={self.percentage}, color={self.color})"

def get_repo_languages(owner: str, repo: str) -> List[Language]:
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return [], 0

    languages = response.json()
    total_size = sum(languages.values())

    return [
        Language(name, size, (size / total_size) * 100, get_language_color(name))
        for name, size in languages.items()
    ], total_size

def plot_pie_chart(language_list: List[Language], output_path: str = "pie_chart.svg"):
    labels = [f"{lang.name} ({lang.percentage:.1f}%)" for lang in language_list]
    sizes = [lang.size for lang in language_list]
    colors = [lang.color for lang in language_list]

    plt.figure(figsize=(6, 6))
    wedges, _ = plt.pie(sizes, colors=colors, startangle=140, wedgeprops={'edgecolor': 'black'}, labeldistance=1.1)

    plt.legend(
        handles=wedges, labels=labels,
        loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3,
        handleheight=1.5, labelspacing=1.2
    )

    plt.subplots_adjust(top=0.9, bottom=0.2, left=0.1, right=0.9)
    plt.title("Repository Language Distribution")
    plt.axis('equal')

    plt.savefig(output_path, format="svg", bbox_inches="tight")
    print(f"Pie chart saved at {output_path}")
    # plt.show();

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a GitHub repository language pie chart.")
    parser.add_argument("owner", type=str, help="GitHub repository owner (username or org)")
    parser.add_argument("repo", type=str, help="GitHub repository name")

    args = parser.parse_args()
    languages, _ = get_repo_languages(args.owner, args.repo)

    if languages:
        plot_pie_chart(languages)
