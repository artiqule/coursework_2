import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker, relationship


Base = declarative_base()
engine = sq.create_engine('postgresql+psycopg2://********:*********@localhost:5432/vkinder')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "user"
    id_vk = sq.Column(sq.Integer, primary_key=True)
    action = sq.Column(sq.String, nullable=True, unique=False)
    name = sq.Column(sq.String, nullable=False, unique=False)
    token = sq.Column(sq.String, nullable=False, unique=True)
    id_search = relationship("SearchQueries", backref="user")


class SearchQueries(Base):
    __tablename__ = "queries"
    id = sq.Column(sq.Integer, primary_key=True)
    id_response = sq.Column(sq.Integer, nullable=False, unique=False)
    id_queries = sq.Column(sq.Integer, sq.ForeignKey("user.id_vk"))


def create_table():
    tabeles = (User.__tablename__, SearchQueries.__tablename__)
    for table_name in tabeles:
        if table_name in engine.table_names():
            return True
        else:
            Base.metadata.create_all(engine)




