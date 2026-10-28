import json, os, urllib.request
U="bujosa"; T=os.environ["GH_TOKEN"]
def gql(q):
    r=urllib.request.Request("https://api.github.com/graphql",json.dumps({"query":q}).encode(),{"Authorization":"bearer "+T})
    return json.load(urllib.request.urlopen(r))["data"]["user"]
d=gql('{user(login:"%s"){followers{totalCount} contributionsCollection{contributionCalendar{totalContributions} totalCommitContributions totalPullRequestContributions} repositories(first:100,ownerAffiliations:OWNER,isFork:false,orderBy:{field:STARGAZERS,direction:DESC}){totalCount nodes{stargazerCount languages(first:5,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}'%U)
c=d["contributionsCollection"]; rs=d["repositories"]
stars=sum(n["stargazerCount"] for n in rs["nodes"]); langs={}
for n in rs["nodes"]:
    for e in n["languages"]["edges"]:
        k=e["node"]["name"]; langs.setdefault(k,[0,e["node"]["color"] or "#888"]); langs[k][0]+=e["size"]
top=sorted(langs.items(),key=lambda x:-x[1][0])[:6]; tot=sum(v[0] for _,v in top) or 1
rows=[("Contributions (last year)",c["contributionCalendar"]["totalContributions"]),("Commits (last year)",c["totalCommitContributions"]),("Pull requests (last year)",c["totalPullRequestContributions"]),("Public repos",rs["totalCount"]),("Stars earned",stars),("Followers",d["followers"]["totalCount"])]
s=['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="230" font-family="Segoe UI,Helvetica,Arial,sans-serif"><rect width="718" height="228" x="1" y="1" rx="8" fill="#0d1117" stroke="#30363d"/>','<text x="24" y="38" fill="#58a6ff" font-size="18" font-weight="600">GitHub stats</text>']
for i,(k,v) in enumerate(rows):
    y=72+i*25; s.append(f'<text x="24" y="{y}" fill="#c9d1d9" font-size="14">{k}</text><text x="330" y="{y}" fill="#ffffff" font-size="14" font-weight="600" text-anchor="end">{v:,}</text>')
s.append('<text x="380" y="38" fill="#58a6ff" font-size="18" font-weight="600">Top languages</text>')
x=380
for k,(sz,col) in top:
    w=int(316*sz/tot); s.append(f'<rect x="{x}" y="56" width="{max(w,1)}" height="10" fill="{col}"/>'); x+=w
for i,(k,(sz,col)) in enumerate(top):
    y=96+i*22; s.append(f'<circle cx="388" cy="{y-5}" r="5" fill="{col}"/><text x="400" y="{y}" fill="#c9d1d9" font-size="13">{k} {100*sz/tot:.1f}%</text>')
s.append('</svg>'); open("stats.svg","w").write("".join(s))
