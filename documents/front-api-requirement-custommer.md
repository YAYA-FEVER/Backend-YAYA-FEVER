# FRONT-API-REQUIREMENTS-CUSTOMMER

## shelf plant list (GET) no token required
(ลิสของต้นไม้ที่ปลูกอยู่)

success
```
{
  plantList: [<plantList>]
}
```
plantList stucture
```
{
  id: <id>,
  status: <true or false>
}
```

## plant detail (GET) no token required
success
```
{
  ใส่อะไรก็ใส่มา เอาให้กุสามารถโชว์ได้ว่าต้นไม้ต้นนี้ต้นอ่ะไร
}
```
failed
```
{
  "data":{
      "detail": "plant not exists"
    }
{
```

## reserve (GET) token required
success
```
null
```

failed
```
{
  "detail": "Not authorized"
{
```

## basket list (GET) token required
(ลิสที่userได้ทำการจองไว้)

success
```
{
  "basketList": [<basketList>]
}
```
failed
```
{
  "detail": "Not authorized"
{
```


