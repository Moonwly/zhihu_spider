import scrapy
from scrapy.http import Request, Response
from zhihu_spider.settings import *
from zhihu_spider.items import *
from zhihu_spider.misc.tools import config_logger
import json
import re
import time

config_logger()


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    url_user_info_api_format = 'https://www.zhihu.com/api/v4/members/{}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    url_activities_api_format = 'https://www.zhihu.com/api/v4/members/{}/activities?limit=7&desktop=True'
    url_followers_api_format = 'https://www.zhihu.com/api/v4/members/{}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    start_urls = [
        url_user_info_api_format.format('zhang-jia-wei')
    ]

    def __init__(self, **kwargs):
        super(ZhihuSpider, self).__init__(**kwargs)
        self.base_url = 'https://www.zhihu.com'

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url, method='GET', headers=ZHIHU_HEADER, dont_filter=False)

    def parse(self, response: Response):
        text = response.text
        user_info_json = json.loads(text)
        user_info = self.parse_user_info(user_info_json)
        # 检查用户是否被爬取过
        with open("zhihu_spider/txt/user_info.txt") as f:
            user_list = f.read()
            f.close()

        # 用户未被爬取过
        url_token = user_info['url_token']
        uid = user_info['uid']
        if url_token not in user_list:
            with open('zhihu_spider/txt/user_info.txt', 'a', encoding='utf-8') as f:
                f.write(url_token + '\n')
                f.close()
            yield user_info

            activities_url = self.url_activities_api_format.format(url_token)
            yield Request(url=activities_url,
                          callback=self.parse_activities,
                          headers=ZHIHU_HEADER,
                          dont_filter=False,
                          meta={'url_token': url_token,
                                'uid': uid})

            followers_url = self.url_followers_api_format.format(url_token)
            yield Request(url=followers_url,
                          callback=self.parse_followers,
                          headers=ZHIHU_HEADER,
                          dont_filter=False,
                          meta={'url_token': url_token,
                                'uid': uid})

    def parse_user_info(self, user_info_json):
        user_info = UserInfo()
        items = user_info_json.items()
        for key, value in items:
            if key == 'id':
                user_info['uid'] = value
            elif key == 'url_token':
                user_info['url_token'] = value
            elif key == 'name':
                user_info['name'] = value
            elif key == 'type':
                user_info['type'] = value
            elif key == 'headline':
                user_info['headline'] = value
            elif key == 'gender':
                user_info['gender'] = value
            elif key == 'follower_count':
                user_info['follower_count'] = value
            elif key == 'answer_count':
                user_info['answer_count'] = value
            elif key == 'article_count':
                user_info['article_count'] = value
            elif key == 'employments':
                all_employments = value
                if len(all_employments) < 1:
                    pass
                else:
                    employment_info = all_employments[0]
                    if employment_info.get('company', ''):
                        user_info['company'] = employment_info.get('company').get('name', '')
                    if employment_info.get('job', ''):
                        user_info['job'] = employment_info.get('job').get('name', '')
            else:
                pass

        return user_info

    def parse_activities(self, response: Response):
        url_token = response.meta['url_token']
        uid = response.meta['uid']
        json_text = response.text
        activities_json = json.loads(json_text)
        paging = activities_json['paging']
        data = activities_json['data']
        if data:
            for action in data:
                # 回答问题
                if action['verb'] == 'ANSWER_CREATE':
                    answer = Answer()
                    target = action.get('target', '')
                    if target:
                        answer['uid'] = uid
                        answer['url_token'] = url_token
                        answer['aid'] = target.get('id', '')
                        answer['qid'] = target.get('question', '').get('id', '')
                        answer['content'] = self.clean_content(target.get('content', ''))
                        answer['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                               time.localtime(target.get('created_time', '')))
                        answer['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                               time.localtime(target.get('updated_time', '')))

                    if not self.check_if_got_answer(str(answer['aid'])):
                        yield answer

                # 点赞回答
                elif action['verb'] == 'ANSWER_VOTE_UP':
                    answer = Answer()
                    target = action.get('target', '')
                    if target:
                        author = target.get('author', '')
                        if author:
                            answer['uid'] = author.get('id', '')
                            answer['url_token'] = author.get('url_token', '')
                        answer['aid'] = target.get('id', '')
                        answer['qid'] = target.get('question', '').get('id', '')
                        answer['content'] = self.clean_content(target.get('content', ''))
                        answer['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                               time.localtime(target.get('created_time', '')))
                        answer['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                               time.localtime(target.get('updated_time', '')))

                        if not self.check_if_got_answer(str(answer['aid'])):
                            yield answer

                    agree_answer = AgreeAnswer()
                    agree_answer['url_token'] = url_token
                    agree_answer['aid'] = answer['aid']
                    agree_answer['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                 time.localtime(action.get('created_time', '')))
                    yield agree_answer

                # 提出问题
                elif action['verb'] == 'QUESTION_CREATE':
                    question = Question()
                    target = action.get('target', '')
                    if target:
                        question['uid'] = uid
                        question['url_token'] = url_token
                        question['qid'] = target.get('id', id)
                        question['title'] = target.get('title', '')
                        question['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                 time.localtime(target.get('created', '')))

                        if not self.check_if_got_question(str(question['qid'])):
                            yield question

                # 关注问题
                elif action['verb'] == 'QUESTION_FOLLOW':
                    question = Question()
                    target = action.get('target', '')
                    if target:
                        author = target.get('author', '')
                        if author:
                            question['uid'] = author.get('id', '')
                            question['url_token'] = author.get('url_token', '')
                        question['qid'] = target.get('id', '')
                        question['title'] = target.get('title', '')
                        question['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                 time.localtime(target.get('created', '')))

                        if not self.check_if_got_question(str(question['qid'])):
                            yield question

                    follow_question = FollowQuestion()
                    follow_question['url_token'] = url_token
                    follow_question['qid'] = question['qid']
                    follow_question['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                    time.localtime(action.get('created_time', '')))
                    yield follow_question

                # 发表文章
                elif action['verb'] == 'MEMBER_CREATE_ARTICLE':
                    article = Article()
                    target = action.get('target', '')
                    if target:
                        article['uid'] = uid
                        article['url_token'] = url_token
                        article['arid'] = target.get('id', '')
                        article['title'] = target.get('title', '')
                        article['content'] = self.clean_content(target.get('content', ''))
                        article['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.localtime(target.get('created', '')))
                        article['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.localtime(target.get('updated', '')))

                        if not self.check_if_got_article(str(article['arid'])):
                            yield article

                # 点赞文章
                elif action['verb'] == 'MEMBER_VOTEUP_ARTICLE':
                    article = Article()
                    target = action.get('target', '')
                    if target:
                        author = target.get('author', '')
                        if author:
                            article['uid'] = author.get('id', '')
                            article['url_token'] = author.get('url_token', '')
                        article['arid'] = target.get('id', '')
                        article['title'] = target.get('title', '')
                        article['content'] = target.get('content', '')
                        article['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.localtime(target.get('created', '')))
                        article['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                time.localtime(target.get('updated', '')))

                        if not self.check_if_got_article(str(article['arid'])):
                            yield article

                    agree_article = AgreeArticle()
                    agree_article['url_token'] = url_token
                    agree_article['arid'] = article['arid']
                    agree_article['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                  time.localtime(action.get('created_time', '')))
                    yield agree_article

        if paging and not paging['is_end']:
            next_url = paging['next']
            yield Request(url=next_url,
                          callback=self.parse_activities,
                          headers=ZHIHU_HEADER,
                          dont_filter=False,
                          meta={'url_token': url_token, 'uid': uid})

    def parse_followers(self, response: Response):
        url_token = response.meta['url_token']
        uid = response.meta['uid']
        json_text = response.text
        follower_json = json.loads(json_text)
        paging = follower_json['paging']
        data = follower_json['data']

        if data:
            for user in data:
                followers_url_token = user['url_token']
                yield Request(url=self.url_user_info_api_format.format(followers_url_token),
                              callback=self.parse,
                              headers=ZHIHU_HEADER,
                              dont_filter=False)

        if paging and not paging['is_end']:
            next_url = paging['next']
            yield Request(url=next_url,
                          callback=self.parse_followers,
                          headers=ZHIHU_HEADER,
                          dont_filter=False,
                          meta={'url_token': url_token,
                                'uid': uid})

    # 检查问题是否被爬取过
    def check_if_got_question(self, qid):
        with open("zhihu_spider/txt/question.txt") as f:
            question_list = f.read()
            f.close()
        # 问题未被爬取过
        if qid not in question_list:
            with open('zhihu_spider/txt/question.txt', 'a', encoding='utf-8') as f:
                f.write(qid + '\n')
                f.close()
            return False
        else:
            return True

    # 检查回答是否被爬取过
    def check_if_got_answer(self, aid):
        with open("zhihu_spider/txt/answer.txt") as f:
            answer_list = f.read()
            f.close()
        # 问题未被爬取过
        if aid not in answer_list:
            with open('zhihu_spider/txt/answer.txt', 'a', encoding='utf-8') as f:
                f.write(aid + '\n')
                f.close()
            return False
        else:
            return True

        # 检查问题是否被爬取过

    # 检查文章是否被爬取过
    def check_if_got_article(self, arid):
        with open("zhihu_spider/txt/article.txt") as f:
            article_list = f.read()
            f.close()
        # 问题未被爬取过
        if arid not in article_list:
            with open('zhihu_spider/txt/article.txt', 'a', encoding='utf-8') as f:
                f.write(arid + '\n')
                f.close()
            return False
        else:
            return True

    # 清除html标签
    def clean_content(self, html_content):
        return re.sub('<[^<]+?>', '', html_content).replace('\n', '').replace('&nbsp;', '').strip()
