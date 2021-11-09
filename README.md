# fastfoodDeliveryAggregator

Автор - Филин Дмитрий Алексеевич
Студент 1 курса ЗКИ-21 ИКИТ СФУ
Начал работу над проектом 02.11.21
github - https://github.com/244sinfall
Программа обладает следующими возможностями:
1. Конструктор продуктов и блюд. Блюда собираются из продуктов, которые добавляются через интерфейс администратора.
У продуктов есть характеристики, масса за единицу и цена. Характеристики используются для математического рассчета
Ценности блюд, в то время как цена продуктов используется для расчета себестоимости блюда. Блюдо собирается из
созданных продуктов, имеют свою пищевую ценность, цену, название, установленное администратором. Записи о продуктах
и блюдах хранятся в JSON файлах.

2. У администратора есть возможность создать on-line отчет за выбранное количество дней. Отчет отражает расход
продуктов, реализованные блюда, себестоимость утраченных продуктов, а также прибыль с заказов и их количество (WIP)

3. Администратор может полностью удалять записи заказах. Записи, как и продукты с блюдами хранятся в JSON файле.

4. Менеджер может полностью изменять заказы, время приготовления, статус оплаты, статус заказа. Он может помечать
заказ как принятый, завершенный и так далее. Менеджер может смотреть завершенные заказы в отдельной вкладке, но не
может с ними взаимодействовать, только с теми, которые сейчас действительны.

5. Клиент может заказывать блюда из интерактивного списка. Клиент может несколько раз нажать на одно и тоже блюдо,
чтобы заказать несколько порций. Цена чека считается автоматически. Сервис позволяет оформить еду с доставкой в г.
Красноярск, Дивногорск, Сосновоборск или же самовывозом на розничной точке (Киренского 26Б :D). Клиент может оплатить
еду наличными при получении или картой сразу в приложении. Программа сохраняет заказы, которые создал конкретный
клиент. При новых заказах автоматически добавляется номер телефона и адрес, Который был указан к предыдущему заказу.

6. Заказы хранят расширенную информацию вроде времени заказа и времени к доставке, которое пользователь может указать
при заказе. Кроме того, JSON отражает оплачен ли заказ, оформлена доставка или самовывоз, также отражает конкретное
время заказа и прочую необходимую информацию.


[![Total alerts](https://img.shields.io/lgtm/alerts/g/244sinfall/fastfoodDeliveryAggregator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/244sinfall/fastfoodDeliveryAggregator/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/244sinfall/fastfoodDeliveryAggregator.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/244sinfall/fastfoodDeliveryAggregator/context:python)

