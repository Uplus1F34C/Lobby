const userId = 0

if (window.Telegram && window.Telegram.WebApp) {
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

const API_BASE_URL = 'http://localhost:8000'; // Убедитесь, что это совпадает с адресом вашего FastAPI сервера

function getRandomBoolean() {
    return Math.random() < 0.5
}

async function fetchAchievements(tgId) {
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
  const hexGrid = document.getElementById('hexGrid');
  
  // Показываем заглушку на время загрузки
  hexGrid.innerHTML = '<p>Загрузка достижений...</p>';

  let achievements = {}
  
  // Получаем достижения с сервера
  if (userId != 0) {
    achievements = await fetchAchievements(userId);
  } else {
    achievements = {
    "Кормилец": {
        "description": "Принеси вкусняшки к чаю",
        "type": "Achivment",
        "img": "Food",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Волонтер": {
        "description": "Стань волонтером кванториума",
        "type": "Achivment",
        "img": "GoodBoy",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Денис": {
        "description": "Допрыгни до потолка",
        "type": "Achivment",
        "img": "Denis",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Местный Жуков": {
        "description": "Хорошо покажи себя в роли тимлида",
        "type": "Achivment",
        "img": "teamlid",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Эврика!": {
        "description": "Найди неожиданное и эффективное решение проблемы",
        "type": "Achivment",
        "img": "idea",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Победитель": {
        "description": "Займи призовое место в не групповом соревновании",
        "type": "Test",
        "img": "Medal",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Отличник": {
        "description": "Получи максимально возможную оценку за год",
        "type": "Test",
        "img": "Profy",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Как?": {
        "description": "Получи максимально возможное количество баллов",
        "type": "Test",
        "img": "que",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Превозмог": {
        "description": "Выйди со своим проектом на коллаборацию",
        "type": "Test",
        "img": "Star",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Активный": {
        "description": "Сходи на мероприятие кванториума",
        "type": "Achivment",
        "img": "event",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Командный игрок": {
        "description": "Прими активное участие в командной работе",
        "type": "Achivment",
        "img": "group",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Это моё?": {
        "description": "Создай свой кейс или проект",
        "type": "Achivment",
        "img": "Hummer",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Мастер": {
        "description": "Принеси настольную игру",
        "type": "Achivment",
        "img": "GameMaster",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Оратор": {
        "description": "Покажи всем, как надо говорить на публике",
        "type": "Achivment",
        "img": "micro",
        "status": getRandomBoolean(),
        "point": 25
    }
}
  }
  
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