---
title: 它加密了吗，如加——明日方舟：终末地 资源解密记录
date: 2023-12-30 22:17:36
tags:
---

# 它加密了吗，如加——明日方舟：终末地 CBT1 资源解密记录

~~没啥可说的，鸽了几个月的东西（）~~

## 观察

先看看AB包，这种奇怪后缀肯定加了料 ~~不加我倒立~~

![Alt text](image-1.png)

瞄一下程序行为，读取AB包看起来比较正常，偏移看上去没问题

![Alt text](image.png)

扔进 AssetStudio，改了压缩类型，大概率也做了加密 (和某厂差不多的味道)

![Alt text](image-2.png)

## 分析

这玩意的 UnityPlayer.dll 不仅加了VMP3，也加了不知名压缩壳，我选择直接 dump 出来之后再静态分析 (差了几倍你敢信???)

![Alt text](image-3.png)

找到 `CreateDecompressor`, 果然使用了自定义的flag

![Alt text](image-4.png)

![Alt text](image-5.png)

解压函数一时半会看不出来什么问题，先去看看前面的处理，一般来说不在解压做解密，那就会在读取做解密

![Alt text](image-6.png)

找到 `ArchiveStorageReader::ReadFromStorage`，发现了点问题，直接一个jmp大跳跳到别的函数去读取了

![Alt text](image-7.png)

这个函数实际上就是将读取的工作扔去 `FairGuardProtect.dll` 里面，具体可以看下面 GPT4 的解释

![Alt text](image-8.png)

![Alt text](image-9.png)

![Alt text](image-10.png)

动态一下（其实看堆栈也行），跳转来到了 `FairGuardProtect.dll + 0x26F50`，下面的 `sub_180049950` 一眼就看出是解密函数 ~~废话，那你拿缓冲区内存去干嘛~~

![Alt text](image-11.png)

进去瞄一眼，好嘛，直接明文，加密跟没加一样

![Alt text](image-12.png)

直接把伪代码抄一下，补齐一下依赖的函数，顺利解密

注: 其实 LZ4 解压那边也动了点手脚，但出于版权问题不写完，也算是保护下对方版权－O－

![Alt text](image-13.png)

## 结尾

现在厂商这么有钱了嘛，第二个看到买 Unity 源码改的厂商了（）