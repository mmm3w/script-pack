## 重新整理的脚本
python为主，之前有过shell脚本，后来全改成py来实现了。

#### PixicGetter
用于下载Pixiv画师的所有作品，因为Pixiv在登录上加入了Google人机验证，所以采用读取chrome的cookie来建立session
`downloadArtworks`：用于下载单张图片，输入作品的pid
`traverseCreator`：用于下载画师的所有作品，输入画师的uid

#### bokaro
用于从niconico上获取VOCALOID榜单曲目，将会生成MD表格

#### paofu
用于泡芙云签到，虽然不怎么用，而且好像运行并不稳定

#### proxy
代理中要用的一些脚本，以及两个备用的软件包。

#### timing
用于整点报时用的脚本，用的舰娘语音。同时包含从一些wiki站下载语音的脚本(这部分脚本因为网站的一些原因可能工作不正常)。

#### rename
用于重命名文件的脚本。重新整理了代码，功能整合，通过文件配置来预输入一些参数。

#### decompile
用于反编译APK的脚本。写的有点烂，不支持多平台，只确认能在win上跑，而且没有信心不出bug。考虑重写