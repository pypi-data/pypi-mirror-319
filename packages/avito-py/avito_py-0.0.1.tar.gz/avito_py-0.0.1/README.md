# Шаблон проекта pypi

## Как применить шаблон к себе:
- в pyproject.toml поменяйте данные на свой

```
[tool.poetry]
name = "basic_pypi"
version = "0.0.2"
description = ""
authors = ["Nikolay Baryshnikov <root@k0d.ru>"]
packages=[
    { include = "package" },
]
license="MIT"
readme="README.md"
homepage="https://github.com/p141592"
repository="https://github.com/p141592/basic_pypi"
keywords=["poetry", "pypi"]
```

- Установите классифайды которые подходят для вашего проекта https://pypi.org/classifiers/

- Поменяйте автора лицензии

```
Copyright (c) 2020 Baryshnikov Nikolay
```

## Запушить проект в pypi

- Зарегистрируйтесь там https://pypi.org/account/register/
- Если poetry еще не установлен, установите `pip install poetry`
- Выполните `make push` в корне проекта. В консоли попросят ввести логин/пароль от учетки в pypi
- Наслаждайтесь проектом в pypi `pip install <имя проекта, которое [tool.poetry].name>`
