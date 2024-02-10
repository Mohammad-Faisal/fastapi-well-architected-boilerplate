# Creating a well architected Fast API application

First create the project directory and navigate to it.

```bash
mkdir fastapi-well-architected-boilerplate
cd fastapi-well-architected-boilerplate
```

Then create the following directories and files:

```bash
mkdir -p src/{api,core,db}
touch src/__init__.py
touch src/{main}.py
```

The project structure should look like this:

```bash
.
├── src
│   ├── main.py
└── README.md
```

The `src` directory contains the main application code. 

The `main.py` file is the entry point of the application.

## Create virtual environment and install dependencies

Create a virtual environment and install the required dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the two dependencies `fastapi` and `uvicorn` using the following command:

```bash
pip3 install fastapi uvicorn
```

- The `fastapi` package is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. 

- The `uvicorn` package is a lightning-fast ASGI server implementation, using uvloop and httptools.

And create a `requirements.txt` file to store the dependencies.

```bash
pip3 freeze > requirements.txt
```

Add the following code into the `src/main.py` file.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

And run the application using the following command:

```bash
uvicorn src.main:app --reload
```

Now open your browser and navigate to `http://localhost:8000/docs` to see the API documentation.

## Different environments anc configuration settings

The application will have different environments such as development, testing, and production. Each environment will have its own configuration settings. 

The configuration settings will be stored in a `.env` file in the root directory of the project. The `.env` file will contain the following settings:

```bash
# .env
ENV=development
DATABASE_URL=sqlite:///./test.db
```

The `ENV` setting will be used to determine the current environment. The `DATABASE_URL` setting will be used to connect to the database. The `DATABASE_URL` setting will be different for each environment.

Let's install the `pydantic-settings` package to load the configuration settings from the `.env` file.

```bash
pip3 install pydantic-settings
```

The `src/config.py` file contains the following code:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"
        
settings = Settings()
```

The `Settings` class contains the configuration settings. The `Config` class is used to load the settings from the `.env` file.

Now you can print the configuration settings using the following code:

```python
from src.config import settings

print(settings.ENV)
print(settings.DATABASE_URL)
```

## Format the code using Black

The `black` package is a Python code formatter. It will format the code according to the Python PEP 8 style guide.

Install the `black` package using the following command:

```bash
pip3 install black
```

And create a `pyproject.toml` file in the root directory of the project with the following content:

```bash
[tool.black]
line-length = 88
target-version = ['py37']
```

The `pyproject.toml` file contains the configuration settings for the `black` package. The `line-length` setting is used to specify the maximum line length. The default is 88 but you can change it to any value you want.

The `target-version` setting is used to specify the Python version.

Now you can format the code using the following command:

```bash
black src
```

This command will format the code in the `src` directory.

Now black is great for formatting the code but it can be a bit too aggressive. If you want to see what changes it would make without actually making them, you can use the `--diff` option:

```bash
black --diff src
```

If you want to see what changes it would make without actually making them, you can use the `--check` option:

```bash
black --check src
```

Also black focuses more on the code formatting. If you want to check the code for style and programming errors, you can use the `flake8` package.

## Lint the code using Flake8

The `flake8` package is a Python code linter. It will check the code for style and programming errors.

Install the `flake8` package using the following command:

```bash
pip3 install flake8
```

And create a `.flake8` file in the root directory of the project with the following content:

```bash
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```

The `.flake8` file contains the configuration settings for the `flake8` package. The `max-line-length` setting is used to specify the maximum line length. The `extend-ignore` setting is used to ignore the `E203` and `W503` errors.


Now you can lint the code using the following command:

```bash
flake8 src
```

This command will lint the code in the `src` directory.

## Database models and migrations

The application will use the `SQLModel` package to work with the database. 

This is built on top of SQLAlchemy and Pydantic. It will allow us to define the database models using Python type hints.

Install the `SQLAlchemy` package using the following command:

```bash
pip3 install sqlmodel
```

The `src/database.py` file contains the following code:

```python
from sqlmodel import create_engine, Session
from src.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

This code creates a database engine and a session. The `get_session` function is used to get the session.


## Create our first model

Now let's create our first database model. We will create separate domains for each domain in the application.

Let's create our user domain

```bash 
touch src/api/user/{__init__.py,models.py}
```

This will create the following structure:

```bash
.
├── src
│   ├── api
│       ├── user
│           ├── __init__.py
│           ├── models.py
# ... the other stuff
└── README.md
```

Then create the user model using the following code.

```python
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str
    email: str
    password: str
```

The `User` class is a database model. It inherits from the `SQLModel` class. 

The `id` field is the primary key. The `username`, `email`, and `password` fields are the columns in the database table.

Now we have the models but we need to create the database tables.

## Database migrations with Alembic

The `Alembic` package is a database migration tool for SQLAlchemy. It will create the database and tables in the production environment.

Install the `Alembic` package using the following command:

```bash
pip3 install alembic
```

Then you can run the following command to initialize alembic.

```bash
alembic init migrations
```

This will create a `migrations` directory in the root directory of the project.

The `migrations` directory contains the following structure:

```bash
.
├── migrations
│   ├── README
│   
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
```

Notice that it will also create a `alembic.ini` file in the root directory of the project.

```bash
[alembic]
# other configs
sqlalchemy.url = driver://user:pass@localhost/dbname
```

You need to specify the `sqlalchemy.url` setting in the `alembic.ini` file. This setting is used to connect to the database.

Then edit the `env.py` file and add the following line to the section [target_metadata]:

```sh
from src.database import SQLModel
target_metadata = SQLModel.metadata
```

Then open the `script.py.mako` file and add the following at the top

```
import sqlmodel
```

Now we are ready to run our first migration.

```bash
alembic revision --autogenerate -m "Initial migration"
```

This command will create a new migration file in the `migrations/versions` directory.

Now you can run the migration using the following command:

```bash
alembic upgrade head
```

This command will create the database and tables in the production environment.

But wait, we are not in the production environment yet. We are still in the development environment. So we need to create a separate configuration file for the development environment.

## Create a separate configuration file for the development environment

Create a `development.env` file in the root directory of the project with the following content:

```bash
# development.env
ENV=development
DATABASE_URL=sqlite:///./test.db
```

The `development.env` file contains the configuration settings for the development environment.

Now you can run the application using the following command:

```bash
uvicorn src.main:app --reload --env-file .development.env
```

This command will run the application in the development environment.

For local development we need a local database. And we can use docker to create a local database. It will greatly improve the local development experience.

## Create a local database using Docker

Let's see how we can use docker-compose to create a local database and run the local server from the same file. 

This will allow us to run the application and the database using a single command.

First, install Docker and Docker Compose on your machine.

Then create the base `Dockerfile` in the root directory of the project with the following content:

```bash
FROM python:3.12.1-alpine3.18

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG DATABASE_URL DATABASE_URL="default_values"
ARG OPEN_AI_SECRET_KEY="default_values"
ARG PORT
# Expose the port your FastAPI app will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

You can deploy your application anywhere with this docker file.

Then create a `docker-compose.yml` file in the root directory of the project with the following content:

```bash
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: test
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    command: uvicorn src.main:app --reload --env-file .development.env --host 0.0.0.0 --port 8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/test
    depends_on:
      - db

volumes:
    postgres_data:
```

The `db` service is used to create the database. It uses the `postgres:13` image. The `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` settings are used to create the database.

The `app` service is used to run the application. It uses the `uvicorn` command to run the application. The `--env-file .development.env` setting is used to load the configuration settings from the `development.env` file.


## Database credentials

In this configuration our local database url will be `postgresql://user:password@localhost:5432/test`

But in the docker file we used `DATABASE_URL=postgresql://user:password@db:5432/test` because in this context the database is a service and the host is `db`.

You can update the `.development.env` file to use the new database url in case we want to access it from the local machine.

```env
# .development.env
ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/test
```

Also don't forget to upgrade the `alembic.ini` file to use the new database url.

```ini
[alembic]
# other configs
sqlalchemy.url = postgresql://user:password@localhost:5432/test
```

Now you can run the application and the database using the following command:

```bash
docker-compose up
```

This command will create the database and run the application.

Now you can run your first migration on the local database using the following command:

```bash
alemibc revision --autogenerate -m "Initial migration"
```

This command will create a new migration file in the `migrations/versions` directory.

Now you can run the migration using the following command:

```bash
alembic upgrade head
```

Now if you visit your local database you will see the `user` table.

## Create the user API

Now let's create the user API. We will create a router for the user domain.

Create a `router.py` file in the `src/api/user` directory with the following content:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
```

The `router` object is an instance of the `APIRouter` class. It is used to define the routes for the user domain.

Now you can add the user router to the main application using the following code:

```python
from fastapi import FastAPI

from src.api.user.router import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
```

But we don't want to deal with dummy data. Instead we want to use the database to store and retrieve the users.

## Create the user service

Create a `service.py` file in the `src/api/user` directory with the following content:

```python
from fastapi import Depends
from src.database import get_session
from src.api.user.models import User
from sqlmodel import  select, Session


class UserService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_users(self):
        statement = select(User)
        users = self.session.exec(statement).all()
        return users
```

The `get_users` function is used to get the users from the database. Also we are initializing the session in the constructor.

Now you can use the `get_users` function in the user router using the following code:

```python
from fastapi import APIRouter, Depends

from src.api.user.service import UserService

router = APIRouter()

@router.get("/")
async def read_users(user_service : UserService = Depends()):
    users = user_service.get_users()
    return users
```

Notice that we are using the `Depends` function to inject the `UserService` object into the `read_users` function.

Now you can run the application and navigate to `http://localhost:8000/users` to see the users.

## Create a user.

Now let's create another function to create a user. But before that we need to create the request and response models.

Create a new file named `schems.py` in the `src/api/user` directory with the following content:

```python
from pydantic import BaseModel

class UserCreateInput(BaseModel):
    name: str
    email: str
    password: str
```

Then update the `service.py` file to include the `create_user` function.

```python
def create_user(self, user_create_input):
        user = User(**user_create_input.model_dump())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
```

Finally add the route.

```python
from fastapi import APIRouter, Depends

from src.api.user.service import UserService

router = APIRouter()

@router.get("/")

async def read_users(user_service : UserService = Depends()):
    users = user_service.get_users()
    return users

@router.post("/")
async def create_user(user_create_input: UserCreateInput, user_service : UserService = Depends()):
    user = user_service.create_user(user_create_input)
    return user
```

Now if you go to the terminal and send the following post request

```
curl -X 'POST' \
  'http://localhost:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Mohammad Faisal",
  "email": "mohammadfaisal1011@gmail.com",
  "password": "faisal"
}'
```

You will receive the following response with the success message!

## Get the details of a user.

Now let's create another function to get the details of a user.

For this we don't need any request schema as we will be using the user id to get the details.

```python
@router.get("/{user_id}")
async def read_user(user_id: int, user_service : UserService = Depends()):
    user = user_service.get_user(user_id)
    return user
```

Then remember to add the function in the service.

```python
def get_by_id(self, user_id: int):
    statement = select(User).where(User.id == user_id)
    user = self.session.exec(statement).one()
    return user
```

But we need to handle the case when the user is not found.

```python
from sqlmodel import select, Session, SQLModel

class UserService:
    def get_by_id(self, user_id: int):
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).one_or_none()
        if user is None:
            raise Exception("User not found")
        return user
```

Now this check will raise an exception if the user is not found.

But we need to handle this exception in the router.

```python
from fastapi import APIRouter, Depends, HTTPException

from src.api.user.service import UserService

router = APIRouter()

@router.get("/")

async def read_users(user_service : UserService = Depends()):
    users = user_service.get_users()
    return users

@router.post("/")
async def create_user(user_create_input: UserCreateInput, user_service : UserService = Depends()):
    user = user_service.create_user(user_create_input)
    return user

@router.get("/{user_id}")
async def read_user(user_id: int, user_service : UserService = Depends()):
    try:
        user = user_service.get_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
```

Now you will receive a 404 error if the user is not found.

## Update the user.

Now let's create another function to update the user.

For this we need to create a request schema.

```python
class UserUpdateInput(BaseModel):
    name: str
    email: str
    password: str
```

Then update the `service.py` file to include the `update_user` function.

```python
def update_user(self, user_id, user_update_input):
    statement = select(User).where(User.id == user_id)
    user = self.session.exec(statement).one()
    for key, value in user_update_input.dict().items():
        setattr(user, key, value)
    self.session.add(user)
    self.session.commit()
    self.session.refresh(user)
    return user
```

Finally add the route.

```python
@router.put("/{user_id}")
async def update_user(user_id: int, user_update_input: UserUpdateInput, user_service : UserService = Depends()):
    try:
        user = user_service.get_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
```

Now you can see that we have added the check for the user. If the user is not found we will raise a 404 error.

Now this is a duplicate code. We can move this check to the service.

We can use the concept of dependencies to create a dependency that will check if the user exists.

Create a new file named `dependencies.py` in the `src/api/user` directory with the following content:

```python
from fastapi import HTTPException, Depends

from src.api.user.service import UserService

def get_user(user_id: int, user_service: UserService = Depends()):
    user = user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

Then update the `router.py` file to include the `get_user` dependency.

```python
@router.get("/{user_id}")
async def read_user(
    user_id: int,
    user_service: UserService = Depends(),
    user: Mapping = Depends(get_user),
):
    user = user_service.get_by_id(user_id)
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update_input: UserUpdateInput,
    user_service: UserService = Depends(),
    user: Mapping = Depends(),
):
    user = user_service.update(user_id, user_update_input)
    return user

```

Now you can see that we are using the `get_user` dependency to check if the user exists. And you can do the same. Now you don't have any duplications.

## Delete the user.

Now let's create another function to delete the user.

Then update the `service.py` file to include the `delete_user` function.

```python
def delete_user(self, user_id):
    statement = select(User).where(User.id == user_id)
    user = self.session.exec(statement).one()
    self.session.delete(user)
    self.session.commit()
    return user
```

Finally add the route.

```python
@router.delete("/{user_id}")
async def delete_user(user_id: int, user_service : UserService = Depends()):
    user = user_service.delete(user_id)
    return user
```