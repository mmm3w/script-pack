### 透明网关

##### base-component (sudo)
基础组件安装，其中包括ssr编译库，ssr，ss-tproxy
+ 参数1:(all/base/libsodium/mbedtls/ssr/tproxy)需要安装的部分
+ 参数2:(akkariiin/-) ssr版本

##### ssr-subscribe
通过订阅地址获取相关服务器的json配置文件
+ 需要同目录下 [sub.conf]() 配置文件
+ configfile="your path" 配置文件存放的路径
+ url="your subscription address" 订阅地址

##### server-set
修改ss-tproxy相关配置信息，主要用于服务器配置切换
+ 参数1:配置文件的路径
+ 内网网段直接修改脚本文件

##### server-test
简单测试服务器访问延迟
+ 参数1:配置文件路径，ssr-subscribe脚本生成配置文件的路径
+ 参数2:对服务器简单过滤
