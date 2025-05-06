const API_BASE_URL = 'http://localhost:8000'; // Убедитесь, что совпадает с адресом вашего FastAPI сервера
const TEST_TG_ID = 1359587483; // Тестовый TG ID

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

  // Получаем данные с сервера
  const [groupRating, kvantRating] = await Promise.all([
    fetchGroupRating(TEST_TG_ID),
    fetchKvantRating(TEST_TG_ID)
  ]);

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