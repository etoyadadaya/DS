from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

# List = {
#     'tom': {
#         "name": "tom", "age": 10,
#     },
#     'jack': {
#         "name": "jack", "age": 20,
#     },
# }


sqlite_db = 'sqlite:///imdb.db'

engine = create_engine(sqlite_db, echo=True)


class Base(DeclarativeBase): pass


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)


Base.metadata.create_all(bind=engine)


def add_people(name: str, age: int):
    with Session(autoflush=False, bind=engine) as db:
        person = Person(name=name, age=age)
        db.add(person)
        db.commit()
        db.refresh(person)


def add_many_people(List: list):
    people_list = []

    for guy in List:
        person = Person(name=List[guy]['name'], age=List[guy]['age'])
        people_list.append(person)

    with Session(autoflush=False, bind=engine) as db:
        db.add_all(people_list)
        db.commit()


def retrieve_people():
    with Session(autoflush=False, bind=engine) as db:
        people = db.query(Person).all()
        for p in people:
            print(f"{p.id}.{p.name} ({p.age})")


def get_by_id(_id: int):
    with Session(autoflush=False, bind=engine) as db:
        person = db.get(Person, 1)
        print(f"{person.name} - {person.age}")


def update_person_by_id(_id: int, name: str, age: int):
    with Session(autoflush=False, bind=engine) as db:
        person = db.query(Person).filter(Person.id == _id).first()

        if person is not None:
            print(f"{person.id}.{person.name} ({person.age})")

            # изменениям значения
            person.name = name
            person.age = age

            db.commit()  # сохраняем изменения

            # проверяем, что изменения применены в бд - получаем один объект, у которого имя - Tomas
            result = db.query(Person).filter(Person.id == _id).first()
            print(f"{result.id}.{result.name} ({result.age})")


def delete_person_by_id(_id: int):
    with Session(autoflush=False, bind=engine) as db:
        person = db.query(Person).filter(Person.id == _id).first()
        db.delete(person)
        db.commit()


# add_people("ivan", 20
# retrieve_people()
# add_many_people(List)
# get_by_id(1)
# update_person_by_id(1, "aboba", 100)
# delete_person_by_id(1)
