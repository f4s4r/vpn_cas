# mini-vpn

Учебный VPN-туннель: два TUN-интерфейса соединены через UDP, пакеты обфусцируются XOR.

## Команды

Один раз:

    docker network create vpnnet
    docker build -t minivpn .

Терминал 1 (сервер):

    docker run -it --rm --name vpnserver --network vpnnet --cap-add=NET_ADMIN --device /dev/net/tun -v ${PWD}:/app minivpn python3 server.py

Терминал 2 (клиент):

    docker run -it --rm --name vpnclient --network vpnnet --cap-add=NET_ADMIN --device /dev/net/tun -v ${PWD}:/app minivpn python3 client.py

В клиенте выбрать `register`, ввести логин и пароль. Дождаться `tunnel is up`.

Терминал 3 (проверка):

    docker exec -it vpnclient ping 10.0.0.1
