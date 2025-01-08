# dgi-skeleton

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

dgi-skeleton merupakan library untuk membuat template Django project yang telah distandarisasi

## Struktur Project

```
root_directory
├── apps
│   ├── user
│   │   ├──── api
│   │   │   ├──── __init__.py
│   │   │   ├──── serializers.py
│   │   │   ├──── urls.py
│   │   │   └──── views.py
│   │   ├──── migrations
│   │   ├──── __init__.py
│   │   ├──── admin.py
│   │   ├──── apps.py
│   │   ├──── cron.py
│   │   ├──── models.py
│   │   ├──── tests.py
│   │   └──── views.py
│   ├── utils
│   │   ├──── __init.py__
│   │   ├──── models.py
│   │   └──── pagination.py
│   └── __init__.py
├── configs
│   ├── __init__.py
│   ├── asgi.py
│   ├── healthcheck.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── .gitignore
├── Dockerfile
├── manage.py
└── requirements.txt
```

### `admin.py`

models yang akan didaftarkan di django admin didefinisikan menggunakan decorator `@admin.register(modelnya)`, contoh penggunaan:

```python
from django.contrib import admin

from apps.user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('kolom1', 'kolom2', 'kolom3', 'kolom..n')
    search_fields = ('kolom1', 'kolom2', 'kolom..n')
    autocomplete_fields = ('kolom1', 'kolom2', 'kolom..n') # jika ada relasi ke tabel lain
```

### `models.py`

semua class models harus diturunkan dari `class BaseModel` yang telah didefinisikan pada file `apps/utils/models.py`, contoh penggunaan:

```python
from django.db import models

from apps.utils.models import BaseModel

class MyModel(BaseModel):
    # kolom ...
    pass
```

untuk model user yang digunakan sebagai akses login ke django admin atau ke api, dapat menggunakan model yang telah didefinisikan pada file `apps/user/models.py`

```python
class User(AbstractUser):
   pass
```

model tersebut menggunakan `username` sebagai default identifier, jika terdapat kebutuhan untuk mengubah menjadi `email` atau field lain, bisa dilakukan dengan menambahkan atribut `USERNAME_FIELD`, contohnya seperti:

```python
class User(AbstractUser):
   email = models.EmailField(unique=True) # atau field lain

   USERNAME_FIELDS = 'email' # atau field lain
```
catatan:
khusus untuk email, diperlukan untuk mengubah atribut `REQUIRED_FIELDS` menjadi
```python
class User(AbstractUser):
   email = models.EmailField(unique=True)

   USERNAME_FIELDS = 'email'
   REQUIRED_FIELDS = ('first_name', 'last_name', 'username') # ... field lainnya selain email
```

dokumentasi: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

### `apps.py`

karena app django nya berada dalam directory `apps`, maka terdapat beberapa bagian yang harus diubah, di antaranya adalah:

- `/{nama_appnya}/apps.py`

   ubah atribut `name` contohnya seperti:

   ```python
   class UserConfig(AppConfig):
      # ...
      name = 'apps.user' # sebelumnya name = 'user'
   ```

- `settings.py`

   dalam variabel `INSTALLED_APPS` tambahkan `apps.user`, contohnya seperti:

   ```python
   INSTALLED_APPS = [
      # ....
      'apps.user',
   ]
   ```

### `cron.py`

file ini digunakan jika terdapat kebutuhan untuk menggunakan cron. Cron yang digunakan adalah [django-cron](https://django-cron.readthedocs.io/en/latest/installation.html). Contoh penggunaannya:

1. Buat cron
   ```python
   from django_cron import CronJobBase, Schedule

   class MyCronJob(CronJobBase):
      RUN_EVERY_MINS = 120 # setiap 2 jam

      schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
      code = 'apps.namaappnya.cron.my_cron_job' # kode unit cron

      def do(self):
         pass # script cronnya
   ```

2. Daftarkan cron di variabel `CRON_CLASSES` pada file `settings.py`
   ```python
   CRON_CLASSES = [
      'apps.namaappnya.cron.my_cron_job',
      # ...
   ]
   ```

3. Jalankan cron menggunakan `python manage.py runcrons`

### `tests.py`

usahakan untuk selalu membuat test code untuk mengetahui ketika terjadi perubahan, perubahan tersebut tidak menyebabkan error. Contoh test code sederhana anggaplah terdapat class `Barista` dengan method `buat_kopi()` dengan return value class `Kopi`

```python
class Kopi:
   pass

class Barista:
   def buat_kopi():
      # ...
      return Kopi()
```

```python
from django.test import TestCase

class BaristaTestCase(TestCase):
   def test_buat_kopi(self):
      barista = Barista()
      result = barista.buat_kopi()

      self.assertIsInstance(result, Kopi)
```

untuk menjalankan testnya dapat menggunakan perintah `python manage.py test`

### `api/serializers.py`

file ini berisikan semua class serializer yang terdapat dalam app yang bersangkutan, terdapat banyak sekali jenis serializer yang dapat digunakan, untuk itu gunakanlah sesuai kebutuhan yang ada. Selain itu hindari `query` dalam method untuk serializer dengan argument `many=True` karena akan mempengaruhi performa query, contohnya

`models.py`
```python
from django.db import models

from apps.utils.models import BaseModel

class Author(BaseModel):
   name = models.CharField(max_length=100)
   # ...

class Blog(BaseModel):
   author = models.ForeingKey(Author, on_delete=models.CASCADE, related_name='blogs')
   # ...
```

`api/serializers.py`
```python
from rest_framework import serializers

from .models import Author, Blog

class ListAuthorSerializer(serializers.ModelSerializer):
   jumlah_blog = serializers.SerializerMethodField()

   def get_jumlah_blog(self, obj):
      jumlah_blog = Blog.objects.filter(author=obj).count()
      return jumlah_blog
   
   class Meta:
      model = Author
      fields = ('id', 'name', 'jumlah_blog')
```

`api/views.py`
```python
from .models import Author
from .serializers import ListAuthorSerializer

# ...
def get(self, request):
   authors = Author.objects.all()
   serializer = ListAuthorSerializer(authors, many=True)
   return serializer.data
```

contoh di atas akan mengakibatan terjadinya `N+1` query, jika terdapat 10 `Author` maka yang akan terjadi adalah 1 query untuk semua `Author` dan 10 query untuk masing-masing `Author` untuk menghitung jumlah `Blog`. Hal di atas dapat dihindari dengan menggunakan mendapatkan jumlah blog dari `views.py` kemudian akses value nya dari serializer. Contohnya

`api/views.py`
```python
from django.db.models import Count

from .models import Author
from .serializers import ListAuthorSerializer

# ...
def get(self, request):
   authors = Author.objects.annotate(jumlah_blog=Count('blogs'))
   serializer = ListAuthorSerializer(authors, many=True)
   return serializer.data
```

`api/serializers.py`
```python
from rest_framework import serializers

from .models import Author, Blog

class ListAuthorSerializer(serializers.ModelSerializer):
   jumlah_blog = serializers.IntegerField()
   
   class Meta:
      model = Author
      fields = ('id', 'name', 'jumlah_blog')
```

### `api/views.py`



























## Penggunaan

### Instalasi
   ```bash
   pip install dgi-skeleton
   ```

### Inisiasi Project
   1. Buat django project
      ```bash
      dgi-skeleton startproject {namaproject}
      ```
   2. Masuk ke directory `{namaproject}` yang telah dibuat, kemudian install dependency:
      ```bash
      pip install -r requirements.txt
      ```
   3. Ubah config `.env` sesuai kebutuhan

### Membuat App Baru
   1. Masuk ke directory apps
      ```bash
      cd apps
      ```
   2. Buat app baru
      ```bash
      dgi-skeleton startapp {namaapp}
      ```
   atau dari directory root sejajar dengan file `manage.py` jalankan
   ```bash
   dgi-skeleton startapp {namaapp} --destination ./apps
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Referensi

- [Django](https://docs.djangoproject.com/en/dev)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)
- [DRF Standarized Errors](https://drf-standardized-errors.readthedocs.io/en/latest/)
- [django-cron](https://django-cron.readthedocs.io/en/latest/index.html)
