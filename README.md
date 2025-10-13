# suprint 

**Suprint** – программа для печати (или сохранения в pdf, jpg, png) произвольных фрагментов изображения с любыми размерами, поддерживаемыми установленным в системе принтером.

Для pdf  файлов поддерживаются размеры А0 - А4.
<br>

https://github.com/user-attachments/assets/8cba01ce-3bb8-43b0-a4b7-02aa22575eb7

<br>

Работа программы протестирована в Windows 10 и Slackware Linux 15.0.
<br>
<br>

**Запуск программы в Windows 10 и выше:**

Скачайте zip-файл (<> Code -> Download zip)
<br>
<br>

<img width="491" height="300" alt="скачать" src="https://github.com/user-attachments/assets/99d6d275-8bdd-4672-aeac-852a0ef6e0ae" />

<br>
<br>

Распакуйте zip-файл в удобное место. 

Перейдите в папку с программой и в командной строке (cmd.exe) введите *py main.py*

либо запустите файл *win_start.bat*

<br>
<br>

**Зависимости:**

1. python >= 3.9
2. pyqt >= 6.1

<br>
<br>

**Замечание:**

а) если не установлен python - скачать с [официального сайта](https://www.python.org/downloads/) и установить;

б) в командной строке (для Windows  это cmd.exe) набрать *pip3 install PyQt6.*

<br>
<br>

**Быстродействие**

Программа (suprint) открывает большие изображения достаточно долго.
Так, например, ноутбук под управлением Windows 10 (Intel Pentium CPU 5405U @ 2.30GHz, оперативная память 8 ГБ и дискретная видеокарта NVIDIA GeForce MX110) открывает изображение размером 235 МБ за 15 сек.
