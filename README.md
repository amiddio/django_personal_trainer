# Personal Trainer

## Описание проекта

Сайт "Персональный тренер" позволяет пользователям выбрать тренера и бронировать событие/тренировку.

Реализован следующий функционал:
* авторизация, регистрация и личный кабинет пользователей
* расширена модель Юзер (из коробки) несколькими дополнительными полями
* создана модель Тренер
* тренерам можно привязать различные события/тренировки, которые имеют даты начала и конца тренировки, стоимость и количество мест
* событиям добавлена функция тэгирования, благодаря которой их можно фильтровать
* авторизованный пользователь может забронировать для себя событие/тренировку
* авторизованный пользователь может оставлять комментарии тренерам
* реализована функция лайков-дизлайков, которые, авторизованный пользователь может ставить тренерам и/или комментариям
* страница обратной связи
* управлением контентом происходит через админ панель

## На чем построен

Django, bootstrap, unittests

## Демонстрация работы в скриншотах

### Авторизация

![Screenshot_1](/screenshots/account_login.png)

### Регистрация

![Screenshot_1](/screenshots/account_register.png)

### Редактирование профиля

![Screenshot_1](/screenshots/account_edit.png)
![Screenshot_1](/screenshots/account_change_password.png)

### Домашняя страница

![Screenshot_1](/screenshots/home.png)

### Список тренеров

![Screenshot_1](/screenshots/all_trainers.png)

### Страница тренера

![Screenshot_1](/screenshots/trainer_detail.png)
![Screenshot_1](/screenshots/trainer_detail_bottom.png)

### Список действующих событий/тренировок

![Screenshot_1](/screenshots/all_events.png)

### Детальная информация о событии

![Screenshot_1](/screenshots/event_detail.png)
![Screenshot_1](/screenshots/event_detail_booked.png)

### Страница для обратной связи

![Screenshot_1](/screenshots/contact.png)

### Некоторые страницы админ панели

![Screenshot_1](/screenshots/admin_trainers.png)
![Screenshot_1](/screenshots/admin_trainer_edit.png)
![Screenshot_1](/screenshots/admin_events.png)
![Screenshot_1](/screenshots/admin_event_edit.png)
![Screenshot_1](/screenshots/admin_comment_edit.png)
