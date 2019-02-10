# EMP
EMP(Easy MicroPython) 是一个为MicroPython编写的第三方模块，通过对例如WiFi的连接和管理，文件的增删改查等一些复杂操作的封装，
使得用户能够更容易的在MicroPython上进行一些基本的操作，同时，该模块的存在使得你可以轻松的将你的设备和我们的EMP-IDE进行连接，无论是有线串口的模式还是无线WiFi的模式。

在开始之前，我们先简单的介绍一下EMP-IDE工作的基本原理。

## EMP-IDE的基本工作原理:
### 数据交互
IDE的数据交互是通过REPL的输入与输出来完成的。

### EMP-IDE指令集
我们把文件读写，目录遍历诸如之类的基本操作进行了一定的封装，使得在MicroPython上数据能够按照我们规定的函数接口正常的流动。这些指令被封装在 `emp-ext` 模块中，即本项目中的内容，我们暂且称之为`EMP-IDE指令集`。在EMP-IDE上任何可能的图形化界面操作，都可以映射到相应的指令，从而获得我们想要的数据。


## 安装
### 使用upip
该项目已上传至Pypi，我们可以使用`upip`在MicroPython上进行安装，也可以使用`emptool`，通过PC为MicroPython设备进行安装。
在诸如ESP32等一些物联网MCU上你可以很容易的安装`emp`，通过使用`upip`

```python
>>> import upip
>>> upip.install('emp-ext')
```

### 使用emptool

> TODO


## 使用
安装完成之后，你便可以使用如下的指令来开启EMP-IDE指令集，以便EMP-IDE进行调用：

### 串口连接模式
```python
>>> from emp_ide import ide
```
### 无线连接模式
> 在这个模式下，你需要保证你的MicroPython设备，和运行EMP-IDE的PC在同一网络环境下，这一点很重要。

```python
>>> from emp_webide import ide
```
如果你的设备没有连接到网络，那么请注意按照命令行提示，进行网络连接。


### 开机自动加载
如果你想要开机自动加载以上两种的任何一种模式，都很简单：
```python
>>> from emp_utils import set_boot_mode
>>> set_boot_mode()
[0]     Normal
        Normal start
[1]     Turn on WiFi
        Automatically connect to WiFi when booting.
[2]     EMP-IDE-SerialPort
        This mode is for developers. You can use EMP-IDE via serialport connection.
[3]     EMP-IDE-WebSocket
        In this mode, You can use EMP-IDE via websocket connection.
Please input your choice:  [0-3] 
```

[0-3] 分别对应于：
- [0]  正常启动
- [1]  开机启动WiFi，这是一个较为人性化的wifi连接程序
- [2]  开机加载串口连接模式的EMP-IDE指令集
- [3]  开机加载无线连接模式的EMP-IDE指令集



