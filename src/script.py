
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import csv

load_dotenv()

token = os.environ["token"]
url = os.environ["github_api_url"]
repositories = []


query = '''
query {
  search(query: "stars:>1", type: REPOSITORY, first: 20, after: null) {
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
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
'''

headers = {"Authorization": "Bearer " + token}
count = 0
data = []
cursor = None 

while count < 1000:
    if cursor:
        query_with_cursor = query.replace('after: null', 'after: "%s"' % cursor)

        response = requests.post(url, json={"query": query_with_cursor}, headers=headers)
    else:
        response = requests.post(url, json={"query": query}, headers=headers)

    if response.status_code == 200:
        repos = response.json()['data']['search']['edges']
        page_info = response.json()['data']['search']['pageInfo']
        cursor = page_info['endCursor']
        has_next_page = page_info['hasNextPage']

        for repo in repos:
            count += 1
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
            
            row = [count, name, stars, age, num_pr_aprovados, num_releases, dias_sem_update, linguagem_primaria, razao_closed_issues]
            data.append(row)
        print(count)
    else:
        print('Error:', response.content)

with open('resultados.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Número', 'Nome', 'Estrelas', 'Idade (anos)', 'PRs Aprovados', 'Releases', 'Dias sem Update', 'Linguagem Primária', 'Razão de Issues Fechadas'])
    for row in data:
        writer.writerow(row)


    # print(f'\nREPOSITÓRIO Nº {count}')
    # print(f'Nome: {name} Stars: {stars}')
    # print(f'M01 - idade do repositório: {age} anos\n'
    #       f'M02 - Total de pull requests aceitas: {num_pr_aprovados}\n'
    #       f'M03 - Total de releases: {num_releases}\n'
    #       f'M04 - Tempo desde a última atualização: {dias_sem_update} dias\n'
    #       f'M05 - Linguagem primária: {linguagem_primaria}\n'
    #       f'M06 - Razão entre número de issues fechadas pelo total de issues: {razao_closed_issues}\n')
