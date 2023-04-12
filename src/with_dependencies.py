from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import relationship

sqlite_db = 'sqlite:///imdbtmp.db'

engine = create_engine(sqlite_db, echo=True)

companies_list = {
    "Microsoft",
    "Apple",
    "Google"
}

users_list = {
    "Tom",
    "Bob",
    "John"
}


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", back_populates="company")


Base.metadata.create_all(bind=engine)


def create_users_with_companies(user_list, company_list):
    with Session(autoflush=False, bind=engine) as db:

        companies = []
        users = []

        # создаем компании
        for company in company_list:
            companies.append(Company(name=company))
            print(company)

        print(companies)

        # создаем пользователей
        for user in user_list:
            users.append(User(name=user))
            print(user)

        print(users)

        # устанавливаем для компаний списки пользователей
        for company in companies:
            for user in users:
                if company.name == "Apple":
                    if user.name == "John":
                        company.users = [user]
                        print(f"{company.name} - {user.name}")
                elif company.name == "Microsoft":
                    if user.name == "Tom":
                        company.users = [user]
                        print(f"{company.name} - {user.name}")
                elif company.name == "Google":
                    if user.name == "Bob":
                        company.users = [user]
                        print(f"{company.name} - {user.name}")

        # добавляем компании в базу данных, и вместе с ними добавляются пользователи
        db.add_all(companies)
        db.commit()

        # # можно отдельно добавить объект в список
        # alice = User(name="Alice")
        # google.users.extend([alice])  # добавляем список из одного элемента
        #
        # # можно установить для пользователя определенную компанию
        # sam = User(name="Sam")
        # sam.company = microsoft
        # db.add(sam)
        # db.commit()


def retrieve_user_company():
    with Session(autoflush=False, bind=engine) as db:
        users = db.query(User).all()
        for user in users:
            print(f"{user.name} ({user.company.name})")


def retrieve_company_users():
    with Session(autoflush=False, bind=engine) as db:
        companies = db.query(Company).all()
        for company in companies:
            print(f"{company.name}")
            for user in company.users:
                print(f"{user.name}")


def edit_user_company(company_name: str, user_name: str):
    with Session(autoflush=False, bind=engine) as db:
        # получаем пользователя
        user = db.query(User).filter(User.name == user_name).first()

        # получаем компанию
        company = db.query(Company).filter(Company.name == company_name).first()

        # меняем компанию
        if user is not None and company is not None:
            user.company = company
            db.commit()

        # проверяем изменение
        users = db.query(User).all()
        for u in users:
            print(f"{u.name} - {u.company.name}")


def delete_user_from_company(user_name: str, company_name: str):
    with Session(autoflush=False, bind=engine) as db:
        # получаем пользователя
        tom = db.query(User).filter(User.name == user_name).first()

        # получаем компанию
        google = db.query(Company).filter(Company.name == company_name).first()

        # удаляем из компании
        if user_name is not None and company_name is not None:
            google.users.remove(tom)
            db.commit()

        # проверяем изменение
        users = db.query(User).all()
        for user in users:
            print(f"{user.name} - {user.company.name if user.company is not None else None}")

# create_users_with_companies(users_list, companies_list)
# retrieve_user_company()
# retrieve_company_users()
# edit_user_company("Google", "Tom")
# delete_user_from_company("Bob", "Google")
