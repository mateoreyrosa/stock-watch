import itertools
import math
import os
import urllib
from time import sleep

import sqlalchemy as sa
from sqlalchemy import Column, String, DECIMAL, Boolean, Integer, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Symbol(Base):
    __tablename__ = 'Symbol'
    Symbol = Column(String, primary_key=True)
    Name = Column(String)
    MarketOpenPrice = Column(DECIMAL(12, 4))
    IsProcessingPrice = Column(Boolean)

class Process(Base):
    __tablename__ = 'Process'
    SymbolsProcessed = Column(Boolean, primary_key=True)
    NumReplicas = Column(Integer)


def createConnection():
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};'
                                     f'SERVER={os.environ["SERVER"]};'
                                     f'DATABASE={os.environ["DATABASE"]};'
                                     f'UID={os.environ["UID"]};'
                                     f'PWD={os.environ["PWD"]};')
    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    Session = sessionmaker(bind=engine)
    return Session()


def get_num_replicas(session):
    while True:
        try:
            result = session.query(Process).first()
            return result.NumReplicas
        except:
            sleep(20)


