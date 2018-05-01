# import requests
# from bs4 import BeautifulSoup
#
#
# class Joke(object):
#     def __init__(self):
#         self.url = 'https://www.qiushibaike.com/'
#
#     def get_joke(self):
#         res = requests.get(self.url)
#         html = res.text
#         soup = BeautifulSoup(html, 'lxml')
#         content = soup.select('.article > a > .content > span')
#         content_lis = []
#         for i in content:
#             # print(i)
#             j = i.get_text()
#             content_lis.append(j)
#         return content_lis
