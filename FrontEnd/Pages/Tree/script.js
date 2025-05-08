if (window.Telegram && window.Telegram.WebApp) {
    const initData = window.Telegram.WebApp.initData;
    
    // Парсим initData (он в формате URL-encoded строки)
    const params = new URLSearchParams(initData);
    const userStr = params.get('user'); // Получаем JSON строку с данными пользователя
    
    if (userStr) {
      const user = JSON.parse(userStr);
      const userId = user.id;
      console.log('User ID:', userId);
      console.log('User ID');
    } else {
      console.error('User data not found in initData');
    }
  } else {
    console.error('Telegram WebApp API not available');
  }


const API_BASE_URL = 'http://localhost:8000';
const TEST_TG_ID = 1359587483; // Тестовый TG ID

const MARK_COLORS = {
    3: '#4AB968', // зеленый
    2: '#E6F355', // желтый
    1: '#F35555', // красный
    0: '#D4D4D4', // серый (для mark: 0)
    default: '#D4D4D4' // серый (по умолчанию)
};

async function fetchMarksData(tgId) {
    try {
        const response = await fetch(`${API_BASE_URL}/get_marks/${tgId}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        
        if (data.status && !data.error && data.topics) {
            return data.topics;
        } else {
            console.error('Ошибка в данных тем:', data.info);
            return {};
        }
    } catch (error) {
        console.error('Ошибка при запросе данных тем:', error);
        return {};
    }
}



async function initializeTopics() {
    const container = document.getElementById('flex-container');

    // Показываем заглушку на время загрузки
    container.innerHTML = '<p>Загрузка данных тем...</p>';

    // Получаем данные с сервера
    const topicsData = await fetchMarksData(TEST_TG_ID);

    if (Object.keys(topicsData).length === 0) {
        container.innerHTML = '<p>Не удалось загрузить данные тем</p>';
        return;
    }

    // Очищаем контейнер перед добавлением новых данных
    container.innerHTML = '';

    // Создаем блоки для каждой ветки (раздела)
    Object.keys(topicsData).forEach(branchId => {
        const branch = topicsData[branchId];
        const branchBlock = document.createElement('div');
        branchBlock.textContent = branch.title;
        branchBlock.style.textAlign = 'center';
        branchBlock.style.fontFamily = "Comic Relief";
        
        const topicsContainer = document.createElement('div');

        // Создаем кнопки для каждой темы
        Object.keys(branch.topics).forEach(topicId => {
            const topic = branch.topics[topicId];
            const topicBtn = document.createElement('button');

            // Устанавливаем цвет в зависимости от оценки
            topicBtn.style.backgroundColor = MARK_COLORS[topic.mark] || MARK_COLORS.default;
            
            // Добавляем изображение, если оно есть
            if (topic.img) {
                const img = document.createElement('img');
                img.src = `../img/Topics/${topic.img}`;
                topicBtn.appendChild(img);
            }

            // Обработчик клика по теме
            topicBtn.addEventListener('click', (event) => {
                showTopicInfo(topic, topicBtn, event);
                highlightSelectedTopic(topicBtn);
            });

            topicsContainer.appendChild(topicBtn);
        });

        branchBlock.appendChild(topicsContainer);
        container.appendChild(branchBlock);
    });
}

// Показывает информацию о теме
function showTopicInfo(topic, topicBtn, event) {
    const infoBlock = document.getElementById('info');
    if (!infoBlock) return;

    const mark = topic.mark;

    // Заполняем информацию
    const titleElement = document.getElementById('title');
    const descriptionElement = document.getElementById('description');
    const pointsElement = document.getElementById('points');
    const markElement = document.getElementById('mark');
    
    if (titleElement) titleElement.textContent = topic.title;
    if (descriptionElement) descriptionElement.textContent = topic.description;
    if (pointsElement) pointsElement.textContent = `${mark*topic["X"]}/${topic["X"]*3}`;

    // Устанавливаем цвет и текст оценки
    if (markElement) {
        markElement.style.backgroundColor = MARK_COLORS[mark] || MARK_COLORS.default;
        markElement.textContent = mark;
    }

    // Позиционируем блок информации
    positionInfoBlock(infoBlock, topicBtn, event);
    infoBlock.style.display = 'block';
}


// Подсвечивает выбранную тему
function highlightSelectedTopic(topicBtn) {
    // Сбрасываем стиль всех кнопок
    document.querySelectorAll('#flex-container button').forEach(btn => {
        btn.style.border = '1px solid #000000';
    });
    // Подсвечиваем текущую
    topicBtn.style.border = '3px solid rgb(0, 82, 97)';
}

// Позиционирует блок информации
function positionInfoBlock(infoBlock, topicBtn, event) {
    const rect = topicBtn.getBoundingClientRect();
    const style = infoBlock.style;
    const infoHeight = 200; // Примерная высота блока информации
    
    if (window.innerWidth > 700) {
        // Позиционируем по центру вертикально
        const centerY = rect.top + window.scrollY + (rect.height / 2) - (infoHeight / 2);
        style.top = `${Math.max(0, centerY)}px`; // Не выходим за верхнюю границу
        
        style.position = "absolute";
        style.width = "300px";
        style.borderRadius = "20px";
        style.bottom = `auto`;
        
        // Горизонтальное позиционирование (как было)
        style.left = (rect.x + 400 > window.innerWidth) 
            ? `${rect.left - 300 - 50}px` 
            : `${rect.left + 100}px`;
    } else {
        // Для мобильной версии оставляем как было (снизу)
        style.left = `0px`;
        style.bottom = `0px`;
        style.position = "fixed";
        style.width = "100%";
        style.borderRadius = "20px 20px 0 0";
    }
}

// Скрываем блок информации при клике вне его
document.addEventListener('click', (event) => {
    const infoBlock = document.getElementById('info');
    if (!infoBlock) return;
    
    if (!infoBlock.contains(event.target) && !event.target.closest('button')) {
        infoBlock.style.display = 'none';
        document.querySelectorAll('#flex-container button').forEach(btn => {
            btn.style.border = '1px solid #000000';
        });
    }
});

// Инициализируем при загрузке страницы
document.addEventListener('DOMContentLoaded', initializeTopics);