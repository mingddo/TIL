# 1. SQL & ORM 문제풀이



### 선행준비

- sql_orm_practice.zip 파일 다운받고

  ```python
  $ python manage.py migrate
  $ python manage.py loaddata users/users.json
  
  $ python manage.py shell_plus --print-sql
  $ User.objects.count()
  # 100개 나오는지 확인
  ```

  

1) user 테이블 전체 데이터를 조회하시오.

```sql
SELECT * FROM users_user;
```

```python
User.objects.all()
```



2) id가 19인 사람의 age를 조회하시오.

```sql
SELECT age FROM users_user WHERE id = 19;
```

```python
User.objects.filter(id=19).values('age')
or 
User.objects.get(pk=19).age
```



3) 모든 사람의 age를 조회하시오.

```sql
SELECT age FROM users_user;
```

```python
User.objects.values('age')
```



4) age가 40 이하인 사람들의 id와 balance를 조회하시오.

```sql
SELECT id, balance FROM users_user WHERE age <= 40;
```

```python
users = User.objects.filter(age__lte = 40).values('id', 'balance')

for user in users:
  print(user.get('id'))
  print(user.get('balance'))
  
or

users = User.objects.filter(age__lte = 40)
for user in users:
  print(user.id, user.balance)
```



5) last_name이 ‘김’이고 balance가 500 이상인 사람들의 first_name을 조회하시오.

```sql
SELECT first_name FROM users_user WHERE last_name='김' AND balance >= 500;
```

```python
User.objects.filter(last_name='김', balance__gte=500).values('first_name') 
or
User.objects.filter(last_name='김').filter(balance__gte=500).values('first_name')
```



6) first_name이 ‘수’로 끝나면서 행정구역이 경기도인 사람들의 balance를 조회하시오.

```sql
SELECT balance FROM users_user WHERE first_name LIKE '%수' AND country='경기도';
```

```python
User.objects.filter(first_name__endswith=('수'), country='경기도').values('balance')
```

안되는데!

![image-20201008010938390](../../sql/slowstarters/DB-SQL_ORM.assets/image-20201008010938390.png)

7) balance가 2000 이상이거나 age가 40 이하인 사람의 총 인원수를 구하시오.

```sql
SELECT COUNT(*) FROM users_user WHERE balance >= 2000 OR age <= 40;
```

```python
from django.db.models import Q

User.objects.filter(Q(balance__gte=2000) | Q(age__lte=40)).count()
```



8) phone 앞자리가 ‘010’으로 시작하는 사람의 총원을 구하시오.

```sql
SELECT COUNT(*) FROM users_user WHERE phone LIKE '010%';
```

```python
User.objects.filter(phone__startswith='010').count()
```



9) 이름이 ‘김옥자’인 사람의 행정구역을 경기도로 수정하시오.

```sql
UPDATE users_user SET country='경기도' WHERE first_name='옥자' AND last_name='김'
```

```python
User.objects.filter(first_name='옥자', last_name='김').update(country='경기도')

# 결과 확인
User.objects.filter(first_name='옥자', last_name='김')[0].country
or
User.objects.get(first_name='옥자', last_name='김').country
```



10) 이름이 ‘백진호’인 사람을 삭제하시오.

```sql
DELETE FROM users_user WHERE first_name='진호' AND last_name='백';
SELECT * FROM users_user WHERE first_name='진호' AND last_name='백';
```

```python
User.objects.filter(first_name='진호', last_name='백').delete()
or
User.objects.get(first_name='진호', last_name='백').delete()
```



11) balance를 기준으로 상위 4명의 first_name, last_name, balance를 조회하시오.

```sql
SELECT first_name, last_name, balance FROM users_user ORDER BY balance DESC LIMIT 4;
```

```python
users = User.objects.order_by('-balance').values('first_name', 'last_name', 'balance')[:-4]
for user in users:
  print(user.get('last_name'))
  print(user.get('first_name'))
  print(user.get('balance'))
  print('-----------')
```



12) phone에 ‘123’을 포함하고 age가 30미만인 정보를 조회하시오.

```sql
SELECT * FROM users_user WHERE phone LIKE '%123%' AND age < 30;
```

```python
User.objects.filter(phone__contains='123', age__lt=30)
```



13) phone이 ‘010’으로 시작하는 사람들의 행정 구역을 중복 없이 조회하시오.

```sql
SELECT DISTINCT country FROM users_user WHERE phone LIKE '010%';
```

```python
User.objects.filter(phone__startswith='010').values('country').distinct()
```



14) 모든 인원의 평균 age를 구하시오.

```sql
SELECT AVG(age) FROM users.user;
```

```python
from django.db.models import Avg

User.objects.aggregate(Avg('age'))
```



15) 박씨의 평균 balance를 구하시오.

```sql
SELECT AVG(balance) FROM users_user WHERE last_name='박';
```

```python
User.objects.filter(last_name='박').aggregate(Avg('balance'))
```



16) 경상북도에 사는 사람 중 가장 많은 balance의 액수를 구하시오.

```sql
SELECT MAX(balance) FROM users_user WHERE country = '경상북도'
```

```python
from django.db.models import Max

User.objects.filter(country='경상북도').aggregate(Max('balance'))
```



17) 제주특별자치도에 사는 사람 중 balance가 가장 많은 사람의 first_name을 구하시오.

```sql
SELECT first_name FROM users_user WHERE country='제주특별자치도' ORDER BY balance DESC LIMIT 1;
```

```python
User.objects.filter(country='제주특별자치도').order_by('-balance').values('first_name')[0]
User.objects.filter(country='제주특별자치도').order_by('-balance').values('first_name').first()
```



# 모두모두 과목평가 통과합시다!! 빠이팅입니다!

- ##### 다양한 조회 요청 방법

  - **all**

    ```
    Post.objects.all()
    ```

    모든 데이터를 다 가져옵니다.

  - **filter**

    ```
    Post.objects.filter()
    ```

    특정 데이터로 필터링해서 가져옵니다. 인자로는 `필드명=조건값` 이 들어가며 2개 이상 들어갈 경우, 두 조건을 and로 묶어주게 됩니다. or 로 묶어주기 위해서는 아래와 같이 Q 를 사용해야합니다.

    ```
    from django.db.models import Q
    
    Item.objects.filter(Q(title="제목") | Q(content="내용"))
    ```

  - **exclude**

    ```
    Post.objects.exclude()
    ```

    filter 와 상반되는 개념으로, `필드명=조건값` 으로 들어오는 인자를 제외한 나머지 값들을 가져옵니다.

  - **get**

    ```
    Post.objects.get()
    ```

    `필드명=조건값` 를 인자로 가지며, 해당 하는 데이터가 유일하게 존재해야 합니다. 0개이거나 2개 이상이면 에러가 발생합니다.

  - **first**

    ```
    Post.objects.first()
    ```

    가장 첫번째 데이터를 가져옵니다.

  - **last**

    ```
    Post.objects.last()
    ```

    가장 마지막 데이터를 가져옵니다.

  - **index**, **slice**

    ```
    Post.objects[index]
    Post.objects[start:stop:step]
    ```

    python 의 list와 같이 인덱싱 및 슬라이싱이 가능합니다. 단, 음수가 들어갈 수 없습니다.

   

  ##### 조건을 통한 데이터 조회 방법

  `필드명__조건 = 조건값` 을 `filter` 의 인자로 넘겨주줘 다음과 같은 방식으로 조건을 부여하여 조건에 부합되는 데이터를 조회할 수 있습니다. 위에서 정의한 모델에 맞게 예시를 통해 알아보겠습니다.

  각 예시는 언더바를 **두 개** 씩 사용하고 있으므로 헷갈리지 맙시다.

  - 숫자 / 날짜 /시간 필드

    - 필드명__lt

      필드명__lt = 조건값 : 필드명 < 조건값

      ```
      Post.objects.filter(is_published__lt = date(1961,1,1))
      ```

    - 필드명__lte

      필드명__lte = 조건값 : 필드명 <= 조건값

    - 필드명__gt

      필드명__gt = 조건값 : 필드명 < 조건값

    - 필드명__gte

      필드명__gte = 조건값 : 필드명 < 조건값

     

    예시는 전체적으로 비슷하다고 생각되어 첫번째 에서만 기재해주었습니다. 각 알파벳은 의미하는 함축어가 존재하는데, `l 은 less` 를 `g는 greater` 를`t 는 than` 을 `e 는 equal` 을 의미합니다.

     

  - 문자열 필드

    - **필드명__startswith**

    ```
    Post.objects.filter(title__startswich="[Django]")
    ```

    `필드명__startswith = 조건값` 을 통해 조건값으로 시작하는 데이터를 모두 가져옵니다.

    - **필드명__endswith**

    `필드명__endswith = 조건값` 을 통해 조건값으로 끝나는 데이터를 모두 가져옵니다.

    - **필드명__contains**

    `필드명__contains = 조건값` 을 통해 조건값이 포함되는 데이터를 모두 가져옵니다.

    - **필드명__istartswith**

    `필드명__istartswith = 조건값` , startswith 와 동일하지만 대소문자를 구분하지 않습니다.

    - **필드명__iendswith**

    `필드명__iendswith = 조건값` , endswith 와 동일하지만 대소문자를 구분하지 않습니다.

    - **필드명__icontains**

    `필드명__icontains = 조건값`, contains 와 동일하지만 대소문자를 구분하지 않습니다.

     

  ##### 데이터 정렬

  정렬 조건을 지정하는 방법으로는 2가지가 있습니다.

  - **모델 클래스에서 지정**

  ```
  # core/models.py
  
  from django.db import models
  
  class Post(models.Model):
      title = models.CharField(max_length=30)
      content = models.TextField()
      is_published = models.BooleanField(default=False)
      
      class Meta:
        	ordering = ['id']
          # 역순으로 지정
          # ordering = ['-id']
  ```

  Meta 클래스에 `ordering` 을 이용해서 list 로서 지정을 해줍니다.

  클래스에 정렬을 추가하는건 모든 클래스에 다 권장 사항입니다. 데이터베이스가 자체적으로 최적화 하는 과정에서 순서가 바뀔 가능성이 있기 때문에 이를 통해 순서를 보장받을 수 있습니다.

   

  - **queryset에서 지정**

  ```
  Post.objects.all().order_by('id')
  # 역순으로 지정
  Post.objects.all().order_by('-id')
  ```

  다음과 같이 `order_by` 를 통해서 해당 필드 순서로 `queryset`을 정렬합니다.

  두 가지 방식을 동시에 하면 `queryset`에 `order_by` 지정 을 따릅니다.

   