# Роль zabbix_agent_install

## Описание

Данная роль устанавливает на машины zabbix агенты, и прописывает их все в админ панель zabbix сервера. Сначала роль удаляет агент с машины, если он был, удаляет все каталоги связанные с ним. После устанавливает агент и настраивает его. В конце роль прописывает все настроенные агенты в админ панель zabbix сервера.

## Переменные

*Переменные в каталоге defaults данной роли:*

- `zabbix_agent_catalogs` - каталоги которые необходимо удалить после удаления zabbix агента.

*Переменные которые необходимо указать в файлах group_vars:*

- `zabbix_servers` - переменная с автоматической генерацией списка хостов zabbix сервера. Имя группы "zabbix_servers" необходимо заменить на свое.
```
zabbix_servers: "{{ groups['zabbix_servers'] | map('extract', hostvars, 'ansible_host') }}"
```

*Переменные которые необходимо указать в файлах host_vars:*

- `zabbix_psk_identity` - переменная zabbix агента, содержащая PSK идентификатор сервера для записи в конфиг.
```
zabbix_psk_identity: "PSK 001"
```

- `ansible_user` - переменная zabbix сервера, содержащая имя пользователя zabbiz.
```
ansible_user: Admin
```

- `ansible_httpapi_pass` - переменная zabbix сервера, содержащая пароль пользователя zabbix.
```
ansible_httpapi_pass: test
```

- Переменые zabbix сервера необходимые для базового подключения к админ панели для добавления агентов.
```
ansible_network_os: community.zabbix.zabbix
ansible_connection: httpapi
ansible_httpapi_port: 8080
ansible_zabbix_url_path: ""
```

