# API DOCUMENT

## MENU
- [Auth](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/blob/main/documents/api_doc.md#auth)
- [Admin](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/blob/main/documents/api_doc.md#admin)
## Auth
<hr>







### __register__

url

```
http://127.0.0.1:8000/users/register
```

body

```
{
    "username": <username>,
    "password": <passowrd>
}
```
response

success
```
{
    "Register success"
}
```
failed
```
{
    "data": {
        "detail": "Username is taken"
    }
}
```







### __login__

url

```
http://127.0.0.1:8000/users/login
```

body

```
{
    "username": <username>,
    "password": <passowrd>
}
```
response

success
```
{
    "token" : <generated token>
}
```
failed
```
{
    "data": {
        "detail": "Invalid username and/or password"
    }
}
```









### __check__ __permission__

url
```
http://127.0.0.1:8000/users/getpermission
```

body
```
{
    "username": <username>,
    "password": <passowrd>
}
```
response

success
```
{
    "username" : <username>
}
```
failed
```
{
    "data": {
        "detail": "Permission denined"
    }
}
```

## Admin

### __Plant__ __info__

url
```
http://127.0.0.1:8000/admin/plant_info/{id}
```

respon
success
```
{
    ...
}
```

can't find plant
```
{
    "data": {
        "detail": "Plant ID not found"
    }
}
```

permission denied
```
{
    "data": {
        "detail": "Permission denied"
    }
}
```

### __set__ Auto mode

url
```
http://127.0.0.1:8000/admin/auto_mode}
```

body
```
{
    "ID": <int>
}
```
