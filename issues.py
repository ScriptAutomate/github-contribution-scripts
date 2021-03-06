#!/usr/bin/env python3

from gql import gql, Client, AIOHTTPTransport
from os import environ
from sys import argv

transport = AIOHTTPTransport(
    url="https://api.github.com/graphql",
    headers={"Authorization": "bearer " + environ["GITHUB_TOKEN"]},
)
client = Client(transport=transport, fetch_schema_from_transport=True)


def make_request(after=None):
    if after is None:
        query = gql(
            """
query {
  user(login: \""""
            + argv[1]
            + """\") {
    issues(first: 100) {
      edges {
        node {
          url
        }
      }
      pageInfo {
        endCursor
        hasNextPage
        hasPreviousPage
        startCursor
      }
      totalCount
    }
  }
}
"""
        )
    else:
        query = gql(
            """
query {
  user(login: \""""
            + argv[1]
            + """\") {
    issues(first: 100, after: \""""
            + after
            + """\") {
      edges {
        node {
          url
        }
      }
      pageInfo {
        endCursor
        hasNextPage
        hasPreviousPage
        startCursor
      }
      totalCount
    }
  }
}
"""
        )
    result = client.execute(query)
    for i in result["user"]["issues"]["edges"]:
        print(i["node"]["url"])
    if result["user"]["issues"]["pageInfo"]["hasNextPage"]:
        return result["user"]["issues"]["pageInfo"]["endCursor"]
    else:
        print("totalCount: " + str(result["user"]["issues"]["totalCount"]))
        return None


after = None
while True:
    after = make_request(after=after)
    if after is None:
        break
