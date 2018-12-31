项目地址：[网易云音乐评论词云一键生成](https://github.com/geebos/wangyi_musi_wordcloud)

使用方法：

非常简单

```python
# 声明一个对象
music_id = '26608973'
wordcloud = WangYiMusicWordCloud(music_id, mask='mask.jpg', font_path='microsoft-yahei.ttf')
wordcloud.show_wordcloud()
```

效果如下：

![](http://upload-images.jianshu.io/upload_images/8516750-ff0bbe5ceb34c8ad.png)

### 依赖库

- `jieba`
- `pillow`
- `matplotlib`
- `numpy`
- `wordcloud`
- `requests`
- python版本 3.6.4

### 参数说明

- `music_id`必选参数，要生成的词云的音乐的 id，网页中打开音乐详情页面地址栏中的 id的值：`https://music.163.com/#/artist?id=789380`	
- `font_path`必选参数，字体文件路径
- `mask`可选参数，一张背景色为白色的图片的地址，如果想要生成的词云有特定的形状可以使用这个参数
- `stop_words`可选参数，屏蔽词列表，在里面的词都会被屏蔽，不会显示在词云中

### 方法说明

- `generate(**kwargs)`生成词云对象，可以重新指定 `naks`和`font_path`参数
- `show_wordcloud()`会自动调用（使用初始化的参数）`generate()`函数并将词云图片显示出来
- `to_file(filename)`将生成的词云图片保存下来，`filename`是要保存的文件名（带后缀）