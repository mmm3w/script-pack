### [食用说明](#thumb)
`dirthumb.py`: 创建文件夹封面，遍历所有文件夹和其子文件夹。当目录中存在图片文件时，会选择第一张图片复制名为`.thumb`的文件作为文件的封面图。
```python
py .\dirthumb.py targetdir
```

`cleardirtumb.py`：删除封面文件，删除上个脚本创建的封面文件，注意如果用户自有文件名为`.thumb   `，也会被删除。
```python
py .\cleardirtumb.py targetdir
```

`videothumb.py`：创建视频封面，遍历所有文件夹和其子文件夹。当目录中存在视频文件时，会创建`.videothumb`文件夹，然后截取视频帧以视频名保存一张jpg。如果如果视频长度大于10s，会截取第10秒的画面，否则截取第0秒画面。
```python
py .\videothumb.py targetdir
```

`clearvideothumb.py`：删除封面文件
```python
py .\clearvideothumb.py targetdir
```
