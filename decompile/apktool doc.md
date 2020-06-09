#### 反编译
apktool可以使用 [**d**]() 或者 [**decode**]() 进行反编译操作
```shell
$ apktool d foo.jar
$ apktool decode foo.jar
// 将foo.jar 反编译至 foo.jar.out 文件夹

$ apktool d bar.apk
$ apktool decode bar.apk
// 将 bar.apk 反编译至 bar 文件夹

$ apktool d bar.apk -o baz
// 将 bar.apk 反编译至 baz 文件夹
```
#### 编译
apktool可以使用 [**b**]() 或者 [**build**]() 进行编译操作
```shell
$ apktool b foo.jar.out
$ apktool build foo.jar.out
// 将 foo.jar.out 文件夹中的文件编译输出为 foo.jar.out/dist/foo.jar 文件

$ apktool b bar
// 将 bar 文件夹中的文件编译输出为 bar/dist/bar.apk 文件

$ apktool b .
// 将 当前 文件夹中的文件编译后输出至 ./dist 文件夹

$ apktool b bar -o new_bar.apk
// 将 bar 文件夹中的文件编译输出为 into new_bar.apk 文件

$ apktool b bar.apk
// WRONG: brut.androlib.AndrolibException: brut.directory.PathNotExist: apktool.yml
// 必须使用文件夹，不支持jar或者apk
```
为了能够重新运行重新构建过的应用，你必须对应用重新签名
#### 架构
apktool可以使用 [**if**]() 或者 [**install-framework**]() 进行编译操作
并且包含两个可选参数
+ [**-p, --frame-path**]() [**<dir\>**]() 框架apk的路径
+ [**-t, --tag**]() [**<tag\>**]()

```shell
$ apktool if framework-res.apk
I: Framework installed to: 1.apk
// framework-res.apk 的 pkgId 是 1(which is 0x01)

$ apktool if com.htc.resources.apk
I: Framework installed to: 2.apk
// com.htc.resources 的 pkgId 是 0x02

$ apktool if com.htc.resources.apk -t htc
I: Framework installed to: 2-htc.apk
// pkgId-tag.apk

$ apktool if framework-res.apk -p foo/bar
I: Framework installed to: foo/bar/1.apk

$ apktool if framework-res.apk -t baz -p foo/bar
I: Framework installed to: foo/bar/1-baz.apk
````
#### 说明
每个版本的Apktool都包含了最新的aosp框架，保证能够完成大多数apk的编译和反编译工作。但是有些制造商还包含了自己的框架文件，针对这些制造商的apk，必须首先安装框架文件。
###### 如何找到框架文件
在设备 [**/system/framework**]() 目录下的大多数apk都可能是框架文件。有部分设备可能会放在 [**/data/system-framework**]() 目录下 甚至隐藏在 [**/system/app**]() 或者 [**/system/priv-app**]() 目录中。它们通常会命名成 [**"resources", "res",  "framework"**]()
