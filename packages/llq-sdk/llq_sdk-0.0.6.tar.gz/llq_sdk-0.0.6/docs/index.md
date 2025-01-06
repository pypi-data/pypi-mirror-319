## Getting Started

The LLQ SDK is a library designed to help developers interact seamlessly with the LeLabQuantique.com API.

### Installation

You can install the LLQ SDK from PyPI using pip:

```bash
pip install llq-sdk
```

### API Key

An API key is required for insertion operations. You can request an API key by creating an issue in the LLQ SDK repository:
[https://github.com/Le-Lab-Quantique/llq-sdk](https://github.com/Le-Lab-Quantique/llq-sdk).

### Exemple

```python
from llq import GraphQLClient, PartnersQuery

client = GraphQLClient(endpoint_url="https://lelabquantique.com/graphql")
await client.connect()
partners = PartnersQuery()
partners_query = partners.get(first=50)
response = await client.execute(partners_query)
partners_list = partners.parse(response)
await client.close()

print(partners_list)
```
