document.addEventListener('touchmove', function(e) {
  // Если контент уже вверху или внизу — блокируем стандартное поведение
  const scroller = e.target.closest('.scrollable-element');
  if (scroller) {
    const isTop = scroller.scrollTop <= 0;
    const isBottom = scroller.scrollTop + scroller.clientHeight >= scroller.scrollHeight;
    if ((isTop && e.deltaY < 0) || (isBottom && e.deltaY > 0)) {
      e.preventDefault();
    }
  }
}, { passive: false });


const userId = 0

if (window.Telegram && window.Telegram.WebApp) {

    window.Telegram.WebApp.disableVerticalSwipes()

    const initData = window.Telegram.WebApp.initData;

    // Парсим initData (он в формате URL-encoded строки)
    const params = new URLSearchParams(initData);
    const userStr = params.get('user'); // Получаем JSON строку с данными пользователя

        if (userStr) {
            const user = JSON.parse(userStr);
            const userId = user.id;
            console.log('User ID:', userId);
        } else {
            console.error('User data not found in initData');
        }
    } else {
    console.error('Telegram WebApp API not available');
}

const API_BASE_URL = 'http://localhost:8000'; // Убедитесь, что совпадает с адресом вашего FastAPI сервера

async function fetchGroupRating(tgId) {
  try {
    const response = await fetch(`${API_BASE_URL}/get_group_raiting/${tgId}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    return data.group_rating || [];
  } catch (error) {
    console.error('Ошибка при запросе рейтинга группы:', error);
    return [];
  }
}

async function fetchKvantRating(tgId) {
  try {
    const response = await fetch(`${API_BASE_URL}/get_kvant_raiting/${tgId}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    return data.kvant_rating || [];
  } catch (error) {
    console.error('Ошибка при запросе рейтинга параллели:', error);
    return [];
  }
}

function createStudentElement(student, index, isLeader = false) {
  const studentDiv = document.createElement('div');
  studentDiv.className = 'student';

  if (isLeader) {
    studentDiv.id = ['zero', 'first', 'second', 'third'][index] || '';
  }

  // Обрабатываем разные названия поля с баллами (point/points)
  const points = student.points !== undefined ? student.points : student.point;

  studentDiv.innerHTML = isLeader
    ? `
      <div class="rank"><div class="text">${points} б.</div></div>
      <div class="name"><div class="text">${student.surname} ${student.name}</div></div>
      <div class="score"><div class="text">${student.group || ''}</div></div>
    `
    : `
      <div class="rank"><div class="text">${index + 1}</div></div>
      <div class="name"><div class="text">${student.surname} ${student.name}</div></div>
      <div class="score"><div class="text">${points} б.</div></div>
    `;

  return studentDiv;
}

async function initializeRatings() {
  const groupContainer = document.getElementById('group');
  const leadersContainer = document.getElementById('leaders')?.querySelector('#top');
  
  if (!groupContainer || !leadersContainer) {
    console.error('Не найдены контейнеры для рейтингов');
    return;
  }

  // Показываем заглушки на время загрузки
  groupContainer.innerHTML = '<p>Загрузка рейтинга группы...</p>';
  leadersContainer.innerHTML = '<p>Загрузка топ лидеров...</p>';

  let groupRating = []
  let kvantRating = []

  // Получаем данные с сервера
  if (userId != 0) {
    [groupRating, kvantRating] = await Promise.all([
      fetchGroupRating(userId),
      fetchKvantRating(userId)
    ]);
  } else {
    groupRating = [{'id': 4, 'name': 'Алексей ', 'surname': 'Романов ', 'points': 75}, {'id': 7, 'name': 'Максим ', 'surname': 'Морозов ', 'points': 50}, {'id': 2, 'name': 'Дмитрий ', 'surname': 'Кузнецов ', 'points': 25}, {'id': 8, 'name': 'Ольга ', 'surname': 'Волкова ', 'points': 25}, {'id': 1, 'name': 'Даниил', 'surname': 'Леонов', 'points': 0}, {'id': 3, 'name': 'Мария ', 'surname': 'Романова ', 'points': 0}, {'id': 5, 'name': 'Андрей ', 'surname': 'Сидоров ', 'points': 0}, {'id': 6, 'name': 'Юрий ', 'surname': 'Петров ', 'points': 0}, {'id': 9, 'name': 'Сергей ', 'surname': 'Соколов ', 'points': 0}, {'id': 10, 'name': 'Татьяна ', 'surname': 'Иванова ', 'points': 0}]
    kvantRating = [{'student_id': 4, 'name': 'Алексей ', 'surname': 'Романов ', 'group': 'С-IT-1', 'points': 75}, {'student_id': 12, 'name': 'Алексей ', 'surname': 'Сидоров ', 'group': 'C-IT-3', 'points': 75}, {'student_id': 7, 'name': 'Максим ', 'surname': 'Морозов ', 'group': 'C-IT-1', 'points': 50}, {'student_id': 11, 'name': 'Наталья ', 'surname': 'Кузнецова ', 'group': 'C-IT-2', 'points': 50}]
  }  

  // Очищаем контейнеры перед добавлением новых данных
  groupContainer.innerHTML = '';
  leadersContainer.innerHTML = '';

  // Заполняем рейтинг группы
  if (groupRating.length > 0) {
    groupRating.forEach((student, index) => {
      // Добавляем поддержку старой структуры данных
      const normalizedStudent = {
        ...student,
        point: student.points !== undefined ? student.points : student.point
      };
      groupContainer.appendChild(createStudentElement(normalizedStudent, index));
    });
  } else {
    groupContainer.innerHTML = '<p>Нет данных о рейтинге группы</p>';
  }

  // Заполняем топ лидеров
  if (kvantRating.length > 0) {
    kvantRating.forEach((student, index) => {
      // Добавляем поддержку старой структуры данных
      const normalizedStudent = {
        ...student,
        point: student.points !== undefined ? student.points : student.point
      };
      leadersContainer.appendChild(createStudentElement(normalizedStudent, index, true));
    });
  } else {
    leadersContainer.innerHTML = '<p>Нет данных о топ лидерах</p>';
  }
}

// Инициализируем при загрузке страницы
document.addEventListener('DOMContentLoaded', initializeRatings);
