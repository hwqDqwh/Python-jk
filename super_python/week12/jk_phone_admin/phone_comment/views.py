from django.shortcuts import render
from .models import Comments
from django.db.models import Avg
import datetime


def phone_comment(request):
    """
    展示爬虫获取的手机评论信息
    """

    if request.POST:
        params_agree = request.POST['min_agree'] if not None else 0
        params_opposition = request.POST['min_opposition'] if not None else 0
        search_text = request.POST['search_text'] if not None else 0
        search_date = request.POST['search_date'] if not None else datetime.datetime.date()
    else:
        params_agree, params_opposition, search_text, search_date = (0, 0, '', 0)

    ###  从models取数据传给template  ###
    comments = Comments.objects.filter(
        agree__gte=params_agree,
        opposition__gte=params_opposition,
        comment_content__contains=search_text,
        created_at__contains=search_date,
    )

    # 采集日期处理和去重生成页面的筛选内容
    created_at_list = Comments.objects.values('created_at').distinct()

    created_date_list = []
    for i in created_at_list:
        created_date_list.append(i['created_at'].strftime('%Y-%m-%d'))

    created_date_list = list(set(created_date_list))

    # 评论数量
    counter = Comments.objects.all().count()

    # 平均赞同
    star_avg =f" {Comments.objects.aggregate(Avg('agree'))['agree__avg']:0.1f} "
    # 情感倾向
    sent_avg =f" {Comments.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = Comments.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = Comments.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    return render(request, 'result.html', locals())