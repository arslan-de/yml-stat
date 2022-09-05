# YML file statistics

In order to get summary statistics from yml-file data run the following script:
```
python3 yml-stat.py url
```
Where: 
- url to yml-file (default value: "https://nnetwork.ru/yandex-market.xml")

### YML format documentation 
https://yandex.com/support/direct/feeds/requirements.html

### File examples
https://nnetwork.ru/yandex-market.xml

https://saratov.tbmmarket.ru/tbmmarket/service/yandex-market.xml

### Result example:
```
| category                                                                                            |   offers |
|-----------------------------------------------------------------------------------------------------|----------|
| IP ТЕЛЕФОНЫ CISCO                                                                                   |        0 |
| IP ТЕЛЕФОНЫ CISCO / АКСЕССУАРЫ                                                                      |        2 |
| IP ТЕЛЕФОНЫ CISCO / СНЯТО С ПРОИЗВОДСТВА                                                            |        0 |
| IP ТЕЛЕФОНЫ CISCO / СНЯТО С ПРОИЗВОДСТВА / TЕЛЕФОНЫ СЕРИИ 7900                                      |        0 |
| IP ТЕЛЕФОНЫ CISCO / СНЯТО С ПРОИЗВОДСТВА / TЕЛЕФОНЫ СЕРИИ 8900                                      |        0 |
| IP ТЕЛЕФОНЫ CISCO / СНЯТО С ПРОИЗВОДСТВА / TЕЛЕФОНЫ СЕРИИ 9900                                      |        0 |
| IP ТЕЛЕФОНЫ CISCO / СНЯТО С ПРОИЗВОДСТВА / ТЕЛЕФОНЫ CISCO SMALL BUSINESS                            |        1 |
| IP ТЕЛЕФОНЫ CISCO / СНЯТО С ПРОИЗВОДСТВА / ТЕЛЕФОНЫ СЕРИИ 6900                                      |        0 |
| IP ТЕЛЕФОНЫ CISCO / ТЕЛЕФОНЫ СЕРИИ 3900                                                             |        2 |
| IP ТЕЛЕФОНЫ CISCO / ТЕЛЕФОНЫ СЕРИИ 7800                                                             |        4 |
| IP ТЕЛЕФОНЫ CISCO / ТЕЛЕФОНЫ СЕРИИ 8800                                                             |        7 |
```
