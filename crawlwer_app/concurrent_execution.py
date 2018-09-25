"""Concurrent execution of a crawler"""
import time
import asyncio
import requests


async def get_website_details(kwargs):
    """Crawls website and return lenght of response."""
    await asyncio.sleep(kwargs['Delay'])
    response_length = len(requests.get('https://www.damart.co.uk/' + kwargs['URL']).text)
    return response_length


async def concurrent_execution(urls, download_delay, max_concurrent_tasks):
    """Performs main functionality."""
    num_urls = len(urls)
    len_sum = 0
    while urls:
        tasks = [asyncio.ensure_future(get_website_details({'URL': url, 'Delay': download_delay}))
                 for url in urls[0:max_concurrent_tasks]]
        await asyncio.gather(*tasks)
        for task in tasks:
            len_sum = len_sum + task.result()
        urls = urls[max_concurrent_tasks::]
    return {
        'Total bytes downloaded': len_sum,
        'Average size of Page': len_sum/num_urls,
        'Number of requests': len(urls),
    }


def start_concurrent_execution(kwargs):
    """Initiates paralell execution."""
    start_time = time.time()
    loop = asyncio.get_event_loop()
    task = loop.create_task(concurrent_execution(kwargs['urls'], kwargs['delay'], kwargs['workers']))
    loop.run_until_complete(task)
    print(task.result())
    loop.close()
    end_time = time.time()
    print("Time Consumed: {}Seconds".format(end_time - start_time))
