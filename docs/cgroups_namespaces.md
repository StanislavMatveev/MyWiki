# Контрольные группы и пространство имен

*[[linux|<- Назад]]*

*[[index|<- На главную]]*
***
## Контрольные группы

*Контрольная группа (control group, cgroups, cgroup)* - набор процессов (группа), объединенных по некоторым признакам, для которого механизмами ядра наложена *изоляция* и установлены *ограничения* на некоторые вычислительные ресурсы (процессорные, сетевые, ресурсы памяти, ресурсы I/O).
Данный механизм существенным образом *используется* в технологии инициализации `systemd`, а так же является *ключевым* элементом в реализации системы виртуализации на уровне операционной системы [[lxc#LXC|LXC]].

Одна из *целей* механизма - предоставить единый *программный интерфейс* к целому спектру средств управления процессами. Механизм предоставляет следующие *возможности*:

- *ограничение ресурсов (resourse limiting):* использование памяти, в том числе виртуальной;
- *приоритезацию:* разным группам можно выделить разное количество процессорного ресурса и пропускной способности подсистемы I/O;
- *учет:* подсчет затрат тех, либо иных ресурсов группой;
- *изоляцию:* разделения [[cgroups_namespaces|пространств имен]] для групп таким образом, что одной группе недоступны процессы, сетевые соединения и файлы другой;
- *управление:* приостановку (freezing) групп, создание контрольных точек (checkpointing) и их перезагрузку.

*Управление* контрольными группами возможно различными способами:

- через *доступ* к виртуальной файловой системе `cgroup` напрямую;
- *утилитами* `cgcreate`, `cgexec`, `cgclassify` из libcgroup;
- используя *демон* механизма правил (rules engine daemon), который автоматически перемещает процессы определенных пользователей, групп или команд в cgroups согласно конфигурации;
- *косвенно* через другие программные средства, использующие контрольные группы, например через системы контейнеризации [[lxc#LXC|LXC]] и `Docker`, библиотеку `libvirt`, технологию инициализации `systemd`, кластерное управляющее программное обеспечение Grid Engine.

***
## Пространство имен

*Пространство имен (namespaces)* - функция ядра Linux, позволяющая *изолировать* и *виртуализировать* глобальные системные ресурсы множества процессов. Одной из основных целей поддержки пространств имен является *реализация* контейнеров.

Пространство имен дает процессам, запущенным в контейнерах, *иллюзию*, что они имеют свои собственные ресурсы. Основная цель изоляции процессов состоит в *предотвращении вмешательства* процессов одного контейнера в работу других контейнеров, а также работу хостовой машины. На данный момент существует несколько технологий контейнеризации, *основными* же являются [[lxc#LXC|LXC]] и `Docker`. И в основе этих технологий лежат пространства имен и они имеют *одинаковый* принцип работы.

> Идеи, лежащие в основе *механизма* пространств имен, исходят из ранних операционных систем. В *Unix* в 1979 году был добавлен системный вызов `chroot` с целью обеспечить *изоляцию* части файловой системы и предоставить "площадку для тестирования", *отделенную* от основной системы.

Linux-система при старте инициализирует *один экземпляр* каждого типа пространства имен, *кроме* пространства имен *файловой системы*. После инициализации можно *создать* или *объединить* дополнительные пространства имен.

Все пространства имен поддерживают *вложенность*, то есть между ними можно установить связь "*родитель-потомок*". Таким образом некоторые пространства *наследуют* все свойства от своего родительского пространства имен. Однако это верно не для всех пространств.

*Функциональные возможности* пространства имен одинаковы для всех типов: каждый процесс *связан* с пространством имен и может видеть или использовать только ресурсы, связанные с этим пространством имен, и, где это применимо, с его потомками. Таким образом, каждый процесс (или его группа) может иметь *уникальное* представление о ресурсе. Изолированный ресурс зависит от типа пространства имен, созданного для данной группы процессов.

### Виды пространства имен

- **Пространство имен файловой системы (Mount)** - это независимое дерево файловой системы, ассоциированное с определенной группой процессов.

- **Пространство имен UTS (Unix Time Sharing)** - используется для изоляции двух конкретных элементов системы, относящихся к системному вызову `uname`.

> `uname` - консольная утилита, выводящая *информацию* о системе.

- **Пространство имен ID процессов (PID)** - изолирует пространство ID процессов, это означает, что процессы в различных пространствах могут иметь одинаковые ID.

> Однако в пространстве имен хоста все процессы имеют *уникальные* идентификаторы, таким образом необходимо *разделять* идентификатор *внутри* определенного пространства и *снаружи* этого пространства, то есть в хостовой машине.

- **Пространство имен сетей (Network)** - предоставляет изоляцию систем ресурсов, связанных с сетями (сетевое оборудование, стеки протоколов IPv4 и IPv6, таблицы IP-маршрутизации, файрволы, номера портов и др.).

> *Физические* сетевые устройства могут принадлежать только одному пространству. При этом каждое пространство имен может иметь одно или несколько *виртуальных* устройств, и таким образом для обеспечения доступа во внешнюю сеть между физическим и виртуальным устройством из разных пространств создается *мост*. То есть по сути туннель между разными пространствами имен сети.

- **Пространство имен межпроцессорного взаимодействия (IPC)** - включает в себя семафоры, разделяемую память и очереди сообщений.

- **Пространство имен пользователей (ID)** - изолирует ID пользователей и групп, корневой каталог, ключи и capabilities.

***