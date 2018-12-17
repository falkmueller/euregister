# Project: Lobby Register

Web application to analyse the [EU transarency register](https://data.europa.eu/euodp/en/data/dataset/transparency-register)

## requirements

```pip install Whoosh```

## Commands

- start service: ```./service.sh start```
    - optional with port: ```./service.sh start 8001```
    - optional with output in terminal: ```./service.sh 8001 output```
- end service: ```./service.sh stop```
    - optional with port: ```./service.sh stop 8001```
- create index 
    - import csv: ```./cmd.py lib.parser.import_csv```
        - optional with csv file path: ```./cmd.py lib.parser.import_csv data/source/full_export_new.csv```
    - create search index: ```./cmd.py lib.parser.create_index```

## TODO

### Backend

- add geo locations
- create search index
- add frontend api

## Frontend

- UX/UI