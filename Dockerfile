FROM python:slim

WORKDIR /app

# Stuff for pyodbc to install correctly in image and run correctly in container
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
  && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update \
  && ACCEPT_EULA=Y apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql17 mssql-tools

COPY requirements.txt requirements.txt

RUN pip3 install --only-binary :all: greenlet
RUN pip3 install --only-binary :all: MarkupSafe
RUN pip3 install --only-binary :all: Flask-SQLAlchemy
RUN pip3 install --only-binary :all: -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]