import os
import requests
import random
from concurrent.futures import ThreadPoolExecutor


class ProxyManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProxyManager, cls).__new__(cls)
            cls._instance.proxies = []  # Initialize the proxy list
            cls._instance.update_proxy_list()  # Fetch and test proxies immediately upon creation
        return cls._instance

    def update_proxy_list(
        self,
        url="https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    ):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Split the response text by newline to get each proxy
            proxy_lines = response.text.strip().split("\n")
            proxies_to_test = [
                {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                for proxy in proxy_lines
            ]

            # Use a ThreadPoolExecutor to test proxies concurrently
            max_workers = os.cpu_count() * 2
            print(f"Testing proxies with {max_workers} workers...")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = executor.map(self._test_proxy, proxies_to_test)

            # Update the proxy list with only the working proxies
            self.proxies = [
                proxy
                for proxy, is_working in zip(proxies_to_test, results)
                if is_working
            ]
            print(f"Updated proxy list with {len(self.proxies)} working proxies.")
        except requests.RequestException as e:
            print(f"Error fetching proxies: {e}")

    def get_proxy(self):
        # Return a random proxy from the list
        if self.proxies:
            return random.choice(self.proxies)
        else:
            print("Proxy list is empty. Fetching new proxies.")
            self.update_proxy_list()
            return self.get_proxy() if self.proxies else None

    def _test_proxy(self, proxy):
        # Test the proxy by sending a request to google.com
        test_url = "https://www.google.com"
        try:
            response = requests.get(test_url, proxies=proxy, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
