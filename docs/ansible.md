# Ansible

*[[apps|<- Назад]]*

*[[index|<- На главную]]*
***
## Основы ansible

[Документация.](https://docs.ansible.com/ansible/latest/index.html)

`ansible` - система *управления конфигурациями*, написанная на языке программирования Python, с использованием декларативного языка разметки для описания конфигураций. Применяется для *автоматизации* настройки и развертывания программного обеспечения.

> Главное отличие Ansible от аналогов - *не нужна* установка *агента* или *клиента* на целевые системы.

Большинство сред Ansible состоят из трех *основных компонентов*:

- *Control node* (узел управления) - система, на которой установлен Ansible.
- *Inventory* (инвентаризация) - логически организованный, список управляемых узлов.
- *Managed node* (управляемый узел) - удаленная система или хост, которым управляет Ansible.

![[ansible_work_scheme.svg]]

*Установка* описана на [сайте](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html).

Чтобы просмотреть *информацию* об Ansible, в том числе и о конфигах, можно использовать следующую команду: `ansible --version`

Основная *настройка* Ansible происходит через файл конфигурации `ansible.cfg`. В нем можно указать различные параметры, такие как путь к `inventory`, настройки ssh и многое другое.
Ansible *ищет* файл конфигурации в следующем порядке:

- `ANSIBLE_CONFIG` - переменная окружения (если установлена);
- `ansible.cfg` - в текущей директории;
- `~/.ansible.cfg` - в домашней директории;
- `/etc/ansible/ansible.cfg` - основная директория.

*Пример:*

```ini
[defaults]
inventory=./inventory.yml
```

> Чтобы *сгенерировать* конфиг со стандартными настройками по умолчанию, используем следующую команду:
> ```bash
> ansible-config init --disabled > ansible.cfg
> ```

***
## Inventory

*Inventory* (инвентаризация) - это *файл* содержащий организованный *список хостов* и *групп хостов*, которыми управляет Ansible. По умолчанию Ansible использует файл `/etc/ansible/hosts`, но можно указать любой другой файл с помощью параметра `-i` или указав в файле конфигурации. Используя файл инвентаризации, Ansible может *управлять* большим количеством хостов при помощи одной команды.

> Inventory-файл можно создавать как в *формате INI* так и в *формате YAML*. Для небольшого количества хостов подойдет INI, но по мере увеличения, удобнее будет использовать YAML.

*Пример самого простого inventory-файла:*

```ini
[myhost]
192.0.2.50
192.0.2.51
192.0.2.52
```

*Пример более сложного inventory-файла:*

```ini
[nginx_hosts]
nginx1 ansible_host=10.0.3.10 ansible_password=test1

[apache_hosts]
apache1 ansible_host=10.0.3.11 ansible_password=test2
apache2 ansible_host=10.0.3.12 ansible_password=test3

[containers:children]
nginx_hosts
apache_hosts
```

> Чтобы проверить созданный inventory-файл, можно использовать следующую команду:
> ```bash
> ansible-inventory -i inventory.yml --list
> ```

*Пример inventory-файла в формате YAML:*

```yml
nginx_hosts:
  hosts:
    nginx1:
      ansible_host: 10.0.3.10
      ansible_user: owner

apache_hosts:
  hosts:
    apache1:
      ansible_host: 10.0.3.11
    apache2:
      ansible_host: 10.0.3.12
  vars:    # Групповые переменные
    ansible_user: root

containers:    # Метагруппа
  children:
    nginx_hosts:
    apache_hosts:
  vars:
    ansible_ssh_private_key_file: /root/.ssh/id_rsa
```

> Переменные можно хранить в *отдельных* файлах, *названных* по имени группы, для которой они предназначены.

**Некоторые часто используемые переменные:**

- `ansible_host` - имя хоста.
- `ansible_port` - порт хоста для подключения.
- `ansible_user` - пользователь хоста.
- `ansible_password` - пароль от хоста.
- `ansible_ssh_private_key_file` - путь до файла приватного ssh ключа.
- `ansible_become` - выполнять команды с повышением привилегий.

***
## Простые команды в Ansible. Module

*Module* (модуль) - это *код* или *двоичные файлы*, которые Ansible копирует и *выполняет* на каждом управляемом узле (при необходимости) для выполнения *действий*, определенного в каждой задаче (task).

*Список* модулей можно найти по [ссылке](https://docs.ansible.com/ansible/latest/collections/index.html) или воспользоваться *поиском* на сайте документации.

*Простые команды* Ansible позволяют выполнять *одноразовые* задачи на хостах без необходимости создания плейбуков.

**Некоторые простые команды:**

- Пинг серверов:

```bash
ansible myhosts -i inventory.yml -m ping
```
`где: -i - не стандартный inventory-файл; -m - модуль`

- Вывод информации о серверах:

```bash
ansible all -i inventory.yml -m setup
```

- Запуск команды в shell:

```bash
# Позволяет использовать возможности оболочки (конвейеры, перенаправления и т.д.)
ansible nginx_hosts -m shell -a "uptime"
# Без использование оболочки (только для простых команд)
ansible apache_hosts -m command -a "uptime"
```
`где: -a - аргументы`

- Создать файл:

```bash
ansible all -m file -a "path=/root/test.txt state=touch mode=0777"
```

- Удалить файл:

```bash
ansible all -m file -a "path=/root/test.txt state=absent"
```

- Скопировать файл с хоста:

```bash
ansible all -m copy -a "src=test.txt dest=/root/test.txt"
```

- Перезапустить службу:

```bash
ansible apache_hosts -m service -a "name=apache2 state=restarted"
```

***
## Playbooks

*Playbook* (сценарий) - это описание состояния ресурсов системы, в котором она *должна находится* в конкретный момент времени, включая установленные пакеты, запущенные службы, созданные файлы и многое другое. Ansible проверяет, что каждый из ресурсов системы находится в *ожидаемом состоянии* и пытается *исправить* состояние ресурса, если оно *не соответствует* ожидаемому. Для написания плейбуков используется формат YAML с описанием *требуемых состояний* управляемой системы.

Playbook *состоит* из:

- *Playbook* - непосредственно сам плейбук, *список действий*, определяющий порядок, в котором Ansible выполняет операции сверху вниз.
- *Play* - упорядоченный *список задач*, сопоставленный с управляемыми узлами из inventory-файла.
- *Task* - одна *задача*, выполняемая с помощью модуля.
- *Module* - *модуль кода* или *двоичный файл*, который Ansible запускает на управляемых узлах.

*Пример playbook:*

```yml
- name: Test Nginx
  hosts: nginx_hosts
  vars:
    word: Hello

  tasks:
  
    - name: Ping nginx hosts
	  ping:

    - name: Print message
      debug:
        msg: "{{ word }} Nginx!"

    - name: Print ip info witn ansible_facts
      debug:
        msg: "Ip-address eq {{ ansible_facts['all_ipv4_addresses'][0] }}"



- name: Test Apache
  hosts: apache_hosts
  vars:
    word: Hi

  tasks:
  
    - name: Ping apache hosts
	  ping:

    - name: Print message
      debug:
        msg: "{{ word }} Apache!"

    - name: Print ip info with variables
      debug:
        msg: "Ip-address eq {{ ansible_host }}"
```

*Команда для запуска playbook:*

```bash
ansible-playbook -i inventory.yml playbook.yml
```

*Команда для проверки playbook без внесения изменений на хосты:*

```bash
ansible-playbook -i inventory.yml --check playbook.yml
```

***
## Roles & Ansible Galaxy

Сайт с ролями созданными *пользователями*: [Ansible Galaxy](https://galaxy.ansible.com/ui/).

*Roles* (роли) - это способ организации и *повторного использования* кода в Ansible. Роль содержит набор задач, переменных и файлов, *необходимых* для выполнения определенной задачи. Вместо блока tasks в плейбуке можно указать роль.

Роли Ansible имеют определенную *структуру*, включающую семь основных стандартных каталогов. Любые каталоги, которые роль не использует, можно *опустить*.

*Основные каталоги roles:*

- `tasks` - каталог с задачами;
- `handlers` - каталог с обработчиками (особый тип задач);
- `templates` - каталог с шаблонами;
- `files` - каталог с файлами, которые нужны роли;
- `vars` - каталог с переменными;
- `defaults` - каталог, в котором указываются значения по умолчанию для переменных, эти значения имеют самый низкий приоритет, поэтому их легко перебить, определив переменную в другом месте;
- `meta` - каталог с метаданными роли (включая зависимости.

> Внутри каталогов `tasks`, `handlers`, `vars`, `defaults` и `meta`, ansible считывает все, что находится в файле `main.yml`. Другие файлы надо *добавлять* через `include`.
> Внутри роли, на файлы в каталогах `files`, `templates` и `tasks`, можно ссылаться *не указывая путь* к ним (достаточно указать имя файла).

*Создание структуры каталогов для роли:*
```bash
ansible-galaxy role init nginx_role
```

По умолчанию, Ansible *ищет* роли в следующих местах:

- в коллекциях, если они используются;
- в папке `roles/`, которая расположена относительно файла плейбука;
- в папках по умолчанию: `~/.ansible/roles/`, `/usr/share/ansible/roles/`, `/etc/ansible/roles/`;
- в папке, где находится файл плейбука.

### Использование ролей

**Использование ролей на уровне play**

Роли добавленные в раздел `roles`, выполняются *перед* любыми другими задачами в плейбуке.

```yml
- hosts: all
  roles:
    - test_role_1
    - test_role_2
```

**Динамическое повторное использование ролей**

Роли можно использовать *динамически* повторно в любом месте плейбука, при помощи `include_role`. При таком использовании, роли выполняются в том порядке, в котором они *определенны*.

*Особенности:*

- Роль включается *во время выполнения* playbook. Это позволяет использовать *динамические* переменные или `loop` для передачи параметров в роль.
- Можно использовать `include_role` в задачах, чтобы включать роль *несколько раз* с разными параметрами.

```yml
- hosts: all

  tasks:
    - name: Print a message
      debug:
        msg: "this task runs before the role"

    - name: Include the test role
      include_role:
        name: test_role_1
      loop:
        - web1
        - web2
      vars:
        web_server: "{{ item }}"

    - name: Print a message
      debug:
        msg: "this task runs after the role"
```

**Статическое повторное использование ролей**

Роли можно использовать *статически* повторно в любом месте плейбука, при помощи `import_role`. При таком использовании, *поведение* такое же, как при использовании ключевого слова `roles`, только задачи выполняются не в начале, а в том месте где они *определенны*.

*Особенности:*

- Роль импортируется во время парсинга playbook, то есть *до его выполнения*. Это означает, что все задачи и переменные роли становятся *частью* playbook на этапе компиляции.
- Поскольку `import_role` выполняется на этапе компиляции, *нельзя* использовать динамические переменные или `loop` для передачи параметров в роль.

```yml
- hosts: all

  tasks:
    - name: Print a message
      debug:
        msg: "before we run our role"

    - name: Import the test role
      import_role:
        name: test_role_2

    - name: Print a message
      debug:
        msg: "after we ran our role"
```

***
## Collections

*Collections* (коллекции) - это способ организации и распространения модулей, плагинов, ролей и других компонентов Ansible в удобном формате. Коллекции позволяют группировать связанные элементы, что упрощает их использование и управление ими. Они были введены в Ansible 2.8 и стали стандартом для упаковки и распространения контента Ansible.

*Создание новой коллекции:*

```bash
ansible-galaxy collection init my_namespace.my_collection
```

*Установка коллекции (чтобы можно было использовать ее модули и роли в плэйбуках):*

```bash
ansible-galaxy collection install my_namespace.my_collection
```

***
## Molecule

[Документация](https://ansible.readthedocs.io/projects/molecule/).

*Molecule* - это инструмент, который используется для тестирования ролей Ansible. Он позволяет разработчикам создавать, тестировать и управлять окружениями для выполнения тестов, что помогает обеспечить качество и надежность кода.

*Зависимости:*

- ansible-core >= 2.12
- Python >= 3.10

*Установка:*

```bash
# Ubuntu
apt install python3-pip libssl-dev
pip3 install ansible-dev-tools
```

***