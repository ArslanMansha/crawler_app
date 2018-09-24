"""Controls the execution of required type."""
import concurrent_execution
import paralell_execution
import requests
from parsel import Selector


def get_links(url):
    """Extarcts links from home page."""
    response_body = Selector(requests.get(url).text)
    urls = response_body.xpath('//nav[@id="navbar"]/ul//a/@href').extract()
    return urls


def main_menu():
    """Displays main menu."""
    print("Scrapping urls of DAmart Home page")
    print("For Concurrent Execution...press 1")
    print("For parallel Execution.....press 2")
    print("To Exit....................press Any key")
    return input("Enter your choice: ")


def submenu():
    """Take required info from user."""
    delay = float(input("Enter Delay Time: "))
    max_no_of_urls = int(input("Enter maximum number of urls to visit(180 at max): "))
    urls = get_links('https://www.damart.co.uk/')
    max_no_of_urls = max_no_of_urls if max_no_of_urls < len(urls) else len(urls)
    workers = int(input("Enter numer of concurrent requests: "))
    return {
        "delay": delay,
        "urls": urls[0:max_no_of_urls],
        "workers": workers
    }


def app():
    """Summons desired execution."""
    choice = main_menu()
    details = submenu(choice)
    if choice == '1':
        concurrent_execution.start_concurrent_execution(details)
    elif choice == '2':
        paralell_execution.start_paralell_execution(details)
    else:
        return


app()
