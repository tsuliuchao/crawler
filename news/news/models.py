#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc :
"""
import datetime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from news.settings import MYSQL_SHUSHUO_NEWS


Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(MYSQL_SHUSHUO_NEWS)


def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)

def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)


def _get_date():
    return datetime.datetime.now()

class News(Base):
    """定义新闻实体"""
    __tablename__ = "dim_baidu_news"
    # 主键
    id = Column(Integer, primary_key=True)
    # 新闻标题
    m_title = Column(String(120), nullable=True)
    # 正文
    m_json_text = Column(Text, nullable=True)
    # 新闻链接地址
    m_url = Column(String(120), nullable=True)
    # 新闻来源
    m_site = Column(String(60), nullable=True)
    # 发布时间
    m_public_time = Column(Integer)
    # 来源
    m_from = Column(Integer)
