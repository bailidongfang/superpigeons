from superpigeons_apps.user.models import UserInfo, UserScore
from django.db.models.aggregates import Sum


class Level():

    def __init__(self, user):
        self.__user = user
        self.__info = UserInfo.objects.get(username=user)
        self.__level = self.__info.level
        self.__score = self.__info.score
        self.__level_list = [
            ['小鸽蛋', 0],
            ['小雏鸽', 100],
            ['小白鸽', 500],
            ['四边白鸽', 1000],
            ['黑顶盖鸽', 2000],
            ['蝴蝶花鸽', 5000],
            ['麒麟花鸽', 10000],
            ['一代鸽王', 50000]
        ]
        self.__level_count = {
            # '类型'：（单次积分，每日上限）
            'a': (50, 50),
            'b': (30, 300),
            'c': (10, 100),
            'd': (5, 50),
        }

    def __get_lev(self, score):
        # 积分为0
        if score <= self.__level_list[0][1]:
            return self.__level_list[0][0]
        # 积分超过最大等级
        if score >= self.__level_list[-1][1]:
            return self.__level_list[-1][0]
        # 除以上情况以外
        for i in self.__level_list:
            if score >= i[1]:
                pass
            else:
                return self.__level_list[self.__level_list.index(i)-1][0]

    def comput_level(self, score_type):
        # type    登陆=a 50分 日上限50
        #         写文章=b 30分 日上限300
        #         评论=c 10分 日上限100
        #         点赞=d 5分 日上线50
        #判断积分是否到达每日上限
        today_score = UserScore.objects.filter(username=self.__user).filter(type=score_type).aggregate(Sum('score'))['score__sum']
        if today_score == None:
            today_score = 0
        if today_score >= self.__level_count[score_type][1]:
            pass
        else:
            # 记录积分明细到UserScore  表
            UserScore.objects.create(username=self.__user, type=score_type, score=self.__level_count[score_type][0])
            # 更新积分到user_info表
            self.__score = self.__score+self.__level_count[score_type][0]
            self.__level = self.__get_lev(self.__score)
            self.__info.level = self.__level
            self.__info.score = self.__score
            self.__info.save()
