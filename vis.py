import time, os, sys, html
import requests
import pandas as pd

class VIS:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), 'data')
        self.columns = [u'title', u'author', u'abstract', u'keywords', u'type', u'session', u'award', u'video', u'detail']

    # 要爬取的 url 地址
    def getUrl(self, year):
        return f'https://virtual.ieeevis.org/year/{year}/papers.json'

    # 请求原始内容
    def getData(self, year, retry=5):
        req = requests.get(self.getUrl(year), headers={
            "Referer": f'https://virtual.ieeevis.org/year/{year}/papers.html?filter=keywords&search=',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        })
        for i in range(retry):
            try:
                content = req.json()
                if content:
                    filename = os.path.join(self.path, f'VIS_{year}.json')
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(req.text)
                    return content
                else:
                    time.sleep(60)
                    print('failed to get content, retry: {}'.format(i))
                    continue
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
        return None

    # 将原始内容转化为数据列表
    def convertToList(self, content, year):
        return list(map(lambda item: [
            item.get('title', ''),
            ', '.join(item.get('authors', [])),
            item.get('abstract', ''),
            ', '.join(item.get('keywords', [])),
            item.get('paper_type_name', ''),
            item.get('session_title', ''),
            item.get('award', ''),
            item.get('prerecorded_video_link', ''),
            f'https://virtual.ieeevis.org/year/{year}/paper_{item.get("UID", "")}.html'
        ], content))

    # 保存数据至 csv 文件和 md 文件
    def saveData(self, data, year):
        if not data:
            exit()

        # 保存 md 文件
        md = f'# IEEE VIS {year}\n## Papers\n<table><tr>'
        md += '<th>id</th>' + ''.join(map(lambda field: f'<th>{field}</th>', self.columns))
        md += '</tr>'
        for id, item in enumerate(data):
          md += f'<tr><td>{id + 1}</td>'
          md += ''.join(map(lambda field: f'<td></td>' if not field else '<td><a href="{field}">link</a></td>' if field.startswith('http') else f'<td>{html.escape(field)}</td>', item))
          md += '</tr>'
        md += '</table>'
        filename = os.path.join(self.path, f'VIS_{year}.md')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md)

        # 保存 csv 文件
        data_map = {}
        for id, field in enumerate(self.columns):
            data_map[field] = [item[id] for item in data]
        df = pd.DataFrame(data_map, columns=self.columns)
        filename = os.path.join(self.path, f'VIS_{year}.csv')
        df.to_csv(filename, encoding='utf-8')

    # 爬取、保存数据
    def crawlData(self, startYear, endYear):
        for year in range(int(startYear), int(endYear)+1):
            print(year)
            content = self.getData(str(year))
            data_list = self.convertToList(content, year)
            self.saveData(data_list, year)
            time.sleep(5)

if __name__ == '__main__':
    model = VIS()
    if len(sys.argv) > 1:
        start = sys.argv[1]
    else:
        start = '2022'
    if len(sys.argv) > 2:
        end = sys.arv[2]
    else:
        end = start
    model.crawlData(start, end)