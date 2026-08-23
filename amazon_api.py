import requests
import hmac
import hashlib
import base64
from urllib.parse import quote
from datetime import datetime
from config import (
    AMAZON_ACCESS_KEY,
    AMAZON_SECRET_KEY,
    AMAZON_ASSOCIATE_TAG,
)

class AmazonAPI:
    def __init__(self):
        self.access_key = AMAZON_ACCESS_KEY
        self.secret_key = AMAZON_SECRET_KEY
        self.associate_tag = AMAZON_ASSOCIATE_TAG
        self.endpoint = 'https://api.amazon.com'
        self.region = 'us-east-1'
        self.service = 'ProductAdvertisingAPI'
        
    def _create_signature(self, params_str):
        """Create AWS Signature Version 4 for Amazon API requests"""
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            params_str.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode('utf-8')
    
    def search_products(self, keywords, max_results=5):
        """
        Search for products on Amazon
        
        Args:
            keywords (str): Product search keywords
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of product dictionaries with affiliate links
        """
        try:
            # Using Amazon Product Advertising API
            params = {
                'Operation': 'ItemSearch',
                'SearchIndex': 'All',
                'Keywords': keywords,
                'ResponseGroup': 'Large',
                'AssociateTag': self.associate_tag,
                'Service': self.service,
                'AWSAccessKeyId': self.access_key,
                'Timestamp': datetime.utcnow().isoformat() + 'Z',
                'Version': '2013-08-24'
            }
            
            # Sort parameters for signature
            sorted_params = sorted(params.items())
            params_str = '&'.join([f"{k}={quote(str(v), safe='~')}" for k, v in sorted_params])
            
            # Create signature
            signature = self._create_signature(params_str)
            
            # Build final URL with signature
            url = f"{self.endpoint}/?{params_str}&Signature={quote(signature, safe='~')}"
            
            # Make request
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse response and extract products
            products = self._parse_response(response.text, max_results)
            return products
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_product_details(self, asin):
        """
        Get detailed information about a specific product
        
        Args:
            asin (str): Amazon Standard Identification Number
            
        Returns:
            dict: Product details with affiliate link
        """
        try:
            params = {
                'Operation': 'ItemLookup',
                'ItemId': asin,
                'ResponseGroup': 'Large',
                'AssociateTag': self.associate_tag,
                'Service': self.service,
                'AWSAccessKeyId': self.access_key,
                'Timestamp': datetime.utcnow().isoformat() + 'Z',
                'Version': '2013-08-24'
            }
            
            sorted_params = sorted(params.items())
            params_str = '&'.join([f"{k}={quote(str(v), safe='~')}" for k, v in sorted_params])
            signature = self._create_signature(params_str)
            
            url = f"{self.endpoint}/?{params_str}&Signature={quote(signature, safe='~')}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return self._parse_product_details(response.text)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching product details: {e}")
            return None
    
    def _parse_response(self, xml_response, max_results):
        """Parse XML response from Amazon API"""
        products = []
        try:
            import re
            
            asin_pattern = r'<ASIN>([^<]+)</ASIN>'
            title_pattern = r'<Title>([^<]+)</Title>'
            price_pattern = r'<FormattedPrice>([^<]+)</FormattedPrice>'
            
            asins = re.findall(asin_pattern, xml_response)
            titles = re.findall(title_pattern, xml_response)
            prices = re.findall(price_pattern, xml_response)
            
            for i, asin in enumerate(asins[:max_results]):
                product = {
                    'asin': asin,
                    'title': titles[i] if i < len(titles) else 'Product',
                    'price': prices[i] if i < len(prices) else 'Price not available',
                    'affiliate_url': self._generate_affiliate_url(asin)
                }
                products.append(product)
                
        except Exception as e:
            print(f"Error parsing XML response: {e}")
        
        return products
    
    def _parse_product_details(self, xml_response):
        """Parse detailed product information from XML"""
        try:
            import re
            
            asin = re.search(r'<ASIN>([^<]+)</ASIN>', xml_response)
            title = re.search(r'<Title>([^<]+)</Title>', xml_response)
            price = re.search(r'<FormattedPrice>([^<]+)</FormattedPrice>', xml_response)
            
            return {
                'asin': asin.group(1) if asin else None,
                'title': title.group(1) if title else None,
                'price': price.group(1) if price else None,
                'affiliate_url': self._generate_affiliate_url(asin.group(1)) if asin else None
            }
        except Exception as e:
            print(f"Error parsing product details: {e}")
            return None
    
    def _generate_affiliate_url(self, asin):
        """Generate affiliate URL with associate tag"""
        return f"https://amazon.com/dp/{asin}/?tag={self.associate_tag}"