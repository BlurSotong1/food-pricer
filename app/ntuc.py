from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl

"""
    CONFIGURATION 
"""
url = "https://www.fairprice.com.sg/search?query="
headers = {'User-Agent': 'Mozilla/5.0'}


# Takes in a search query and returns a list of items on NTUC Fairprice
# that matches the query with their `title`, `price`, `measurement`, and `link`

# EXAMPLE:
# INPUT:
#       "chicken breast whole"
# OUTPUT:
# [
#     {
#         'title': "Aw's Market Chicken Breast Whole",
#         'price': 5.0,
#         'measurement': '400 g',
#         'link': 'https://www.fairprice.com.sg/product/aw-s-market-chicken-breast-whole-400-g-90018633',
#         'supermarket': 'ntuc'
#     },
#     {
#         'title': "Aw's Market Duck Breast Whole",
#         'price': 9.45,
#         'measurement': '800 g',
#         'link': 'https://www.fairprice.com.sg/product/aw-s-market-duck-breast-whole-800-g-90018554',
#         'supermarket': 'ntuc'
#     }
# ]
def search(keywords):
    context = ssl._create_unverified_context()

    # Function to generate the search-query URL
    def generateURL(url, keywords):
        cleanedKeywords = keywords.replace(' ', '%20')
        queryURL = url + cleanedKeywords
        return queryURL

    req = Request(generateURL(url, keywords), headers=headers)
    page = urlopen(req, context=context)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    matches = soup.select('div[class*="product-container"]')

    # Initialize the array to be returned
    result = []

    for elem in matches:
        matches = elem.findChildren("a", recursive=False)

        for match in matches:
            # Step 1: Find the name of the food product
            # The image of the food product contains a 'title' attribute that has the name of the food product
            image = match.findChildren("img")
            linkToProduct = match.attrs['href']

            # Step 2: Find the price of the food product
            # The span elements of the food product contain its price
            spanList = match.findChildren("span")
            priceList = []

            for span in spanList:
                # Check that the string contained inside the span element is referring to the price of the food item
                if "$" in span.text:
                    cleanedPrice = span.text.replace('$', '')
                    priceList.append(cleanedPrice)

            # Step 3: Find the weight/volume of the food product
            units = [
                'kg', 'KG',
                'g', 'G',
                'ml', 'ML',
                'l', 'L'
            ]

            measurement = ""
            for span in spanList:
                if any(x in span.text for x in units) and len(span.text) <= 15:
                    measurement = span.text

            # Step 4: Add the title, price, measurement, and link to the food product to the result object
            result.append({
                'title': image[0].attrs['title'],
                'price': min(priceList),
                'measurement': measurement,
                'link': "https://www.fairprice.com.sg" + linkToProduct,
                'supermarket': 'ntuc'
            })

    return result
