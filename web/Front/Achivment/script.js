let userId = 0;
const API_BASE_URL = 'http://localhost:8000';


function getRandomBoolean() {
  return Math.random() >= 0.5;
}
// Данные для гостя
const GuestData = {
    "Кормилец": {
        "description": "Принеси вкусняшки к чаю",
        "img": "Food",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Волонтер": {
        "description": "Стань волонтером кванториума",
        "img": "GoodBoy",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Местный Жуков": {
        "description": "Хорошо покажи себя в роли тимлида",
        "img": "teamlid",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Эврика!": {
        "description": "Найди эффективное решение проблемы",
        "img": "idea",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Победитель": {
        "description": "Выйграй в соревновании кванториума",
        "img": "Medal",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Отличник": {
        "description": "Получи максимум баллов",
        "img": "Profy",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Превозмог": {
        "description": "Выйди со своим проектом на коллаборацию",
        "img": "Star",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Активный": {
        "description": "Сходи на мероприятие кванториума",
        "img": "event",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Командный игрок": {
        "description": "Будь активным в команде",
        "img": "group",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Это моё?": {
        "description": "Создай свой кейс или проект",
        "img": "Hummer",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Оратор": {
        "description": "Покажи всем, как надо выступать на публике",
        "img": "Micro",
        "status": getRandomBoolean(),
        "point": 25
    },
    "Мастер": {
        "description": "Принеси настольную игру",
        "img": "GameMaster",
        "status": getRandomBoolean(),
        "point": 25
    }
}
let userData = { name: "Гость", group: "C-IT-1", points: "0" };
let AchievementsData = {};

// Инициализация Telegram WebApp
function initTelegramWebApp() {
    if (window.Telegram?.WebApp) {
        const TG = window.Telegram.WebApp;
        TG.disableVerticalSwipes();
        
        try {
            const user = JSON.parse(new URLSearchParams(TG.initData).get('user'));
            if (user?.id) userId = user.id;
        } catch (e) {
            console.error('Ошибка парсинга данных пользователя:', e);
        }
    }
}

// Загрузка данных с сервера
async function fetchData() {
    if (userId === 0) {
        AchievementsData = GuestData;
        return;
    }

    try {
        const [achivmentsRes, userRes] = await Promise.all([
            fetch(`${API_BASE_URL}/get_achivments/${userId}`),
            fetch(`${API_BASE_URL}/get_student/${userId}`)
        ]);

        if (!achivmentsRes.ok || !userRes.ok) {
            throw new Error('Ошибка HTTP запроса');
        }

        const [achivments, user] = await Promise.all([achivmentsRes.json(), userRes.json()]);

        if (achivments.status && user.status) {
            AchievementsData = achivments.achivments || GuestData;
            userData = {
                name: user.name || "Гость",
                group: user.group || "C-IT-1",
                points: user.points || "0"
            } 
        } else {
            AchievementsData = GuestData
            userData = {
                name: "Гость",
                group: "C-IT-1",
                points: "0"
            }
        };
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        AchievementsData = GuestData;
    }
}

// Создание элементов достижений
function createAchievements() {
    const container = document.getElementById('Achivment-container');
    container.innerHTML = '';

    Object.entries(AchievementsData).forEach(([title, data]) => {
        const ach = document.createElement('div');
        ach.className = `ach ${data.status ? 'ach_active' : 'ach_noactive'}`;
        
        ach.innerHTML = `
            <div class="ach-front">
                <img src="Img/ACHIVMENT/${data.img}.png" alt="${title}">
            </div>
            <div class="ach-back">
                <div class="ach-top">
                    <h3 class="ach-title">${title}</h3>
                </div>
                <div class="ach-bottom">
                    <p class="ach-desc">${data.description}<br>Баллы: ${data.point}</p>
                </div>
            </div>
        `;
        
        ach.addEventListener('click', (e) => {
            e.stopPropagation();
            document.querySelectorAll('.ach').forEach(item => {
                if (item !== ach) item.classList.remove('active');
            });
            ach.classList.toggle('active');
        });
        
        container.appendChild(ach);
    });

    // Закрытие при клике вне элемента
    document.addEventListener('click', () => {
        document.querySelectorAll('.ach').forEach(ach => {
            ach.classList.remove('active');
        });
    });
}

// Инициализация страницы
async function initPage() {
    initTelegramWebApp();
    await fetchData();
    
    document.getElementById('Name').textContent = `Привет, ${userData.name}!`;
    document.getElementById('Group').textContent = `Группа: ${userData.group}`;
    document.getElementById('Point').textContent = `Баллы: ${userData.points}`;
    
    createAchievements();
}

document.addEventListener('DOMContentLoaded', initPage);