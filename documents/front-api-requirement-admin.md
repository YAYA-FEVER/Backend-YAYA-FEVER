# front-api-requirement-admin.md

## get plant info (GET) token required => permission admin
url
```
url/<linkname>/id=?
```
success
```
{
  "id":<id>,
  "plantName": <plantName>,
  "moisture": <moisture>,
  "humidity": <humidity>,
  "height": <height>,
  "temp": <temp>,
  "autoState": <true of false>
}
```

failed
```
{
  "detail": "Not found:
}
```
## config automatic/manual (POST) token required => permission admin
front payload
```
{
  "headers" {
    ...,
    "Authorization": <token>
  }
  "body": {
    "id":<id>,
  }
}
```
success
```
null
```
failed
```
{
  "detail" : "permission denined"
}
```

## send configuration humidity (POST) token required => permission admin
front payload
```
{
  "headers" {
    ...,
    "Authorization": <token>
  }
  "body": {
    "humidity": <humidity>
  }
}
```
success
```
null
```
failed
```
{
  "detail" : "permission denined"
}
```

## Add/edit plant (POST) token required => permission admin
front payload
```
{
  "headers" {
    ...,
    "Authorization": <token>
  }
  "body": {
    "id":<id>,
    "plantName": <plantName>,
    "plantDetail" : <plantDetail>,
    "price": <price>,
  }
}
```
success
```
null
```
failed
```
{
  "detail" : "permission denined"
}
```

## delete plant (POST) token required => permission admin
front payload
```
{
  "headers" {
    ...,
    "Authorization": <token>
  }
  "body": {
    "id":<id>,
  }
}
```
success
```
null
```
failed
```
{
  "detail" : "permission denined"
}
```
