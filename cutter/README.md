### [食用说明](#cutter)

timenode: 时间节点，单位秒，输入的当前秒会被切入下一分P中
videocutters多线程，效率没差多少
```python
py ./videocutter.py videofile timenode....
```

`autocutter`:扫描目录按指定配置进行剪取视频

配置实例 配置名 `cut.json`
```json
[
    {
        "file":"", //同目录下的文件名
        "part":[ //需要剪出来的部分
            {
                "start":0, //开始时间 s
                "end":-1, //结束时间 -1 为None
                "ext":"1" //名字扩展的部分，会以-ext额形式拼接在原来的文件名上
            }
        ]
    }
]
```