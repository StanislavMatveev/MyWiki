# Роль apache_upstream_restart

## Описание

Данная роль безопасно перезагружает службу apache на серверах, которые используются nginx'ом для балансировки нагрузки. Перед перезагрузкой сервер выводится из потока балансировки nginx, после чего происходит перезагрузка службы apache.
Роль необходимо запускать для хоста nginx.

## Переменные

*Переменные которые необходимо указать в файлах group_vars:*

- `apache_hosts_list` - переменная с автоматической генерацией списка адресов хостов apache (необходимо заменить имя группы "apache_hosts" на свое).
```
apache_hosts_list: "{{ groups['apache_hosts'] | map('extract', hostvars, 'ansible_host') }}"
```

