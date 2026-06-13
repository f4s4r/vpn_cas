# mini-vpn

Учебный VPN на Python: шифрованный туннель между двумя машинами через UDP,
веб-интерфейс на Flask и база пользователей с ролями и правами.


## Требования

Docker Desktop (должен быть запущен)

Питон-пакеты ставить не нужно — их ставит Dockerfile.
VPN работает только в Linux-контейнерах, поэтому всё запускается через Docker.

## Важно

Все команды запускать из корня проекта

## Сборка

    docker network create vpnnet
    docker build -t minivpn .

## Запуск веб-интерфейса

    docker run -it --rm -p 8080:5000 -v ${PWD}:/app minivpn python3 -m web.app

Открыть в браузере: http://localhost:8080
Там регистрация и логин. Остановить — Ctrl+C.

## Запуск VPN

Нужно три терминала, все из корня проекта.

Терминал 1 — сервер:

    docker run -it --rm --name vpnserver --network vpnnet --cap-add=NET_ADMIN --device /dev/net/tun -v ${PWD}:/app minivpn python3 server.py

Терминал 2 — клиент:

    docker run -it --rm --name vpnclient --network vpnnet --cap-add=NET_ADMIN --device /dev/net/tun -v ${PWD}:/app minivpn python3 client.py

В клиенте ввести: register (или login), username, password.
Дождаться надписи "tunnel is up" в обоих терминалах.

Терминал 3 — проверка, что туннель работает:

    docker exec -it vpnclient ping 10.0.0.1


Аккаунты у веба и VPN общие: кого зарегистрировал в браузере, тем же
логином заходишь в клиент.

## Возникавшие проблемы

- "address already in use" на 5000 — порт занят (на macOS был занят AirPlay).
  Веб уже запускается на 8080, открывать http://localhost:8080
- "TemplateNotFound" — html-файлы должны лежать в web/templates/,
  а style.css в web/static/, не россыпью в web/.
- Несколько раз менялась схема бд, нужно в таком случае удалять старую: rm users.sqlite 
