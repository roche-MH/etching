# apache + django + mysql

```python
conda create -n test python=3.5 ##3.6은 하지마세요 하루 꼬박 에러 찾았움 버전호환
conda activate test
pip install django
```

위 두개로 가상환경과 django 기본을 깔아준다.

```python
django-admin startproject beauty
```

![image-20200529141806921](C:\Users\s_m04\OneDrive\바탕 화면\mini_project\makeapp\image-20200529141806921.png)

`manage.py`: Django 프로젝트와 다양한 방법으로 상호작용 하는 커맨드라인의 유틸리티 입니다. `manage.py` 에 대한 자세한 정보는 [django-admin and manage.py](https://django-document-korean.readthedocs.io/ko/master/ref/django-admin.html) 에서 확인할 수 있습니다.

`auth 폴더` : mysql.cnf 는 django 와 mysql 설정에 필요한 정보를 담고 있습니다.

`logs 폴더` : apache2 에서 발생하는 에러들을 따로 로그폴더를 만들어서 관리하기 위해 만들어놨습니다

`beauty/` 디렉토리 내부에는 project 를 위한 실제 Python 패키지들이 저장됩니다. 이 디렉토리 내의 이름을 이용하여, (`beauty.urls` 와 같은 식으로) project 어디서나 Python 패키지들을 import 할 수 있습니다.

`beauty/settings.py`: 현재 Django project 의 환경/구성을 저장합니다. [Django settings](https://django-document-korean.readthedocs.io/ko/master/topics/settings.html) 에서 환경 설정이 어떻게 동작하는지 확인할 수 있습니다.

`beauty/urls.py`: 현재 Django project 의 URL 선언을 저장합니다. Django 로 작성된 사이트의 “목차” 라고 할 수 있습니다. [URL dispatcher](https://django-document-korean.readthedocs.io/ko/master/topics/http/urls.html) 에서 URL 에 대한 자세한 내용을 읽어보세요.

`beauty/wsgi.py`: 현재 project 를 서비스 하기 위한 WSGI 호환 웹 서버의 진입점 입니다. [How to deploy with WSGI](https://django-document-korean.readthedocs.io/ko/master/howto/deployment/wsgi/index.html) 를 읽어보세요.

```python
python manage.py runserver 0.0.0.0:8888
```

![image-20200529142139124](https://t1.daumcdn.net/cfile/tistory/99C88A33598425D326)

다음과 같이 오류가 날수 있으나 웹페이지는 실행이 됨, migrate 는 mysql 과 연동을 같이 함으로 mysql.cnf 를 settings 에 넣어줘서 migrate를 해준다.

![image-20200529142300422](C:\Users\s_m04\OneDrive\바탕 화면\mini_project\makeapp\image-20200529142300422.png)

settings 파일에 사진과 같이 변경하고 mysql 에 접속해서 명령어를 쳐준다.

```sql
apt-get install mysql-python
pip install mysql-client
create user 'username'@'localhost' IDENTIFIED by 'password'
create database beauty;
grant all privileges on beauty.* to 'username'@'localhost';
flush privileges;

```

위 명령어를 쳐서 데이터 베이스와 유저를 생성한후 유저에게 권한을 주었고 이를 완료하면

```python
python manage.py check #이상이 없으면
python manage.py migrate
```

ok 가 뜬다면 성공적으로 완료되었다.

이후 mysql 에 접속하여 beauty database 의 내용을 확인한다.



이후 jango를 실행해서 접속이 되는지 확인한다. 로컬접속은 잘되지만 외부에서 접속은 안되기 때문에

settings > ALLOWED_HOSTS =[] 이부분에 ip나 '*' 를 넣어준다.



## apache2 연동

아파치 설치

```bash
sudo apt-get install apache2
를 설치해서 default page 가 뜨는지 확인한다.
```

jango + apache 를 연결하기위해서는 mod-wsgi 가 필요하다

wsgi는 jango 가 was의 역활을 할수 있도록 해주면서 연동에 필요하다

```bash
apt-get install libapache2-mod-wsgi-py3 # python.3.5
vim /etc/apache2/sites-available/000-default.conf
```

```python
<VirtualHost *:8888>
        ErrorLog /var/www/beauty/logs/error.log
        ServerName beauty

        <Directory /var/www/beauty/beauty>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>
        WSGIDaemonProcess beauty python-path=/home/ubuntu/anaconda3/envs/test/lib/python3.5/site-packages
        WSGIProcessGroup beauty
        WSGIScriptAlias / /var/www/beauty/beauty/wsgi.py process-group=beauty


</VirtualHost>
```

도메인을 로컬로 사용할수 있도록 설정

```bash
vim /etc/hosts
127.0.0.1	beauty
```

python-path=/home/ubuntu/anaconda3/envs/test/lib/python3.5/site-packages

는 anaconda python 가상환경을 쓰기 때문에 가상환경의 site-packages를 실행 해줘야 한다.

```bash
sudo vim /etc/apache2/ports.conf
Listen 8888
service apache2 restart
```

![image-20200529155306750](C:\Users\s_m04\OneDrive\바탕 화면\mini_project\makeapp\image-20200529155306750.png)

anaconda 환경에서 연동할경우 wsgi.py 파일 수정이 필요하다.

```python
"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os,sys
path = os.path.abspath(__file__+'/../..')
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
```

```python
#수정후 리스타트를 한다면 접속이 될것이다.
service apache2 restart
```

