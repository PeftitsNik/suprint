# suprint 

**Suprint** – программа для печати (или сохранения в pdf) произвольных фрагментов изображения с любыми размерами, поддерживаемыми установленным в системе принтером.

Для pdf  файлов поддерживаются размеры А0 - А4.





![output1](https://github.com/PeftitsNik/suprint/assets/142207234/403b41f9-ca12-4def-82d4-66587cb0a537)







Работа программы протестирована в Windows 10 и Slackware Linux 15.0.


**Запуск программы в Windows 10 и выше**

Перейдите в папку с программой и в командной строке (cmd.exe) введите *py main.py*

либо запустите файл *win_start.bat*

**Зависимости:**

1. python >= 3.10
2. pyqt >= 6.1

**Замечание для Windows:**

а) если не установлен python - скачать с [официального сайта](https://www.python.org/downloads/) и установить;

б) в командной строке (cmd.exe) набрать *pip3 install PyQt6.*

**Быстродействие**

Программа (suprint) открывает большие изображения достаточно долго.
Так, например, ноутбук под управлением Windows 10 (Intel Pentium CPU 5405U @ 2.30GHz, оперативная память 8 ГБ и дискретная видеокарта NVIDIA GeForce MX110) открывает изображение размером 235 МБ за 15 сек.
