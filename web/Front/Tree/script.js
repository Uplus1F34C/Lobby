let userId = 0;
const API_BASE_URL = 'http://localhost:8000';

// Цвета для оценок
const MARK_COLORS = {
    3: '#4AB968', // зеленый
    2: '#E6F355', // желтый
    1: '#F35555', // красный
    0: '#D4D4D4', // серый
    default: '#D4D4D4'
};
function getRandomMark() {
    return Math.floor(Math.random() * 4); 
}
// Данные для гостя 
const GuestData = { 
    "1": {
        "title": "Введение в информационные технологии",
        "topics": {
            "1": {
                "title": "Экскурсия по технопарку. Техника безопасности",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Protect.png",
                "mark": getRandomMark(),
                "X": 1
            },
            "2": {
                "title": "Среда окружения, работа с файлами",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Windows.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "3": {
                "title": "Облачные сервисы: виды и функционал",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Cloud.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "4": {
                "title": "Создание презентации\"IT-Я\"",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Presentation.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "5": {
                "title": "Соревнование по киберспортивной Дисциплине",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Game.png",
                "mark": getRandomMark(),
                "X": 4
            }
        }
    },

    "2": {
        "title": "Програмирование на Python",
        "topics": { 
            "1": {
                "title": "Введение в программирование",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/python.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "2": {
                "title": "Числовые переменные, ввод и вывод данных",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/numbers.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "3": {
                "title": "Операции с данными",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/calc.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "4": {
                "title": "Условия",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/vetv.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "5": {
                "title": "Циклы",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/sicl.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "6": {
                "title": "Строковые переменные",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/text.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "7": {
                "title": "Списки",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/list.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "8": {
                "title": "Словари и множества",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/dict.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "9": {
                "title": "Функциональное программирование",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/func.png",
                "mark": getRandomMark(),
                "X": 5
            },
            "10": {
                "title": "Алгоритмическое соревнование",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/test.png",
                "mark": getRandomMark(),
                "X": 4
            },
            "11": {
                "title": "Работа с библиотеками",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/books.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "12": {
                "title": "Графика в python",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/videocard.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "13": {
                "title": "Соревнование \"Добро пожаловать в виртуальный мир\"",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/vr.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "14": {
                "title": "Кейс: \"Создание игры\"",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Game.png",
                "mark": getRandomMark(),
                "X": 5
            }
        }
    },
    "3": {
        "title": "Микроэлектроника",
        "topics": { 
            "1": {
                "title": "Электричество, закон Ома, электрические компоненты",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/electro.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "2": {
                "title": "Знакомство с Tinkercad",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/tinkercad.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "3": {
                "title": "Сборка электрической схемы на макетной плате",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/plata.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "4": {
                "title": "Микроконтроллеры, плата Arduino, Arduino IDE",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/uno.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "5": {
                "title": "Основы синтаксиса языка “Arduino Wiring“",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT//c++.png",
                "mark": getRandomMark(),
                "X": 4
            },
            "6": {
                "title": "Работа с последовательным портом",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/bin.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "7": {
                "title": "Построение логических схем",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/logic.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "8": {
                "title": "Цифровой сигнал",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/1.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "9": {
                "title": "Аналоговый сигнал",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/123.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "10": {
                "title": "Считывание аналогового значения",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/nbin.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "11": {
                "title": "Подключение сервоприводов",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/motor.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "12": {
                "title": "Подключение дисплея",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/screen.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "13": {
                "title": "Кейс: «Создание МФУ»",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/mfu.png",
                "mark": getRandomMark(),
                "X": 5
            }
        }
    },

    "4": {
        "title": "Веб-разработка",
        "topics": { 
            "1": {
            "title": "Введение в веб-разработку",
            "description": "Описание-Описание-Описание-Описание-Описание-Описание",
            "img": "S-IT/internet.png",
            "mark": getRandomMark(),
            "0": 0,
            "X": 1
            },
            "2": {
                "title": "Основные теги HTML",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/html.png",
                "mark": getRandomMark(),
                "0": 0,
                "X": 3
            },
            "3": {
                "title": "Теги, парные и одинарные",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/html_tags.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "4": {
                "title": "Атрибуты тегов",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/plus.png",
                "mark": getRandomMark(),
                "X": 2
            },
            "5": {
                "title": "Каскадная таблица стилей",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/css.png",
                "mark": getRandomMark(),
                "X": 4
            },
            "6": {
                "title": "Наследование стилей",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/alph.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "7": {
                "title": "Интеграция медиа ресурсов",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/video.png",
                "mark": getRandomMark(),
                "X": 3
            },
            "8": {
                "title": "Позиционирование элементов",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/marker.png",
                "mark": getRandomMark(),
                "X": 4
            },
            "9": {
                "title": "Кейс: «Создание сайта-визитки»",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/doc.png",
                "mark": getRandomMark(),
                "X": 5
            } 
        }
    }
};
let TopicsData = {};
let userData = { name: "Гость", group: "C-IT-1", points: "0" };

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
        TopicsData = GuestData;
        return;
    }

    try {
        const [topicsRes, userRes] = await Promise.all([
            fetch(`${API_BASE_URL}/get_marks/${userId}`),
            fetch(`${API_BASE_URL}/get_student/${userId}`)
        ]);

        if (!topicsRes.ok || !userRes.ok) {
            throw new Error('Ошибка HTTP запроса');
        }

        const [topics, user] = await Promise.all([topicsRes.json(), userRes.json()]);

        console.log(user)

        if (topics.status && user.status) {
            TopicsData = topics.topics || GuestData;
            userData = {
                name: user.name || "Гость",
                group: user.group || "C-IT-1",
                points: user.points || "0"
            } 
        } else {
            TopicsData = GuestData
            userData = {
                name: "Гость",
                group: "C-IT-1",
                points: "0"
            }
        };
        // }
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        TopicsData = GuestData;
    }
}

// Подсветка выбранной темы
function highlightSelectedTopic(selectedBtn) {
    document.querySelectorAll('#Topic-container button').forEach(btn => {
        btn.style.border = btn === selectedBtn 
            ? '3px solid rgb(0, 82, 97)' 
            : '1px solid #000000';
    });
}

// Отображение информации о теме
function showTopicInfo(topic, topicBtn) {
    const infoBlock = document.getElementById('info');
    if (!infoBlock) return;

    // Заполнение данных
    document.getElementById('title').textContent = topic.title;
    document.getElementById('description').textContent = topic.description;
    document.getElementById('points').textContent = `${topic.mark * topic.X}/${topic.X * 3}`;
    
    const markElement = document.getElementById('mark');
    markElement.textContent = topic.mark;
    markElement.style.backgroundColor = MARK_COLORS[topic.mark] || MARK_COLORS.default;

    // Позиционирование блока информации
    infoBlock.style.display = 'block';
    
    if (window.innerWidth > 500) {
        // Десктопная версия - фиксированное положение слева внизу
        infoBlock.style.position = 'fixed';
        infoBlock.style.left = '5px';
        infoBlock.style.bottom = '85px';
        infoBlock.style.width = '300px';
        infoBlock.style.borderRadius = '20px';
    } else {
        // Мобильная версия - прикреплено сверху
        infoBlock.style.position = 'fixed';
        infoBlock.style.top = window.innerWidth > 350 ? '80px' : '65px';
        infoBlock.style.left = '0';
        infoBlock.style.right = '0';
        infoBlock.style.width = '100%';
        infoBlock.style.borderRadius = '0 0 20px 20px';
    }

    highlightSelectedTopic(topicBtn);
}

// Создание кнопок тем
function createTopicButtons() {
    const container = document.getElementById('Topic-container');
    container.innerHTML = '';

    Object.entries(TopicsData).forEach(([branchId, branch]) => {
        const branchBlock = document.createElement('div');
        branchBlock.className = 'branch-block';
        branchBlock.style.margin = "0px 10px"
        
        // Заголовок ветки с центрированием
        const branchTitle = document.createElement('h2');
        branchTitle.textContent = branch.title;
        branchTitle.style.textAlign = 'center';
        branchTitle.style.margin = '15px 0';
        branchTitle.style.fontFamily = 'Comic Relief';
        branchTitle.style.fontSize = '20px';
        branchBlock.appendChild(branchTitle);

        const topicsContainer = document.createElement('div');
        topicsContainer.className = 'topics-container';
        topicsContainer.style.display = 'flex';
        topicsContainer.style.flexWrap = 'wrap';
        topicsContainer.style.justifyContent = 'center';
        topicsContainer.style.gap = '10px';

        Object.entries(branch.topics).forEach(([topicId, topic]) => {
            const topicBtn = document.createElement('button');
            topicBtn.style.backgroundColor = MARK_COLORS[topic.mark] || MARK_COLORS.default;
            topicBtn.style.border = '1px solid #000000';
            topicBtn.style.borderRadius = '5px';
            topicBtn.style.padding = '5px';
            topicBtn.style.cursor = 'pointer';
            
            if (topic.img) {
                const img = document.createElement('img');
                img.src = `Img/TOPIC/${topic.img}`;
                img.style.width = '50px';
                img.style.height = '50px';
                img.style.objectFit = 'contain';
                topicBtn.appendChild(img);
            }

            topicBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                showTopicInfo(topic, topicBtn);
            });

            topicsContainer.appendChild(topicBtn);
        });

        branchBlock.appendChild(topicsContainer);
        container.appendChild(branchBlock);
    });

    // Закрытие блока информации при клике вне его
    document.addEventListener('click', (e) => {
        if (!e.target.closest('button') && !e.target.closest('#info')) {
            const infoBlock = document.getElementById('info');
            if (infoBlock) infoBlock.style.display = 'none';
            highlightSelectedTopic(null);
        }
    });
}

// Инициализация страницы
async function initPage() {
    initTelegramWebApp();
    await fetchData();
    
    document.getElementById('Name').textContent = `Привет, ${userData.name}!`;
    document.getElementById('Group').textContent = `Группа: ${userData.group}`;
    document.getElementById('Point').textContent = `Баллы: ${userData.points}`;
    
    createTopicButtons();
}

document.addEventListener('DOMContentLoaded', initPage);
