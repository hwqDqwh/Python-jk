学习笔记

第一节：
    偏函数
    
    Django 源码
        urlconf
        view
        templete
        model
        
    学习源码
        1. 阅读常用功能
        2. 了解其中各个细节的实现细节,找到其中不会的点
        3. 追踪实现，结合官方文档理解
        4. 尝试自己实现

第二节
    include 源码解读
    利用import_module 导入模块


第三节
    view
        最核心的功能是处理用户请求并组装返回数据

        render 是对 HttpResponse 的进一步封装

        QueryDict
            MultiValueDict
                dict

第四节
    view 的响应请求
        要么返回带内容的请求对象，要么抛出异常

        return HttpResponse('xxx', 'headers') 

        HttpResponse 有众多子类可以选择响应不同的信息

    疑问，课程的 test1 方法，好像我指定的响应头没有生效，还不知道原因真奇怪


第五节
    django 处理请求的流程图
        请求                                           响应
            1. wsgi 协议                            请求和响应都会经过 wsgi，对每个用户生成一个 handle 的句柄
            2. 请求中间件,反扒/CSRF                  请求的 2，3，4 都可以中途截止处理并直接返回
            3. URLConf 和 urls.py 路由
            4. 视图中间件
            5. 视图                                 响应请求还是经过视图响应的，并且也有响应请求的中间件
            6. 模型
            7. 模型的查询管理器，ORM
            8. 上下文，代码封装层面的设计，有点像公共类
            9. 渲染模版                              并返回给模型
        
        django 处理整个请求的过程中，可以随时访问到请求对象 request，其它框架如 flask 则不然（需要通过上下文访问）



第六节 models 的自增主键源码追踪
    Options


第七节 查询管理器

    T1.objects.all()
        from_queryset

第八节 templete

    render()方法进行 html 展示和其中内容的渲染

    它是怎么找到对应的模版目录的:
        render_to_string()
            get_template()
                __engine_list(using) 获取模版引擎列表并初始化引擎
                engine.get_template(template_name) 获取对应的模版文件，engine 是 /django/template/engine.py/Engine 类的实例
                    self.find_template(name, skip=skip)
                        loader.get_template(name, skip=skip)
                            get_app_template_dirs(self.app_dirname)
                        
第九节 模版渲染
    class Template:
        def render():
            return self.template.render() 这里是怎么调用到 site-packages/django/template/base.py 的没有很理解

    四种 token 类型
        1. 变量 开头为{{
        2. 快类型 开头为{%
        3. 注释类型 开头为{#
        4. 其它，文本等字符串
    
    追踪代码时可以借助画图来记录跟踪的代码，串联它们的关系
    追踪过程中要注意关注自己的出发点，不要被细节的代码实现带偏整个逻辑线

第十节 Django web 编程的
    登录模块
        创建管理员账号
            python manage.py createsuperuser
    后台模版
    信号


第十一节 管理表单
    form.py

第十二节 CSRF
    settings.py 的 MIDDLEWARE 打开就可以面向全站 POST 请求进行 CSRF 验证

    单独给个别去掉验证，不建议
        from django.views.decorators.csrf import csrf_exempt, csrf_protect
        @csrf_exempt 修饰方法就可以将请求它的排除在验证之外

    AJAX 提交请求也需要添加 CSRF 验证

第十三节 用户登录认证

第十四节 信号
    两个程序间都对一个逻辑有关联的时候就需要信号，很像 laravel 的事件

    connect 触发方式
    from django.core.signals import request_started
    request_started.connect(my_callback1)

    装饰器触发方式
    from django.dispatch import receiver
    @receiver()
    def func():
        pass


第十五节 中间件
    请求中间件、view 中间件

    全局过滤的系统

    中间件的执行顺序跟随 settings.py 中设置的顺序
    中间件的常见过程
        process_request
        process_view
        process_exception
        process_response

第十六节 周边工具
    gunicorn
        pip install gunicorn
        gunicorn MyDjango.wsgi

        IP 端口 worker处理的进程数(逻辑 CPU 个数)

第十七节 celery

第十八节 celery 定时任务

第十九节 Flask 的上下文和信号介绍

第二十节 Ternado