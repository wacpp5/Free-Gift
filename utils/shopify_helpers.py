import os
import requests

SHOP = os.getenv("SHOPIFY_STORE_DOMAIN")
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
GIFT_COLLECTION = os.getenv("FREE_GIFT_COLLECTION_HANDLE", "free-gifts")

def get_free_gift_products():
    url = f"https://{SHOP}/admin/api/2023-10/graphql.json"
    headers = {
        "X-Shopify-Access-Token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    query = f"""
    {{
      collectionByHandle(handle: "{GIFT_COLLECTION}") {{
        products(first: 10) {{
          edges {{
            node {{
              title
              images(first: 1) {{
                edges {{
                  node {{ url }}
                }}
              }}
              variants(first: 1) {{
                edges {{
                  node {{
                    id
                    price
                    availableForSale
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(url, headers=headers, json={"query": query})
    data = response.json()

    products = []
    try:
        for edge in data["data"]["collectionByHandle"]["products"]["edges"]:
            product = edge["node"]
            variant = product["variants"]["edges"][0]["node"]
            if variant["availableForSale"] and float(variant["price"]) == 0.0:
                products.append({
                    "title": product["title"],
                    "image": product["images"]["edges"][0]["node"]["url"],
                    "variant_id": variant["id"].split("/")[-1]
                })
    except Exception as e:
        print("Error parsing products:", e)

    return products[:3]
