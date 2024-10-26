document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const addTaskButton = document.getElementById('add-task');
    const taskList = document.querySelector('#task-list ul');

    // Получение задач с сервера
    const getTasks = async () => {
        const response = await fetch('/tasks');
        const tasks = await response.json();
        console.log(tasks);  // Логируем полученные задачи для отладки
        taskList.innerHTML = '';
        tasks.forEach((task) => {
            const taskItem = document.createElement('li');
            taskItem.textContent = task.task;
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', () => {
                deleteTask(task.id);
            });
            taskItem.appendChild(deleteButton);
            taskList.appendChild(taskItem);
        });
    };

    // Добавление новой задачи на сервер
    const addTask = async (task) => {
        await fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task })
        });
        getTasks();
    };

    // Удаление задачи с сервера
    const deleteTask = async (taskId) => {
        await fetch(`/tasks/${taskId}`, {
            method: 'DELETE'
        });
        getTasks();
    };

    // Обработчик нажатия кнопки добавления задачи
    addTaskButton.addEventListener('click', () => {
        const taskText = taskInput.value.trim();
        if (taskText !== '') {
            addTask(taskText);
            taskInput.value = '';
        }
    });

    // Получение задач при загрузке страницы
    getTasks();
});
