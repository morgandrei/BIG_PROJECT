Это проект сайта рассылок электронных писем
<<<<<<< HEAD
Для работы проекта необходимо выполнить следующие шаги:

Клонировать проект или сделать форк
Запустите виртуальное окружение "env".
Установите зависимости из файла requrements.txt
Создать в корне проекта файл .env и внесите в него все переменные окружения по образцу из файла .env.sample
Создайте миграции \\ python manage.py makemigrations
Примените миграции \\ python manage.py migrate
Для Windows запустите wsl \\ wsl
            запустите редис \\ sudo service redis-server start
Запустите проект \\ python manage.py runserver
Создайте Суперпользователя \\ python manage.py csu

Другие доступные команды:

python manage.py cgm \\ Создание группы "менеджер"
python manage.py run_apscheduler \\  Запуск работы сервиса по расписанию
python manage.py run_newsletter \\  Запуска сервиса вручную

Логика работы проекта:

Создайте новую рассылку, если текущее время больше или равно времени начала, выбираются все клиенты, которые указаны в 
настройках рассылки, и запускается отправка для всех этих клиентов.

Если время начала рассылки еще не наступило, то отправка стартует автоматически при наступлении указанного времени без 
дополнительных действий пользователя.
При отправке сообщений собирается статистика по каждой рассылке для формирования отчетов.

Права доступа:
Для неавторизованного пользователя открыт доступ только к главной странице, странице авторизации и закрыт весь 
функционал системы.

Авторизованный пользователь имеет доступ только к своим клиентам, сообщениям, рассылкам и отчету о своих рассылках.
Персонал может просматривать списки всех клиентов, сообщений, рассылок, пользователей сервиса и имеет доступ к отчету о 
всех проведенных рассылках.

Чтобы добавить пользователя в группу менеджеров, в административной панели установите ему статус персонала
и в разделе групп, выберите группу "manager".
=======
>>>>>>> parent of 7dc56b2 (Update ReadMe.md)
