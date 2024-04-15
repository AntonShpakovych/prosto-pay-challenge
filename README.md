## Task1:
 - Implement own hashmap class (put, get methods are required).
 - write tests for this class.
 - add notes with argumentation for chosen implementation.

```shell
1) To run tests you should type: 
  - python task1/test_hashmap.py
  or 
  - cd task1
  - python test_hashmap.py
2) If you want to use it, just create some new file where you can initialize hashmap
```


## Task 2:
 - Write small service class with methods
   - get(user_id) → UserDTO
   - add(user: UserDTO)
   - signatures can be changed if you think it's needed for better implementation

   - UserDTO - pydantic model
   - Users are stored in db.
   - Assume you have method get_async_session, which returns AsyncSession sqlalchemy object to interact with db

 - write tests for that class
 - add notes with argumentation for chosen implementation

```shell
1) cd task2
2) python -m venv venv
3) venv\Scripts\activate
4) pip install -r requirements.txt

- To run tests you should type: pytest tests
- To use it local:
   - create .env file based on .env.example
   - docker compose up --build
   - create some new file where you can initialize service and repository
```