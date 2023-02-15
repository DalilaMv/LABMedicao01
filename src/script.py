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
        }
      }
    }
  }
}
'''

headers = {"Authorization": "Bearer " + token}


response = requests.post(url, json={"query": query}, headers=headers)

data = response.json()['data']['search']['edges']