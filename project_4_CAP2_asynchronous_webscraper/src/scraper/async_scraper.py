import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

async def fetch_page(url):
	"""
	Entry point that runs the function that fetches web pages.

	args:
		url: string
		
	return:
		None
	"""
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				response.raise_for_status()
				return await response.text()

	except aiohttp.ClientError as e:
		print(f"aiohttp.ClientError occurred: {e}")
		return None

	except asyncio.TimeoutError:
		print(f"asyncio.TimeoutError occurred while fetching {url}")
		return None

	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		return None

async def parse_product_data(html_content):
	"""
	This function parses product data, taking in the raw html text as an argument.

	args:
		html_content: some html file

	return:
		dict: string, variable_name: string
	"""
	if not html_content:
		return None

	soup = BeautifulSoup(html_content, 'html.parser')
	product_name_element = soup.find('span', id=lambda x: x and 'name' in x)
	product_price_element = soup.find('span', id=lambda x: x and 'price' in x)

	product_name = product_name_element.get_text(strip=True) if product_name_element else None		
	product_price = product_price_element.get_text(strip=True) if product_price_element else None

	return {'name': product_name, 'price': product_price}

async def main():
	"""
	This function serves to modify the function call
	to parse_product_data() function with the html content
	returned from the fetch_page(). Allowing for data visibility by me
	(the freakin developer).

	args:
		None

	returns:
		None
	"""
	urls = [
	"http://localhost:8080/e_com_page_1.html", 
	"http://localhost:8080/e_com_page_2.html", 
	"http://localhost:8080/e_com_page_3.html"]

	tasks = [fetch_page(url) for url in urls]
	html_contents = await asyncio.gather(*tasks)
	
	product_data = []

	for url, html in zip(urls, html_contents):
		if html:
			product_info = await parse_product_data(html)
			
			if product_info:
				product_data.append(product_info)
				print(f"URL: {url}")
				print(f"Product Info: {product_info}")
				print("---")
			
			else:
				print(f"Failed to parse data from {url}")
		else:
			print(f"Failed to fetch {url}")
	
	# after the loop is finished, save the collected data.
	if product_data:
		save_to_json(product_data, "products.json")
		print("Data is saved to products.json.")

def save_to_json(data, filename):
	"""
	Save a list of dictionaries to a JSON file.
	
	args:
		data: list of dicts
		filename: string
	"""
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	asyncio.run(main())
