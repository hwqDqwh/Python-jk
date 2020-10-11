学习笔记

第一节

第六节
    函数参数
        *args
        **kargs
    高阶函数
    lambda
        只是表达式，只适合优化简单逻辑
    偏函数
        def add(x, y):
            return x + y
        import functools
        add_1 = functools.partial(add, 1) # 通过 partial 固定第一个参数值
        add_1(2) # 只需要传递第二个参数

        import functools
        g = functools.count()
        next(g) # 每次调用都可以得到 +1 输出
        auto_add_1 = functools.partial(next, g) # 通过偏函数固定处理函数和参数，贼牛逼
        auto_add_1() # 每次调用都有 next(g) 同等效果


第十七节 协程
    特点
        协程是异步的，线程是同步的
        协程是非抢占式的，线程是抢占式的
        协程是主动调度的，线程是被动调度的
        协程可以暂停函数的执行并保留上次执行的状态，是增强型生成器，线程不行
            python 的 yield 很接近协程，区别是 yield 不支持接收输入
        协程是用户级的任务调度，线程是内核级的任务调度
        协程适用于 IO 密集型程序，不适用于 CPU 密集型程序。python 的多线程比较适合 CPU 密集型程序

    await
        import asyncio # 导入包
        async def test():
            await test_2() # await 必须放在 async 关键字修饰的方法中

    事件循环
        程序分配消息的机制


第十八节 aiohttp
    asyncio
    aiohttp

    进程和协程共同使用

    线程和协程不能同时使用，因为 GTL 锁的问题