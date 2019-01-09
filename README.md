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
    - add geo reference ```./cmd.py lib.parser.add_geo_reference```
    - create search index: ```./cmd.py lib.parser.create_index```

## TODO

### Backend

- add geo locations
    - erster druchlauf: 7021 gefundene Geo-Referenzen, 4815 unzugeordnete
- create search index
- add frontend api

## Frontend

- UX/UI

## Daten

- infos: https://lobbypedia.de/wiki/Lobbyregister_EU

- organisation_name
- registration_date
- website_address
- level_of_interest
- number_of_persons_involved
- number_of_ep_accredited_persons
- full_time_equivalent_fte
- overall_budget_turnover_absolute_amount
- overall_budget_turnover_as_a_range
- estimate_of_costs_absolute_amount
- estimate_of_costs_as_a_range
- member_organisations
- fields_of_interest
- eu_initiatives
- section
- subsection
- head_office
    - head_office_address
    - head_office_post_code
    - head_office_country
    - head_office_city