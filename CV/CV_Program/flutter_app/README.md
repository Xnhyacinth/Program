## flutter-app

### 环境

- 安装依赖 `pip install -r ./py/requirements.txt -i https://mirrors.aliyun.com/pypi/simple`

- 视频放入 `./py`目录，修改视频名称为`source.mp4`

- 依次运行获取位置文件

- > python ./py/1.frames.py

- > python ./py/2.discern.py

- > python ./py/3.translate.py

- 或者通过深度学习获取的蒙版文件转换为xml封装为json提供给flutter前端，后续利用flutter实现弹幕调度动画组

### python后端
1.1 提取关键帧
  在这份配置文件中，会先读取视频的帧率，30FPS的视频会吧每一帧都当做关键帧进行处理，60FPS则会隔一帧处理一次，这样是为了保证Flutter在绘制蒙版的性能统一

1.2 逐帧提取
   这里使用opencv提取视频的关键帧图片并保存在当前目录images文件夹下

1.3 提取人物
   ![1650532388_1_.png](https://s2.loli.net/2022/04/21/SezNPwTJ12kiuG9.png)

1.4 像素转换，生成轮廓
   ![invert-clip-frame4.jpg](https://s2.loli.net/2022/04/21/EmCnYyS4x1UhzaA.jpg)
   对每一个人物关键帧进行计算，这里就是一层层的像素操作。opencv会把图片像素点生成numpy三维矩阵，计算速度快，操作起来便捷，比如我们要把一个三维矩阵gray_in的灰度图黑白像素对换，只需要gray = 255 - gray_in就可以得到一个新的矩阵而不需要用python语言来循环。

   最后把计算出的帧的闭包图形路径转换为普通的多维数组类型并存入配置文件Map<key, value>，key为视频的进度时间ms，value为闭包路径（就是图中白色区域的包围路径，排除黑色人物区域），是一个二维数组，因为一帧里会有n个闭包路径组成。另外还要将视频信息存入配置文件，其中frame_cd就是告诉flutter每间隔多少ms切换下一帧蒙版，视频的宽高分辨率用于flutter初始化播放器自适应布局。

   具体JSON数据结构可见下方图片。现在我们已经得到了一个res.json的配置文件，里面包含了该视频关键帧数据的裁剪坐标集，接下来就用flutter去剪纸吧

   ![1650532762_1_.png](https://s2.loli.net/2022/04/21/kEYimwQBoFxV6pf.png)


### flutter 前端
2.1 弹幕调度动画组
   弹幕调度系统各端实现都大同小异，只是动画库的API方式区别。flutter里使用SlideTransition可以实现单条弹幕文字的动画效果
2.2 裁剪蒙版容器
   正式环境肯定是从网络http长连接或者socket获取实时数据，由于我们是离线演示DEMO，方便起见需要在初始化时加载刚才后端产出蒙版路径res.json打包到APP中
   flutter实现蒙版效果的核心就在于CustomClipper类，它允许我们通过Path对象来自定义坐标绘制一个裁剪路径（类似于canvas绘图），我们创建一个MaskPath，并在里面绘制我们刚才加载的配置文件的那一帧，然后通过ClipPath包裹弹幕外层容器
2.3 视频流蒙版同步
   考虑到IOS和Android插件的稳定性，用flutter官方提供的播放器插件video_player
   在video初始化后，通过addListener开始监听播放进度。当播放进度改变时候，获取当前的进度毫秒，去寻找与当前进度最接近的配置文件中的数据集stepsTime，这个配置的蒙版就是当前播放画面帧的裁剪蒙版，此时立刻通过eventBus.fire通知蒙版容器用key为stepsTime的数组路径进行重绘。校准蒙版

