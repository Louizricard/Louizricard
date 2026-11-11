"""Estatísticas reais de repositórios públicos, sem serviços de cards externos."""
from datetime import datetime, timezone
from pathlib import Path
import json, os
from urllib.request import Request, urlopen
USER = "Louizricard"
def get(path):
    headers = {"Accept":"application/vnd.github+json","User-Agent":"Louizricard-profile"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request("https://api.github.com/"+path, headers=headers),timeout=30) as response:
        return json.load(response)
def main():
    user=get(f"users/{USER}")
    repos=[]; page=1
    while True:
        batch=get(f"users/{USER}/repos?type=owner&per_page=100&page={page}")
        repos.extend(r for r in batch if not r["fork"] and not r["private"])
        if len(batch)<100: break
        page+=1
    metrics=[(str(user["public_repos"]),"Repositórios públicos"),(str(sum(r["stargazers_count"] for r in repos)),"Estrelas em projetos próprios"),(str(user["followers"]),"Seguidores")]
    date=datetime.now(timezone.utc).strftime("%d/%m/%Y")
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="200" viewBox="0 0 1200 200" role="img"><title>Estatísticas públicas do GitHub</title><rect width="1200" height="200" rx="16" fill="#081a2f"/>']
    for i,(value,label) in enumerate(metrics):
        x=40+i*396
        parts.append(f'<text x="{x}" y="83" fill="#19e6a7" font-family="DejaVu Sans,Arial,sans-serif" font-size="52" font-weight="700">{value}</text>')
        parts.append(f'<text x="{x}" y="123" fill="#ffffff" font-family="DejaVu Sans,Arial,sans-serif" font-size="21">{label}</text>')
    parts.append(f'<text x="40" y="174" fill="#b7c3d0" font-family="monospace" font-size="16">DADOS PÚBLICOS · {date} UTC · estrelas sem forks</text></svg>\n')
    Path("assets/stats.svg").write_text("".join(parts),encoding="utf-8")
if __name__=="__main__": main()
