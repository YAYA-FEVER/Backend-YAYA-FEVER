# API DOCUMENT

## MENU
- [Auth](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/blob/main/documents/api_doc.md#auth)
- [Admin](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/blob/main/documents/api_doc.md#admin)
- [Customer](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/blob/main/documents/api_doc.md#customer)
- [Hardware](https://github.com/YAYA-FEVER/Backend-YAYA-FEVER/blob/main/documents/api_doc.md#hardware)
<hr>

## Auth

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
payload
```
{
  "headers" {
    ...,
    "Authorization": <token>
  }
}
```

response

success
```
{
    "plant_name": <str>,
    "humidity_soil": <int>,
    "humidity_air_hard": <float>,
    "height_hard": <int>,
    "temp": <float>,
    "activity_auto": <int>
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

### __Auto__ __mode__

url
```
http://127.0.0.1:8000/admin/auto_mode
```

payload
```
{
  "headers" {
    ...,
    "Authorization": <token>
  },
  "body": {
    "ID": <int>,
    "activate_auto": <int>
  }
}
```

response

success
```
{
    "success"
}
```

permission denied
```
{
    "data": {
        "datail": "Permission denined"
    }
}
```

### __Update__ __plant__ && __Created New Plant__

url
```
http://127.0.0.1:8000/admin/new_plant
```

payload
```
{
    "header": {
        ...,
        "Authorization": <token>
    },
    "body": {
        "plant_name": optional<str>,
        "detail": optional<str>,
        "price": optional<int>,
        "ID": <int>
}
```

response

If doesn't have ID in database add new plant
success
```
{
    "Added success"
}
```

If already have ID in database update plant
```
{
    "Update success"
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

### __Set__ __humidity__

url
```
http://127.0.0.1:8000/admin/humidity_front_want
```

payload
```
{
    "header": {
        ...,
        "Authorization": <token>
    },
    "body": {
        "ID": <int>
        "humidity_soil_front": <int>
}
```

response

success
```
{
    "updated success"
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

### __Delete__ __plant__

url
```
http://127.0.0.1:8000/admin/delete_plant
```

payload
```
{
    "header": {
        ...,
        "Authorization": <token>
    },
    "body": {
        "ID": <int>
}
```

reponse

success
```
{
    "delete success"
}
```

permission denied
```
{
    "data": {
        "detail": "Permission denined"
    }
}
```

## Customer

### __Show__ __plant__

url
```
http://127.0.0.1:8000/customer/shelf/plant
```

respond
```
[
    {
        "ID": <int>,
        "booking": <int 1: reserve, 2: not reserve>
    },
    ...
]
```

###  __plant__ __detail__

url
```
http://127.0.0.1:8000/customer/plant_detail/{id}
```

payload
```
{
    "ID": <int>
}
```

respond

found plant
```
{
    "plant_name": <str>,
    "detail": <str>,
    "price": <int>,
    "ID": <int>
}
```

plant not found
```
{
    "data": {
        "detail": "Plant ID not found"
    }
}
```

### __reserve__
```
http://127.0.0.1:8000/customer/reserve
```

Request body
```
{
    "ID": <int>
    "username": <str>
}
```

Responses

success
```
{
    "update success"
}
```

already reserve
```
{
    "already reserve"
}
```

### __Basket__ __list__

url
```
http://127.0.0.1:8000/customer/basket_list
```

Responses

Have plant in basket
```
[
    {
        "ID": <int>,
        "duedate": <datetime>,
        "plant_name": <str>
    },
    ...
    
]
```

## Hardware

### __Update__ __soil__

url
```
http://127.0.0.1:8000/hardware/update/soil
```

Request body
```
{
    "ID": <int>,
    "humidity_soil_hard": <int>
}
```

Responses

plant ID found 
```
{
    "update success"   
}
```

plant ID not found
```
{
    "data": {
        "detail": "Plant ID not found"
    }
}
```

### __Update__ __air__

url
```
http://127.0.0.1:8000/hardware/update/soil
```

Request body
```
{
    "ID": <int>
    "humidity_air_hard": <float>
    "temp": <float>
}
```

Responses

plant ID found 
```
{
    "update success"   
}
```

plant ID not found
```
{
    "data": {
        "detail": "Plant ID not found"
    }
}
```

### __Update__ __height__

url
```
http://127.0.0.1:8000/hardware/update_height
```

Request body
```
{
    "ID": <int>,
    "height_hard": <int>
}
```

Responses

plant ID found 
```
{
    "update success"   
}
```

plant ID not found
```
{
    "data": {
        "detail": "Plant ID not found"
    }
}
```

### __Auto__ __mode__

url
```
http://127.0.0.1:8000/hardware/auto_mode/{ID}
```

Request body
```
{
    "ID": <int>
}
```

Responses

plant ID found
```
{
    "humidity_soil_front": <int>,
    "activate_auto": <int 1: on, 0: off>
    "water_time" : <int>
}
```

plant ID not found
```
{
    "data": {
        "detail": "Plant ID not found"
    }
}
```

### __Check__ __exist__ __plant__

url
```
http://127.0.0.1:8000/hardware/exist_plant/{ID}
```

Request body
```
{
    "ID": <int>
}
```

Responses

plant ID found
```
{
    "existed": 1
}
```

plant ID not found
```
{
    "existed": 0
}
```











