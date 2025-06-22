const form = document.getElementById('taskForm');
form.hidden = true;

const addBtn = document.getElementById('add-task-btn');
const flashMessage = document.getElementById('flash-message');
const taskTableContainer = document.getElementById('task-table-container');
const taskTableBody = document.getElementById('task-table-body');
const spinner = document.getElementById('spinner');
const noTasks = document.getElementById('no-tasks');

form.classList.add('collapsed');

// Toggle task form with animation
addBtn.addEventListener('click', () => {
  if (form.classList.contains('collapsed')) {
    form.classList.remove('collapsed');
    requestAnimationFrame(() => form.classList.add('active'));
  } else {
    form.classList.remove('active');
    setTimeout(() => form.classList.add('collapsed'), 300);
  }
});

// Flash messages
function showFlashMessage(text, type) {
  flashMessage.textContent = text;
  flashMessage.className = type === 'success' ? 'success' : 'error';
  flashMessage.style.display = 'block';
  setTimeout(() => flashMessage.style.display = 'none', 5000);
}

// Color gradient from green (far) to red (near)
function getDeadlineColor(hoursLeft) {
  const max = 48;
  const ratio = Math.max(0, Math.min(1, hoursLeft / max));
  const red = Math.floor(255 * (1 - ratio));
  const green = Math.floor(180 * ratio);
  return `rgb(${red}, ${green}, 80)`;
}

// Load tasks from API
async function loadTasks(showSpinner = true) {
  const spinnerDelay = showSpinner
    ? new Promise(resolve => {
        spinner.style.display = 'block';
        setTimeout(resolve, 3000); // Minimum 3 seconds spinner
      })
    : Promise.resolve();

  try {
    const fetchTasks = fetch('/api/tasks').then(res => res.json());
    const [tasks] = await Promise.all([fetchTasks, spinnerDelay]);

    taskTableBody.innerHTML = '';

    if (tasks.length === 0) {
      noTasks.style.display = 'block';
      taskTableContainer.style.display = 'none';
      return;
    }

    noTasks.style.display = 'none';
    taskTableContainer.style.display = 'block';

    const now = new Date();

    tasks.forEach(task => {
      const deadline = new Date(task[2]);
      const hoursLeft = (deadline - now) / (1000 * 60 * 60);
      const isOverdue = hoursLeft <= 0;

      const row = document.createElement('tr');
      row.classList.add('task-row');
      if (isOverdue) {
        row.classList.add('overdue');
      }

      const color = getDeadlineColor(hoursLeft);
      const circle = `<span class="indicator" style="background-color: ${color};"></span>`;

      row.innerHTML = `
        <td>${circle}</td>
        <td>${task[1]}</td>
        <td>${task[2]}</td>
        <td>${task[3]}</td>
        <td><button class="done-btn" onclick="markAsDone('${task[0]}')">Done</button></td>
      `;
      taskTableBody.appendChild(row);
    });
  } catch (err) {
    showFlashMessage('❌ Failed to fetch tasks', 'error');
    console.error(err);
  } finally {
    spinner.style.display = 'none';
  }
}

// Submit new task
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  spinner.style.display = 'block';

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  try {
    const res = await fetch('/submitData', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    if (result.success) {
      showFlashMessage('✅ Task Added', 'success');
      form.reset();
      form.classList.remove('active');
      setTimeout(() => form.hidden = true, 300);
      await loadTasks(false);
    } else {
      showFlashMessage('❌ Error Adding Task', 'error');
    }
  } catch (err) {
    showFlashMessage('❌ Server Error', 'error');
    console.error(err);
  } finally {
    spinner.style.display = 'none';
  }
});

// Mark a task as completed
async function markAsDone(taskId) {
  try {
    const res = await fetch(`/remove?id=${taskId}`, { method: 'DELETE' });
    const result = await res.json();

    if (result.success) {
      showFlashMessage('🎉 Task completed!', 'success');

      const rows = document.querySelectorAll('#task-table-body tr');
      for (const row of rows) {
        if (row.innerHTML.includes(`markAsDone('${taskId}')`)) {
          row.classList.add('removing');
          setTimeout(async () => {
            row.remove();
            const remainingRows = document.querySelectorAll('#task-table-body tr');
            if (remainingRows.length === 0) {
              noTasks.style.display = 'block';
              taskTableContainer.style.display = 'none';
            }
          }, 500);
          break;
        }
      }
    } else {
      showFlashMessage("😅 Task may not exist anymore.", 'error');
    }
  } catch (err) {
    showFlashMessage('❌ Server Error during deletion', 'error');
    console.error(err);
  }
}

// Initial load + refresh every 30s
window.onload = () => {
  loadTasks(true);
  setInterval(() => loadTasks(false), 30000);
};

document.getElementById("stop-server-btn").addEventListener("click", () => {
    fetch("/home?endpt=stop")
        .then(response => response.json())
        .then(data => {
            if (data.status === true) {
                showStopMessage("Application Closed");
            } else {
                showStopMessage("Unexpected response from server");
            }
        })
        .catch(() => {
            showStopMessage("Application already closed");
        });
});

function showStopMessage(message) {
    const msgBox = document.getElementById("stop-message");
    msgBox.textContent = message;
    msgBox.style.display = "block";

    setTimeout(() => {
        msgBox.style.display = "none";
    }, 5000);
}
