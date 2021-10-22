# Alembic database migrations

I initially didnt want to write about this because implementing database migrations with alembic turned out to be pretty simple and there is so many guides for it out there. Eventually when i was trying to install our application on a new virtual machine for some performance testing i encountered some issues that the guides i saw didnt warn me about so now i feel that i have something worth writing about. I will go into the issues i found and how to avoid them in a moment.

To implement alembic in my project i mostly followed the [official tutorial for alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) and i looked at the [fastapi full-stack cookiecutter](https://github.com/tiangolo/full-stack-fastapi-postgresql) for specific implementation examples.

Initializing alembic is as simple as running `alembic init alembic` if you used apt to install it or `python3 -m alembic init alembic` if you used pip. This will create `alembic` directory with all of the boilerplate code needed for the migrations. Note that you should run this command where you want your alembic folder to be. I did this "next to" the folder that contains all my python code.

```bash
vagrant@vagrant:~/Bookstore-Project/fastapi_backend/app$ python3 -m alembic init alembic
  Creating directory /home/vagrant/Bookstore-Project/fastapi_backend/app/alembic ...  done
  Creating directory /home/vagrant/Bookstore-Project/fastapi_backend/app/alembic/versions ...  done
  Generating /home/vagrant/Bookstore-Project/fastapi_backend/app/alembic/script.py.mako ...  done
  Generating /home/vagrant/Bookstore-Project/fastapi_backend/app/alembic/README ...  done
  Generating /home/vagrant/Bookstore-Project/fastapi_backend/app/alembic.ini ...  done
  Generating /home/vagrant/Bookstore-Project/fastapi_backend/app/alembic/env.py ...  done
  Please edit configuration/connection/logging settings in '/home/vagrant/Bookstore-Project/fastapi_backend/app/alembic.ini' before
  proceeding.
```

In the `alembic.ini` file that was generated i commented out the line with `sqlalchemy.url = driver://user:pass@localhost/dbname` because it will be set in `alembic/env.py`. Thats where you will have to really configure alembic to use your application.

I am getting my database credentials and address from the environment variables so i imported the `os` library to access those.

```python
import os
```

Next the `target_metadata` has to be defined. This variable will need to know you database schema. This is done by giving it `Base.metadata` from your code. I am not sure how the order works exactly here but essentially the `Base` class needs to actually have the schema so if you are importing it from the file where you declared the `Base` variable it might not have the information it needs to have. In my case i have a `models.py` file where i am creating all of my models for sqlalchemy so that is where i am importing it from.

```python
from app import models
target_metadata = models.Base.metadata
```

Now to define the database url i used the function i found in [the fastapi coociecutter](https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/alembic/env.py).

```python
def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql://{user}:{password}@{server}/{db}"
```

Again i am doing it this way because i am defining all of these thing in the environment variables with docker-compose. If you are not doing it this way the database url can be just hardcoded in the next parts.

In the `run_migrations_offline` function change this:

```python
url = config.get_main_option("sqlalchemy.url")
```

To this:

```python
url = get_url()
```

And in `run_migrations_online` function add these two lines to the top.

```python
configuration = config.get_section(config.config_ini_section)
configuration["sqlalchemy.url"] = get_url()
```

Now the full `env.py` should look something like this.

```python
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#target_metadata = None

from app import models

target_metadata = models.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    db = os.getenv("POSTGRES_DB", "app")
    return f"postgresql://{user}:{password}@{server}/{db}"


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Important part

At this point if you were creating the tables in your code you should stop doing that and remove these lines because now alembic should be responsible for creating the tables.

```python
models.Base.metadata.create_all(bind=engine, checkfirst=True)
```

Now if you look at guides online they will the you to run `alembic revision --autogenerate -m 'First commit'` but this is what caused some really annoying issues for me recently. First it is important to understand what `alembic` really is and what does it do. I dont know about you but for me "alembic database migrations" feels a bit cryptic. I kinda thought that it would just look at my database and add any changes i have made but in reality it is not quite that magical. It is more like version control for the database schema and it needs python code for every version to be able to make the changes you need from version to version so every step will be coded. The python code will be automatically generated so it is very convinient but it is not magic.

### The issue
So what happened to me was that i was trying to install my code on a fresh virtual machine but my api was erroring because some table didnt exist in the database. It took a while of troubleshooting to undestand what happened. If you were to run `alembic revision --autogenerate -m 'First commit'` and `alembic upgrade head` now it would be successful because database is "up to date" and no changes have been made. Lets say you had `table1` in the database and now you create `table2` and maybe make some changes to `table1` then and run those commands again it will also work because it will generate the code that will create the new table and make the changes to `table1`. So where is the problem you might ask. See it has the code the make changes to `table1` but it has no idea how to actually create `table1` because you never generated the code to create that table. It will be able to do everything when starting from the database schema you had but it does not know how to get to that point because the database was already up to date.

### The fix

So to avoid running into this issue when you are trying deploy the application or when a new developer tries to run it should be as simple as dropping **all** of the tables before running those commands. In my case i had already ran them so i had to delete **everything** from `alembic/versions` and drop all the tables **including** the `alembic_version` table. If you have not run those commands it should be enough to drop all the tables from your database first. Now the revision command should show that it detected everything that you need in the database in the initial revision and it will be able to start from a completely empty database without any issues. Note that i have a `prestart.sh` script that runs `alembic upgrade head` before starting the backend so that any other developers working on other parts of the project can just run `docker-compose build` and `docker-compose up` to have everything done *automagically* for them but you can run the command manually as well. Also i ran this in the backend container while it was running because i didnt want to manually set the environment variables.

```bash
root@d8556de436aa:/app# alembic revision --autogenerate -m 'First commit'
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'authors'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_authors_id' on '['id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_authors_name' on '['name']'
INFO  [alembic.autogenerate.compare] Detected added table 'books'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_description' on '['description']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_id' on '['id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_isbn' on '['isbn']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_language' on '['language']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_price' on '['price']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_publication_date' on '['publication_date']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_books_title' on '['title']'
INFO  [alembic.autogenerate.compare] Detected added table 'genres'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_genres_name' on '['name']'
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_id' on '['id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_is_active' on '['is_active']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_is_admin' on '['is_admin']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_password_hash' on '['password_hash']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_register_date' on '['register_date']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_username' on '['username']'
INFO  [alembic.autogenerate.compare] Detected added table 'book_authors'
INFO  [alembic.autogenerate.compare] Detected added table 'book_genres'
INFO  [alembic.autogenerate.compare] Detected added table 'book_ownership'
INFO  [alembic.autogenerate.compare] Detected added table 'orders'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_orders_id' on '['id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_orders_order_date' on '['order_date']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_orders_total_price' on '['total_price']'
INFO  [alembic.autogenerate.compare] Detected added table 'reviews'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_reviews_comment' on '['comment']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_reviews_edited' on '['edited']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_reviews_id' on '['id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_reviews_rating' on '['rating']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_reviews_review_date' on '['review_date']'
INFO  [alembic.autogenerate.compare] Detected added table 'ordered_books'
  Generating /app/alembic/versions/b7d3c606877e_first_commit.py ...  done
root@d8556de436aa:/app# alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> b7d3c606877e, First commit
```

## Conclusion

Now with this setup everytime you make changes to the database schema running `alembic revision --autogenerate -m 'something something'` will generate the code to add changes to the database schema and `alembic upgrade head` will look at the `alembic_version` table in the database and decide what code to run to apply the correct changes. This means you dont need to create the tables in your code anymore and you do not need to drop any tables when making changes to them.