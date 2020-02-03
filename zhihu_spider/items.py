# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


# 用户信息
class UserInfo(Item):
    id = Field()
    uid = Field()
    url_token = Field()
    name = Field()
    type = Field()
    headline = Field()
    gender = Field()
    follower_count = Field()
    answer_count = Field()
    article_count = Field()
    company = Field()
    job = Field()


# 知乎问题
class Question(Item):
    id = Field()
    qid = Field()
    # 提问者id和url_token
    uid = Field()
    url_token = Field()
    title = Field()
    created_time = Field()


# 知乎回答
class Answer(Item):
    id = Field()
    aid = Field()
    uid = Field()
    url_token = Field()
    qid = Field()
    content = Field()
    created_time = Field()
    updated_time = Field()


# 知乎文章
class Article(Item):
    id = Field()
    arid = Field()
    uid = Field()
    url_token = Field()
    title = Field()
    content = Field()
    created_time = Field()
    updated_time = Field()


# 收藏回答
class CollectAnswer(Item):
    id = Field()
    url_token = Field()
    aid = Field()
    created_time = Field()


# 点赞回答
class AgreeAnswer(Item):
    id = Field()
    url_token = Field()
    aid = Field()
    created_time = Field()


# 关注问题
class FollowQuestion(Item):
    id = Field()
    url_token = Field()
    qid = Field()
    created_time = Field()


# 收藏问题
class CollectQuestion(Item):
    id = Field()
    url_token = Field()
    qid = Field()
    created_time = Field()


# 点赞文章
class AgreeArticle(Item):
    id = Field()
    url_token = Field()
    arid = Field()
    created_time = Field()


# 收藏文章
class CollectArticle(Item):
    id = Field()
    url_token = Field()
    arid = Field()
    created_time = Field()


class RawDataItem(Item):
    json_obj = Field()
