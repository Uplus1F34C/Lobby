async function fetchAchievements(tgId) {
  const API_BASE_URL = 'http://localhost:8000'; // Убедитесь, что это совпадает с адресом вашего FastAPI сервера
  
  try {
    const response = await fetch(`${API_BASE_URL}/get_achivments/${tgId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (data.status && !data.error && data.achivments) {
      return data.achivments;
    } else {
      console.error('Ошибка в данных достижений:', data.info);
      return {};
    }
  } catch (error) {
    console.error('Ошибка при запросе достижений:', error);
    return {};
  }
}

async function initializeAchievements() {
  const tgId = 1359587483; // Тестовый TG ID
  const hexGrid = document.getElementById('hexGrid');
  
  // Показываем заглушку на время загрузки
  hexGrid.innerHTML = '<p>Загрузка достижений...</p>';
  
  // Получаем достижения с сервера
  const achievements = await fetchAchievements(tgId);
  
  // Если достижений нет, показываем сообщение
  if (Object.keys(achievements).length === 0) {
    hexGrid.innerHTML = '<p>Не удалось загрузить достижения</p>';
    return;
  }

  // Функция для создания HTML-элемента достижения
  function createAchievementElement(key, achievement) {
    const li = document.createElement('li');
    li.className = 'hex';
    
    const bgColor = achievement.status 
      ? (achievement.type === "Achivment" ? "#00FFC3" : "#FF3333")
      : "gray";

    li.innerHTML = `
      <a class="hexIn" style="background-color: ${bgColor}">
        <img src="../img/Achivment/${achievement.img}.png" alt="${key}">
        <h1 id="title">${key}</h1>
        <p id="description">
          ${achievement.description}
          ${achievement.point !== 0 ? `<br><b><small>Награда:<br>${achievement.point} б.</small><b>` : ''}
        </p>
      </a>
    `;

    return li;
  }

  // Очищаем сетку перед добавлением новых элементов
  hexGrid.innerHTML = '';

  // Генерация элементов для всех достижений
  for (const [key, achievement] of Object.entries(achievements)) {
    hexGrid.appendChild(createAchievementElement(key, achievement));
  }
}

// Инициализируем при загрузке страницы
document.addEventListener('DOMContentLoaded', initializeAchievements);