FROM zerogjoe/mssql-python3.6-pyodbc

WORKDIR /usr/lib/app

COPY . .

ENV DATABASE=${DATABASE}
ENV SERVER=${SERVER}
ENV UID=${UID}
ENV PWD=${PWD}
ENV IEX_TOKEN=${IEX_TOKEN}
ENV account_sid=${account_sid}
ENV auth_token=${auth_token}
ENV phone=${phone}
ENV IV_URL=${IV_URL}
ENV IV_PORT=${IV_PORT}
ENV RH_USER=${RH_USER}
ENV RH_PWD=${RH_PWD}
ENV API_URL=${API_URL}


RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["Driver.py"]