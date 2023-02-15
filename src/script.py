import requests
import os
from datetime import datetime
from  dotenv import load_dotenv

load_dotenv()

token = os.environ["token"]
url = os.environ["github_api_url"]
repositories = []

query = '''
query {
  search(query: "stars:>1", type: REPOSITORY, first: 100, after: null) {
    repositoryCount
    edges {
      node {
        ... on Repository {
          nameWithOwner
          stargazerCount
          createdAt
          pullRequests(states: MERGED) {
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

for repo in repos:
    name = repo['node']['nameWithOwner']
    stars = repo['node']['stargazerCount']
    created_at = datetime.strptime(repo['node']['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
    age = round((datetime.now() - created_at).days / 365.25, 2)
    acpted_pr_count = repo['node']['pullRequests']['totalCount']
    print(name,stars,age,acpted_pr_count)
    breakpoint()
