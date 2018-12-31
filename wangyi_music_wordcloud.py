#-*- coding: utf-8 -*
__author__ = 'geebos'
from jieba import posseg
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import wordcloud
import requests
import time
import re
import os


def _content_generator(music_id):
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_%s' % music_id
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Host': 'music.163.com',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': '__f_=1544879495065; _ntes_nnid=ec5f372598a44f7d45726f800d3c244b,1544879496275; _ntes_nuid=ec5f372598a44f7d45726f800d3c244b; _iuqxldmzr_=32; __utmc=94650624; WM_TID=SjPgpIfajWhEUVQQAVYoLv%2BJSutc41%2BE; __utma=94650624.1212198154.1546091705.1546142549.1546173830.4; __utmz=94650624.1546173830.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_NI=fjy1sURvfoc29LFwx6VN7rVC6wTgq5EA1go8oNGPt2OIoPoLBInGAKxG9Rc6%2BZ%2F6HQPKefTD2kdeQesFU899HSQfRmRPbGmc6lxhGHcRpZAVtsYhGxIWtlaVLL1c0Z7HYUc%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee89ef48839ff7a3f0668abc8aa3d15b938b8abab76ab6afbab4db5aacaea290c52af0fea7c3b92aa6b6b7d2f25f92aaaa90e23afb948a98fb3e9692f993d549f6a99c88f43f879fff88ee34ad9289b1f73a8d97a1b1ee488297a2a8c441bc99f7b3e23ee986e1d7cb5b9495ab87d750f2b5ac86d46fb19a9bd9bc338c8d9f87d1679290aea8f069f6b4b889c644a18ec0bbc45eb8ad9789c6748b89bc8de45e9094ff84b352f59897b6e237e2a3; __utmb=94650624.8.10.1546173830; JSESSIONID-WYYY=JhDousUg2D2BV1f%2Bvq6Ka6iQHAWfFvQOPdvf5%5CPMQISbc5nnfzqQAJDcQsezW82Cup2H5n1grdeIxXp79veCgoKA68D6CSkgCXcOFkI04Hv8hEXG9tWSMKuRx0XZ4Bp%5C%5CSbZzeRs6ey4FxADkuPVlIIVSGn%2BTq8mYstxPYBIg0f2quO%5C%3A1546177369761',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }
    limit = 20
    offset = 0
    compiler = re.compile(r'[^\u4E00-\u9FA5^\u3000-\u303F^\uFF00-\uFFEF^0-9^a-z^A-Z]')

    while True:
        params = {
            'limit': limit,
            'offset': offset,
        }
        offset += limit
        r = requests.get(url, headers=headers, params=params)
        comments = r.json()['comments']
        has_more = r.json()['more']

        for t in comments:
            yield compiler.subn('', t['content'])[0]

        if not has_more:
            break


class WangYiMusicWordCloud:
    stop_words = ['首歌']
    def __init__(self, music_id, mask=None, font_path=None, stop_words=None):
        self.music_id = music_id
        self.mask = mask
        self.font_path = font_path

        if not stop_words is None:
            self.stop_words+=stop_words

        self.img_wordcloud = None

    def _cut_word(self, comment):
        word_pairs = posseg.lcut(comment, HMM=False)
        result = []
        for t in word_pairs:
            if not (t.word in result or t.word in self.stop_words):
                result.append(t.word)
        return '/'.join(result)


    def get_words_text(self):
        if os.path.isfile(f'{self.music_id}.txt'):
            print('评论文件已存在，读取文件...')
            with open(f'{self.music_id}.txt', 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print('没有默认评论文件，开始爬取评论...')
            count = 0
            text = []
            comments = _content_generator(self.music_id)
            for t in comments:
                text.append(self._cut_word(t))

                count += 1
                print(f'\r已爬取 {count}条评论', end='')
                if count % 100 == 0:
                    print(f'\r已爬取 {count}条评论, 休息 2s', end='')
                    time.sleep(2)

            str_text = '\n'.join(text)
            with open(f'{self.music_id}.txt', 'w', encoding='utf-8') as f:
                f.write(str_text)
                print(f'\r共爬取 {count}条评论，已写入文件 {self.music_id}.txt')
            return str_text

    def generate(self, **kwargs):
        default_kwargs = {
            'background_color': "white",
            'width': 1000,
            'height': 860,
            'margin': 2,
            'max_words': 50,
            'stopwords': wordcloud.STOPWORDS,
        }
        if not self.mask is None:
            default_kwargs['mask'] = np.array(Image.open(self.mask))
        if not self.font_path is None:
            default_kwargs['font_path'] = self.font_path
        elif 'font_path' not in kwargs:
            raise ValueError('缺少参数 font_path')
        default_kwargs.update(kwargs)

        str_text = self.get_words_text()
        self.wordcloud = wordcloud.WordCloud(**default_kwargs)
        self.img_wordcloud = self.wordcloud.generate(str_text)

    def show_wordcloud(self):
        if self.img_wordcloud is None:
            self.generate()

        plt.axis('off')
        plt.imshow(self.img_wordcloud)
        plt.show()

    def to_file(self, filename):
        self.wordcloud.to_file(filename)

if __name__ == '__main__':
    music_id = '26608973'
    wordcloud_obj = WangYiMusicWordCloud(music_id, mask='mask.jpg', font_path='microsoft-yahei.ttf')
    wordcloud_obj.show_wordcloud()
    wordcloud_obj.to_file('result.jpg')

