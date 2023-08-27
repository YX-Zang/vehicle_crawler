import time
import queue
import requests
import threading


class Requests_vehicle():
    def __init__(self, domain_url):
        self.requests = requests.Session()
        self.domain = domain_url
        self.queue_tasks = queue.Queue()
        self.queue_result = queue.Queue()

    timestamp_now = lambda self: int(time.time() * 1000)

    def get_request(self, url, **kwargs):
        res = self.requests.get(url, headers=self.header(), params=kwargs)
        return res.json()

    def header(self):
        return {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

    def get_models_url(self, uri='/p5bmw/extern/vehicle/models', recursive=True, **kwargs):
        if uri == '/p5bmw/extern/vehicly e/models':
            payloads = {'lang': 'en', 'serviceName': 'bmw_parts', '_': self.timestamp_now(), **kwargs}
        else:
            payloads = {}

        res = self.requests.get(self.domain + uri, params=payloads, headers=self.header())
        time.sleep(1)

        if recursive is False:
            for task in self.process_records(res.json()):
                self.queue_tasks.put(task)
            return

        for i in self.process_records(res.json()):
            if 'res3' in i:
                print(self.domain + i)
                self.queue_result.put(self.domain + i)
            else:
                print(f'recursive {i}')
                self.get_models_url(i)

    def process_records(self, records):
        ls1 = []
        if isinstance(records, dict):
            records = [records]
        for item in records:
            if item.get('data', {}).get('records'):
                for data in item['data']['records']:
                    if data.get('link') and not data.get('id', '').startswith('_'):
                        ls1.append(data['link']['path'])
        return ls1


    def run(self):
        '''
        先爬蟲第一次, 得到layer1 的結果
        將結果放在queue中
        接著再建立五個thread, 去將queue中的結果索取至空
        '''
        # 先爬蟲第一次, 得到layer1 的結果
        self.get_models_url(recursive=False)

        #  setting threading max counts
        semlock = threading.BoundedSemaphore(max_connections)
        threads = []
        for i in range(self.queue_tasks.qsize()):
            semlock.acquire()
            task = self.queue_tasks.get()
            t = threading.Thread(target=self.get_models_url, args=(task,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print('Done')


if __name__ == '__main__':
    max_connections = 10
    target_url = 'https://www.partslink24.com'
    crawler = Requests_vehicle(target_url)
    crawler.run()
