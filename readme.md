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
```
python super.py --build
```
### 4.For more, just explore it
---
>Add
### 5.特性
+ **实现html转dom树，html组件互相引用覆写**
    只需在html首注册`{% register name="任意标志名称" %}`，即可在任何地方使用，例如
    ```html
    c.html
    {% register name="c" %}
    ...

    ```
    ```
    <!-- use it anywhere and any files except for c.html-->
    <c></c>
    ```
+ **实现插槽, 可预留位置插入物件**
    ```html
    component.html
    {% register name="c" %}
    <div>
        {{ label }}
    </div>

    page.html
    <c>
        <div slot="label"></div>
    </c>
    ```
    c中带有slot属性的dom将在编译c组件时替换其中的{{ label }}
+ **支持static静态资源插槽, 一经注册可全局使用**
    需要在settings中配置静态文件名与对应static下路径，之后可以这样用
    ```html
    <!-- res is the name of your import source -->
    <img src="{{ res }}">
    <link href="{{ ... }}">
    ```
+ **支持任意key,value插槽，参数插槽**
    需要调用Super的API接口
    - registRandomSlots
        登记任意key,value，使用时只需写`{{ key }}`，编译后自动替换位`value`
    - registParamsSlots
        登记任意key(参数名),value(参数值)，使用时只需写
        ```
        <script import>
            var key
        </script>
        ```
        它将被替换为
        ```
        ...
            var key = value
        ...
        ```
