from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from typing import List


class ActionRequest(BaseModel):
    '''
        Example:
        `{
            "movie_id" : 123,
            "user_id" : 12,
            "rate" : 4.5
        }`
    '''
    movie_id : int
    user_id : int
    rate : float
    genres : List[str]
    tags : List[str]

class MovieInfo(BaseModel):
    '''
        Example:
        `{
            "movie_id" : 123,
            "genre" : "Thriller",
            "avg_rate" : 3.9
        }`
    '''
    movie_id : int
    genre : str
    avg_rate : float

class UserInfo(BaseModel):
    '''
        {
            "user_id": 123,
            "avg_rating": 4.1,
            "genres_preference": {
                                    "Action": 0.8, 
                                    "Comedy": 0.6
                                },
            "tags_preference":  {
                                    "thrilling": 0.9, 
                                    "funny": 0.7
                                },
            "svd_vector": [0.62, 0.71, 0.41]
        }
    '''
    user_id : int
    avg_rating: float
    genres_preference : dict
    tags_preference : dict
    svd_vector : List[float]


Base = declarative_base()

class UserInfoDB(Base):
    __tablename__ = "user_info"

    user_id = Column(Integer, primary_key=True, index=True)
    avg_rating = Column(Float, nullable=False)
    genres_preference = Column(JSON, nullable=False)
    tags_preference = Column(JSON, nullable=False)
    svd_vector = Column(ARRAY(Float), nullable=False)
