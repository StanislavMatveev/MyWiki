# Тестирование работы Loki + Promtail

*[[tests|<- Назад]]*

*[[index|<- На главную]]*
***
## Данные

**Исходные данные:**

- Две виртуальных машины под управлением Ubuntu 22.04.
- Характеристики 1 узла: 1GB оперативной памяти, 2 ядра процессора.
- На 1 узле установлен Loki.
- Характеристики 2 узла: 1GB оперативной памяти, 1 ядро процессора.
- На 2 узле установлен Promtail.

**Цели:**

- Выявить зависимость нагрузки на систему от количества обрабатываемых логов.

## Нагрузка служб путем увеличения количества записываемых логов

**Использовалось:**

- 100 записей в секунду (длина строки 200 символов)
- Команда: `bash -c 'while true; do head -n 100 /dev/urandom | tr -dc "a-zA-Z0-9" | head -c 200 >> /var/log/messages; echo >> /var/log/messages; sleep 0.01; done'`
- Временной интервал: 1 минута
- 2 теста

**Результаты:**

- Узел Promtail: никаких заметных изменений по процессу не замечено, лишь немного выросла резидентная память процесса с 67M до 77M в первом тесте и с 36M до 48M во втором.
- Узел Loki: никаких заметных изменений по процессу не замечено, лишь так же немного выросла резидентная память процесса с 107M до 123M в первом тесте и с 59M до 85M во втором.

**Использовалось:**

- 1000 записей в секунду (длина строки 200 символов)
- Команда: `bash -c 'while true; do head -n 100 /dev/urandom | tr -dc "a-zA-Z0-9" | head -c 200 >> /var/log/messages; echo >> /var/log/messages; sleep 0.001; done'`
- Временной интервал: 1 минута
- 2 теста

**Результаты:**

- Узел Promtail: никаких заметных изменений по процессу не замечено, лишь немного выросла резидентная память процесса с 71M до 81M в первом тесте и с 48M до 66M во втором.
- Узел Loki: никаких заметных изменений по процессу не замечено, лишь так же немного выросла резидентная память процесса с 119M до 129M в первом тесте и с 86M до 101M во втором.

**Использовалось:**

- 10000 записей в секунду (длина строки 200 символов)
- Команда: `bash -c 'while true; do head -n 100 /dev/urandom | tr -dc "a-zA-Z0-9" | head -c 200 >> /var/log/messages; echo >> /var/log/messages; sleep 0.0001; done'`
- Временной интервал: 1 минута
- 2 теста

**Результаты:**

- Узел Promtail: никаких заметных изменений по процессу не замечено, причем в этот раз даже резидентная память выросла всего на 1M-2M в обоих тестах.
- Узел Loki: никаких заметных изменений по процессу не замечено, лишь так же немного выросла резидентная память процесса с 132M до 145M в первом тесте и с 101M до 109M во втором.

**Использовалось:**

- 100 записей в секунду (длина строки 10000 символов)
- Команда: `bash -c 'while true; do cat output.txt >> /var/log/messages; sleep 0.01; done'`
- Временной интервал: 1 минута

**Результаты:**

- Файл логов вырос с 15M до 456M.
- Узел Promtail: никаких заметных изменений по процессу не замечено, единственный интересный момент заключался в том, что сначала резидентная память начала расти, а потом наоборот уменьшаться, в целом оставаясь в районе одного значения.
- Узел Loki: наблюдались скачки процентной нагрузки на ЦПУ вплоть до 20%, но в целом процессорное время использовалось мало. Резидентная память менялась скачками, то увеличиваясь, то падая в интервале от 120M до 150M.

**Выводы:**

- Никаких значительных изменений на систему в данных тестах выявлено не было.
- Между первыми и вторыми тестами резидентная память оставалась приблизительно в районе одного значения, а вот виртуальная память выросла с 1,7G до 1,8G на узле promtail и с 1,3G до 1,4G на узле loki.
- Если оценить изменения использованной оперативной памяти в тестах, можно заметить, что значение "стало" предыдущего теста, близко к значению "было" следующего теста. Так же, если учитывать предыдущий пункт про виртуальную память, можно сделать вывод, что резидентная память изменяется в определенных значениях пока идет обработка логов, а виртуальная память растет по времени и вероятнее всего связанна с размером файла логов.

***