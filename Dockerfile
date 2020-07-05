FROM zerogjoe/mssql-python3.6-pyodbc

WORKDIR /usr/lib/app

COPY . .


RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["Driver.py"]