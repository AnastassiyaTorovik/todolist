# TODOlist

## Usage

You need to have Docker installed to use TODOlist on your local computer.

Clone the project and run the following commands to start the app:

```
cd todolist
docker-compose up -d
```
Application will be running on 127.0.0.1:8080

If you want to stop the app run:
```
docker-compose stop
```

These commands will delete the app containers with volumes and will remove the image
```
docker-compose down -v
docker image rm todolist_todo-list
```

