 # 防挡弹幕

![1649671958_1_.png](https://s2.loli.net/2022/04/11/P3jD9ukh576tNln.png)




## 一、硬件：

* Windows10或11（无需GPU，有最好）或MacOS 都测试可行

## 二、软件：

* Python==3.8/3.7
* TensorFlow
* imgaug
* opencv 
* pixellib

## 二、用法：

```
optional arguments:
  -h, --help     show this help message and exit
  --video VIDEO  要处理的视频
  --mode MODE    运行模式：mask_i,mask_s,compound 对应：生成蒙版图片(实例分割)、语义分割合成视频
  --danmu DANMU  弹幕文本文件
```



### 2.1、下载相关文件

* 2.1.1 下载字体 `MSYH.ttc` 至 `./fonts`目录下，[下载地址点这里](https://github.com/Xnhyacinth/xnhyacinth/releases/tag/Fonts)
* 2.1.2 下载预训练模型 `mask_rcnn_coco.h5`和`deeplabv3_xception_tf_dim_ordering_tf_kernels.h5`至`./weights`目录下，[deeplabv3下载点这里](https://download.csdn.net/download/ixuyn/85194774?spm=1001.2014.3001.5503)  [mask_rcnn下载点这里](https://download.csdn.net/download/ixuyn/85194933)
* 2.1.3 下载演示视频`1.demo.mp4`至`./videos`目录下，[下载地址点这里](https://github.com/Xnhyacinth/xnhyacinth/releases/tag/Media)

### 2.2、生成蒙版文件

命令：`python demo.py --video={mp4视频地址} --mode=mask_i`，如`python demo.py --video='./videos/1.mp4' --mode=mask_i`，系统会在`mask_img`文件夹下生成每帧画面的蒙版图，类似下图：

![1649671845_1_.png](https://s2.loli.net/2022/04/11/dMIZlPJkpEHsuGU.png)



### 2.3、合成弹幕视频

命令：`python demo.py --video={视频地址} --mode=compound --danmu={弹幕txt文件地址}`，如：`python demo.py --video='./videos/1.mp4' --mode=compound --danmu=danmu.txt`，渲染后的视频在`record_video`目录下。



