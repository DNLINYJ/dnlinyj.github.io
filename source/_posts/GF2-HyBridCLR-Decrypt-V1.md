---
title: HybridCLR C# 方法体解密记录 V1 —— 以23年的少女前线2追放为例
date: 2025-8-27 16:21:22
tags:
---

本来标题我想写 `HybridCLR 标准代码加固解密记录` 的，但考虑到不确定ym是否基于社区版的基础上作的修改，因而作罢

~~不过人家官网上确实有少前2的商业合作案例来着~~

## 初探

在翻文件目录的时候，我发现了在 `GF2_Exilium_Data\StreamingAssets\ClientRes_Windows\Codes` 下有很多 bytes 文件，且文件名都是 Unity 在 Mono 模式编译下的编译产物

![Alt text](image.png)

扔进 dnSpy 看一下，方法识别没有问题，但是方法体里面的 IL 指令全部被混淆，没办法解析

![Alt text](image-1.png)

## 研究

看了一下之前导出的 dump 文件，发现这玩意的解释运行是基于 [HybridCLR](https://hybridclr.doc.code-philosophy.com/) 的

![Alt text](image-2.png)

对于 HybridCLR 的源码解析，知乎有一篇文章写的不错 [【划时代的代码热更新方案——hybridclr源码流程解析】](https://zhuanlan.zhihu.com/p/487599900)

但对于我们调试苦逼人来说，还是官网的指点比较有性价比 () [【官网链接-HybridCLR源码结构及调试】](https://hybridclr.doc.code-philosophy.com/docs/basic/sourceinspect#%E8%B0%83%E8%AF%95)

在官网中提到了，IL层指令集转换在 `HybridCLR/transform/transform.cpp` 的 `HiTransform::Transform` 函数，那么我们就去看看这个函数，多半解密也在这里面

![Alt text](image-3.png)

## 分析

打开 IDA，找到 `HiTransform::Transform`，修一修结构体，一点点对照社区源码 ~~开源的好处~~，发现有一段代码是多出来的

![alt text](image-11.png)

这段代码很明显对 IL 字节码进行了异或解密操作，而解密的 Key 由 `exceptionClausesSize`、`localVarCount` 和 `codeSize` 计算得来

![alt text](image-7.png)

## 解密

照着伪代码把 Key 计算过程和解密过程抄下来，就可以解密了

![alt text](image-8.png)

![alt text](image-9.png)

## 碎碎念

本文其实 2023 年年底就写的差不多了，只是因为懒没写完 :-

![alt text](image-10.png)

最近在逆蓝色原神（bushi）的时候，发现 `HybridCLR` 又换加密算法了，而且比两年前少前二这个还恶心，遂想起这个半成品然后写出来发发 (ˉ﹃ˉ)

今年也高考完了，考得不好去了个双非的信安，悲 :(