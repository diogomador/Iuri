// Selecionando elementos do DOM
const addTaskBtn = document.getElementById('add-task-btn');
const taskInput = document.getElementById('task-input');
const taskList = document.getElementById('task-list');

// Função para adicionar tarefa
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText !== '') {
        const li = document.createElement('li');
        li.textContent = taskText;

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Remover';
        deleteBtn.onclick = () => li.remove();

        li.appendChild(deleteBtn);
        taskList.appendChild(li);
        taskInput.value = '';
    }
}

// Adicionando evento ao botão
addTaskBtn.addEventListener('click', addTask);

// Permite adicionar tarefa com a tecla Enter
taskInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        addTask();
    }
});
