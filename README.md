# armanin-flask
Task Manager Project Documentation

1. Введение
Task Manager — это веб-приложение для управления задачами, разработанное на Flask и работающие с базой данных PostgreSQL. Проект разворачивается в кластере Kubernetes с использованием Minikube.

2. Установка и настройка
Требования:
Docker

Minikube

Kubectl

Git

Шаги установки:
Склонируйте репозиторий проекта:
git clone git@github.com:aisrayelyan/armanin-flask.git
cd task-manager

Соберите Docker-образ приложения:
docker build -t your-dockerhub-username/armanin-flask .

Запустите Minikube:
minikube start --driver=docker --network-plugin=cni --cni=calico
Запушьте образ в Docker Hub:
docker push your-dockerhub-username/armanin-flask
3. Запуск приложения

Применение манифестов Kubernetes:

Примените манифесты:
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml
Запустите Minikube tunnel для доступа к LoadBalancer сервисам:
sudo minikube tunnel --bind-address="*"
Настройте файл /etc/hosts для доступа через домен:
echo "192.168.49.2 task-manager.local" | sudo tee -a /etc/hosts
Откройте браузер и перейдите по адресу:
http://task-manager.local
4. Манифесты Kubernetes

Deployment (deployment.yaml):
apiVersion: apps/v1
kind: Deployment
metadata:
  name: task-manager-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: task-manager
  template:
    metadata:
      labels:
        app: task-manager
    spec:
      containers:
        - name: task-manager-container
          image: your-dockerhub-username/armanin-flask
          ports:
            - containerPort: 5000
Service (service.yaml):
apiVersion: v1
kind: Service
metadata:
  name: task-manager-service
spec:
  selector:
    app: task-manager
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
      nodePort: 32000
  type: NodePort
Ingress (ingress.yaml):
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: task-manager-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: task-manager.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: task-manager-service
            port:
              number: 80
5. Примеры использования
Добавление задачи:
Откройте приложение в браузере.

Введите название задачи в поле ввода и нажмите кнопку "Add Task".

Просмотр и управление задачами:
Список задач отображается в секции "Task List".

Чтобы удалить задачу, нажмите кнопку "Delete" рядом с задачей.

6. Поддержка и контакты
Если у вас возникли вопросы или требуется помощь, пожалуйста, свяжитесь с нашей командой поддержки:

Email: aisrayelyan@gmail.com
https://github.com/aisrayelyan/armanin-flask
