import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

token = os.environ["token"]
url = os.environ["github_api_url"]
repositories = []

# after: null precisa?

query = '''
query {
  search(query: "stars:>1", type: REPOSITORY, first: 10) {
    repositoryCount
    edges {
      node {
        ... on Repository {
          nameWithOwner
          stargazerCount
          createdAt
          updatedAt
          pullRequests(states: MERGED) {
            totalCount
          }
          releases {
            totalCount
          }
          primaryLanguage {
            name
          }
          issues(states: [OPEN, CLOSED]) {
            totalCount
          }
          closedIssues: issues(states: CLOSED) {
            totalCount
          }
        }
      }
    }
  }
}
'''

headers = {"Authorization": "Bearer " + token}

response = requests.post(url, json={"query": query}, headers=headers)

repos = response.json()['data']['search']['edges']
count = 0

for repo in repos:
    count = count + 1
    name = repo['node']['nameWithOwner']
    stars = repo['node']['stargazerCount']
    created_at = datetime.strptime(
        repo['node']['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
    age = round((datetime.now() - created_at).days / 365.25, 2)
    num_pr_aprovados = repo['node']['pullRequests']['totalCount']
    num_releases = repo['node']['releases']['totalCount']
    updated_at = datetime.strptime(
        repo['node']['updatedAt'], '%Y-%m-%dT%H:%M:%SZ')
    dias_sem_update = (datetime.now() - updated_at).days
    linguagem_primaria = repo['node']['primaryLanguage']['name'] if repo['node']['primaryLanguage'] else 'Unknown'
    num_issues = repo['node']['issues']['totalCount']
    closed_issues = repo['node']['closedIssues']['totalCount']
    razao_closed_issues = round(
        closed_issues / num_issues, 2) if num_issues > 0 else 0
    print(f'\nREPOSITÓRIO Nº {count}')
    print(f'Nome: {name} Stars: {stars}')
    print(f'M01 - idade do repositório: {age} anos\n'
          f'M02 - Total de pull requests aceitas: {num_pr_aprovados}\n'
          f'M03 - Total de releases: {num_releases}\n'
          f'M04 - Tempo desde a última atualização: {dias_sem_update} dias\n'
          f'M05 - Linguagem primária: {linguagem_primaria}\n'
          f'M06 - Razão entre número de issues fechadas pelo total de issues: {razao_closed_issues}\n')
