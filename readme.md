# ~ super
## quickstart
### 1.Create html
+ create index.html at 'views/'
```html
{% register name="index" %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1> Hello, this is Super </h1>
</body>
</html>
```
+ create intro.html at 'views/'
```html
{% register name="intro" %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1> this is intro page </h1>
    <card></card>
    <card></card>
    <card></card>
</body>
</html>
```
+ create card.html at 'views/'
```html
{% register name="card" %}

<div>
    here is card
</div>
```
{% register name="intro" %} is necessary, which names this page. Once you register, you can use it anywhere, like this`<card></card>`

### 2.Add router
add router in 'settings'
```python
ROUTER = [
    Url('index', [
        Url('intro')
    ])
]
```

Url(param1, param1)

    param1 is page name,
    param2 is pages that belong to param1
### 3.Run
just run
```d
python super.py build
```
### 4.For more, just explore it
..........