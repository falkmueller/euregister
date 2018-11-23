# Project: Lobby Register

Web application to analyse the [EU transarency register](https://data.europa.eu/euodp/en/data/dataset/transparency-register)

## requirements

```pip install Whoosh```

## start service


```
	./service.sh start
```

optional with port


```
	./service.sh start 8001
```

optional with output in terminal


```
	./service.sh 8001 output
```

## end service


```
	./service.sh end
```

optional with port

```
	./service.sh end 8001
```

## TODO

### Backend

- upload xslx
- import to json store
- add geo locations
- create search index

## Frontend

- UX/UI