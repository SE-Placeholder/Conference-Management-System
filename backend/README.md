# Conference Management System Backend API

## Testing

the current version of the API is live and (should be) accessible at the following url:

- `kind-wind-83282.pktriot.net`

![](https://img.shields.io/uptimerobot/status/m787566269-a2f2cdfea89e35226bfc73df?color=%23E30B5D&label=server%20status&logo=raspberry-pi&logoColor=%23E30B5D&style=for-the-badge)

if it's down blame my ISP

### request with httpie
```bash
http GET localhost:8000/conference/ping/ Authorization:"Bearer <access token>"
```

### request with curl
```bash
curl -X GET localhost:8000/conference/ping/ -H "Authorization: Bearer <access token>"
```

## Development

### requirements
- python 3
- pipenv

### install dependencies
```bash
$ pipenv install
```

### activate pipenv environment
```bash
$ pipenv shell
```

### run dev server
```
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver
```
