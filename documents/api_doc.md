# API DOCUMENT

## MENU
- [Auth](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/edit/main/documents/api_doc.md#auth)
## Auth
<hr>







### __register__

url

```
http://127.0.0.1:8000/register
```

body

```
{
    "username": <username>,
    "password": <passowrd>
}
```
response
sucess
```
null
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
http://127.0.0.1:8000/login
```

body

```
{
    "username": <username>,
    "password": <passowrd>
}
```
response
sucess
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
http://127.0.0.1:8000/getpermission
```

body
```
{
    "username": <username>,
    "password": <passowrd>
}
```
response
sucess
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


