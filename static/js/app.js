const API_URL = '/api/tasks'

async function addTask() {
  const titleRaw = document.getElementById('task-title')
  const priorityRaw = document.getElementById('task-priority')
  const messageRaw = document.getElementById('add-message')

  const title = titleRaw.value.trim()
  const priority = priorityRaw.value.trim()

  if (!title) {
    messageRaw.innerHTML = '<div class="alert alert-warning py-2">Введите название задачи</div>'
    return
  }

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({title, priority})
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Ошибка создания')
    }

    titleRaw.vale = ''
    titleRaw.focus()
    messageRaw.innerHTML = '<div class="alert alert-success py-2">Задача добавлена</div>'
    setTimeout(() => { messageRaw.innerHTML = '' }, 2000)

    loadTasks()
  } catch (error) {
    messageRaw.innerHTML = `<div class="alert alert-danger py-2">${error.message}</div>`
  }
}

document.getElementById('add-form').addEventListener('submit', (event) => {
  event.preventDefault()
  addTask()
})

async function removeTask() {

}

async function doneTask() {

}

async function loadTasks() {
  try {
    const response = await fetch(API_URL)
    if (!response) throw new Error(`HTTP ${response.status}`)
    const data = await response.json()
    renderTask(data.tasks)
  } catch (error) {
    console.error('Ошибка загрузки: ', error)
    document.getElementById('task-list').innerHTML =
      '<div class="alert alert-danger">Ошибка загрузки</div>'
  }
}

function renderTask(tasks) {
  const list = document.getElementById("task-list")
  document.getElementById("task-count").textContent = tasks.length

  if (tasks.length === 0) {
    list.innerHTML = '<div class="text-center text-muted py-4">Нет задач. Добавьте первую!</div>'
    return
  }

  list.innerHTML = tasks.map(task => `
    <div class="card task-item mb-2 ${task.status === 'DONE' ? 'done' : ''}">
      <div class="card-body py-2 px-3 d-flex justify-content-between align-items-center">
          <div>
              <span class="task-title fw-bold">${task.title}</span>
              <span class="badge badge-${task.priority} ms-2">${task.priority}</span>
          </div>
          <div>
              ${task.status !== 'DONE'
                  ? `<button class="btn btn-sm btn-success me-1" onclick="markDone('${task.id}')"><i class="bi bi-check-lg"></i></button>`
                  : `<span class="badge bg-success me-1">DONE</span>`}
              <button class="btn btn-sm btn-danger" onclick="deleteTask('${task.id}')"><i class="bi bi-trash"></i></button>
          </div>
      </div>
    </div>
  `).join('')
}

loadTasks()
