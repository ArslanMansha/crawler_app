"""Parallell execution of a crawler"""
import concurrent.futures
import time
import requests


def get_website_details(kwargs):
    """Crawls website and return lenght of response."""
    time.sleep(kwargs['Delay'])
    response_length = len(requests.get('https://www.damart.co.uk/' + kwargs['URL']).text)
    return response_length


def paralell_execution(urls, download_delay, workers):
    """Performs main functionality."""
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(get_website_details, {'URL': url, 'Delay': download_delay})
                   for url in urls]
        concurrent.futures.wait(futures)
        len_sum = 0
        for future in futures:
            len_sum = len_sum + future.result()

        return {
            'Total bytes downloaded': len_sum,
            'Average size of Page': len_sum/len(urls),
            'Number of requests': len(urls),
        }


def start_paralell_execution(kwargs):
    """Initiates parallell execution."""
    start_time = time.time()
    print(paralell_execution(kwargs['urls'], kwargs['delay'], kwargs['workers']))
    end_time = time.time()
    print("Time Consumed: {}Seconds".format(end_time - start_time))
