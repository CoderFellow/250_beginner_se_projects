import unittest
import asyncio
import aiohttp
from unittest import patch, MagicMock, AsyncMock

from async_scraper import fetch_page

mock_html = """
<!DOCTYPE html>
<html>
<body>
	<span id = "product_1_name">Test Product</span>
	<span id = "product_1_price">$99.99</span>
</body>
</html>
"""

class TestScraper(unittest.TestCase):
	def setUp(self):
		"""
		args:
			None
		returns:
			None
		"""
		# for test_fetch_page_success()
		# creating mock response object for success testing
		self.mock_response = MagicMock()
		self.mock_response.status = 200
		self.mock_response.text = AsyncMock(return_value=mock_html)
		
	@patch('aiohttp.ClientSession.get')
	async def test_fetch_page_success(self, mock_get):
		"""
		args:
			mock_get
			
		returns:
			None
		"""		
		# Configure the mock get to return an async context manager
		# that yields the mock response.
		mock_get.return_value.__aenter__.return_value = self.mock_response
		
		# call the async function and get the result
		result = await fetch_page("http://test.com")
		
		# Asset that the result matches the mock HTML.
		self.assertEqual(result, mock_html)

	
	@patch('aiohttp.ClientSession.get')
	async def test_parse_product_data(self, mock_get):
		"""
		New Test method, testing to see if the right data is being returned.
		
		args:
			mock_get
		
		return:
			None
		"""
		# configure the mock to return successful response
		mock_get.return_value.__aenter__.return_value = self.mock_response
		
		# call fetch page and parse product data
		html_content = await fetch_page("http://test.com")
		product_data = await parse_product_data(html_content)
		
		# defining the expected data
		expected_data = {'name': 'Test Product', 'price': '$99.99'}
		
		# check if the returned dictionaries matches the output data
		self.assertEqual(product_data, expected_data)
				
	@patch('aiohttp.ClientSession.get')
	async def test_fetch_page_timeout(self, mock_get):
		"""
		args:
			mock_get: object
		"""
		# configure the mock to raise a timeout error on entry
		mock_get.return_value.__aenter__.side_effect = asyncio.TimeoutError
		
		# call the async function. The try-except object block in fetch_page
		# should handle error.
		result = await fetch_page("http://test.com")
		
		# Assert that the result is None.
		self.assertIsNone(result)
		

if __name__ == "__main__":
	unittest.main()
