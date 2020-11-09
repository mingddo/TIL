from time import sleep

'''
def sleep_3_seconds():
    sleep(3)
    print('잘잤다!')

print('이제 잘거다!')
sleep_3_seconds()
print('학교간다!')
'''


import requests
import json


response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
# print(response.text)
# print(response.text.get('title'))

todo = response.json()
print(todo)
# todo_title = todo.get('title')

# print(todo_title)
