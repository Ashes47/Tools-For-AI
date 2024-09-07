import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from constants import PROXY_PATH


class ProxyManager:
    _instance = None
    blacklist_file_path = PROXY_PATH

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProxyManager, cls).__new__(cls)
            cls._instance.proxies = []
            cls._instance.blacklist = cls._instance.load_blacklist()
            cls._instance.update_proxy_list()
        return cls._instance

    def load_blacklist(self):
        try:
            with open(self.blacklist_file_path, "r") as file:
                return set(line.strip() for line in file if line.strip())
        except FileNotFoundError:
            return set()

    def save_blacklist(self):
        with open(self.blacklist_file_path, "w") as file:
            for proxy in self.blacklist:
                file.write(proxy + "\n")

    def update_proxy_list(
        self,
        url="https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    ):
        try:
            response = requests.get(url)
            response.raise_for_status()
            proxy_lines = response.text.strip().split("\n")
            proxies_to_test = [
                {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                for proxy in proxy_lines
                if proxy not in self.blacklist
            ]

            max_workers = os.cpu_count() * 2
            print(f"Testing proxies with {max_workers} workers...")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(self._test_proxy, proxies_to_test))

            # Store working proxies with their response times
            working_proxies = [
                (proxy["http"].split("//")[1], time_taken)
                for proxy, (is_working, time_taken) in zip(proxies_to_test, results)
                if is_working
            ]
            # Sort proxies by response time
            working_proxies.sort(key=lambda x: x[1])

            self.proxies = working_proxies
            print(f"Updated proxy list with {len(self.proxies)} working proxies.")
            # Update the blacklist
            self.blacklist.update(
                set(proxy_lines) - set(proxy[0] for proxy in working_proxies)
            )
            self.save_blacklist()
        except requests.RequestException as e:
            print(f"Error fetching proxies: {e}")

    def get_proxy(self):
        if self.proxies:
            # Get the proxy with the fastest response time (first in the sorted list)
            fastest_proxy, fastest_time = self.proxies[0]
            print(
                f"Using fastest proxy: {fastest_proxy} with response time: {fastest_time:.2f} seconds"
            )
            return {
                "http": f"http://{fastest_proxy}",
                "https": f"http://{fastest_proxy}",
            }
        else:
            print("Proxy list is empty. Fetching new proxies.")
            self.update_proxy_list()
            return self.get_proxy() if self.proxies else None

    def remove_and_update_proxy(self, non_functional_proxy):
        # Remove the non-functional proxy and optionally fetch more if the list is low
        self.proxies = [
            proxy for proxy in self.proxies if proxy[0] != non_functional_proxy
        ]
        self.blacklist.add(non_functional_proxy)
        self.save_blacklist()
        print(f"Removed and blacklisted non-functional proxy: {non_functional_proxy}")
        if len(self.proxies) < 5:  # Arbitrary threshold to decide when to fetch more
            print("Proxy count low, updating proxy list...")
            self.update_proxy_list()

    def _test_proxy(self, proxy):
        test_url = "https://www.google.com"
        try:
            start_time = time.time()
            response = requests.get(test_url, proxies=proxy, timeout=5)
            response_time = time.time() - start_time
            return (response.status_code == 200, response_time)
        except requests.RequestException:
            return (False, float("inf"))
