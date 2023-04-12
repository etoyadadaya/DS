import pandas
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Session

sqlite_db = 'sqlite:///top250.db'
engine = create_engine(sqlite_db, echo=True)


class Base(DeclarativeBase): pass


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer)
    name = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    genre = Column(String)
    certificate = Column(String)
    duration = Column(String)


Base.metadata.create_all(bind=engine)


def parse_csv():
    data = {}
    rank: int
    year: int
    rating: float
    name: str
    genre: str
    certificate: str
    duration: str

    csv_data = pandas.read_csv('data.csv')
    frame = pandas.DataFrame(csv_data)
    values = frame.values.tolist()

    for value in values:
        data[value[0]] = {
            "rank": value[0],
            "name": value[1],
            "year": value[2],
            "rating": value[3],
            "genre": value[4],
            "certificate": value[5],
            "duration": value[6]
        }

    return data


def add_movies(movies_list):
    zipped_movies_list = []

    for movie in movies_list:
        film = Movie(
            rank=movies_list[movie]['rank'],
            name=movies_list[movie]['name'],
            year=movies_list[movie]['year'],
            rating=movies_list[movie]['rating'],
            genre=movies_list[movie]['genre'],
            certificate=movies_list[movie]['certificate'],
            duration=movies_list[movie]['duration'],
        )
        zipped_movies_list.append(film)

    with Session(autoflush=False, bind=engine) as db:
        db.add_all(zipped_movies_list)
        db.commit()


def retrieve_movies():
    with Session(autoflush=False, bind=engine) as db:
        movies = db.query(Movie).all()
        for movie in movies:
            print(f"id: {movie.id},"
                  f" name: {movie.name},"
                  f" year: {movie.year},"
                  f" rating: {movie.rating},"
                  f" genre: {movie.genre},"
                  f" certificate: {movie.certificate},"
                  f" duration: {movie.duration}"
                  )


def retrieve_movie_by_id(_id: int):
    with Session(autoflush=False, bind=engine) as db:
        movie = db.get(Movie, 1)
        print(f"{movie.name}")


def data_processing():
    movies_list = parse_csv()
    add_movies(movies_list)


def three_dimensional_visualization():
    df = pandas.read_csv("data.csv")
    labels = ["Rating", "Rank", "Year"]

    fig = plt.figure()
    fig.set_size_inches(6, 6)
    ax = fig.add_subplot(111, projection="3d")

    x = df["rating"]
    y = df["rank"]
    z = df["year"]

    for l in labels:
        rating =  ax.set_xlabel("Rating")
        place = ax.set_ylabel("Rank")
        year = ax.set_zlabel("Year")
        ax.scatter(x, y, z, label=l)

    ax.grid(False)
    ax.legend(loc="best")

    plt.show()


three_dimensional_visualization()

# retrieve_movie_by_id(1)
# retrieve_movies()
# data_processing()
# result = parse_csv()
# print(result)
