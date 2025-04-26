if (window.Telegram && window.Telegram.WebApp) {
    const tgWebApp = window.Telegram.WebApp;
    
    // Получаем ID пользователя
    const userId = tgWebApp.initDataUnsafe.user?.id;
    
    if (userId) {
        alert("Все данные initDataUnsafe:", Telegram.WebApp.initDataUnsafe);
        // Можно отправить этот ID на сервер или использовать в боте
    } else {
        alert("User ID не доступен (пользователь не авторизован)");
    }
} else {
    alert("Telegram WebApp API не загружен");
}





let data = { 
    "1": {
        "title": "Введение в информационные технологии",
        "topics": {
            "1": {
                "title": "Экскурсия по технопарку. Техника безопасности",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Protect.png",
                "mark": 1,
                "0": 0,
                "1" : 1,
                "2" : 2,
                "3" : 3
            },
            "2": {
                "title": "Среда окружения, работа с файлами",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Windows.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "3": {
                "title": "Облачные сервисы: виды и функционал",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Cloud.png",
                "mark": 3,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "4": {
                "title": "Создание презентации\"IT-Я\"",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Presentation.png",
                "mark": 3,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "5": {
                "title": "Соревнование по киберспортивной Дисциплине",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Game.png",
                "mark": 2,
                "0": 0,
                "1" : 4,
                "2" : 8,
                "3" : 12
            }
        }
    },

    "2": {
        "title": "Програмированеи на Python",
        "topics": { 
            "1": {
                "title": "Введение в программирование",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/python.png",
                "mark": 2,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "2": {
                "title": "Числовые переменные, ввод и вывод данных",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/numbers.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "3": {
                "title": "Операции с данными",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/calc.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "4": {
                "title": "Условия",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/vetv.png",
                "mark": 1,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "5": {
                "title": "Циклы",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/sicl.png",
                "mark": 1,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "6": {
                "title": "Строковые переменные",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/text.png",
                "mark": 2,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "7": {
                "title": "Списки",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/list.png",
                "mark": 3,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "8": {
                "title": "Словари и множества",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/dict.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "9": {
                "title": "Функциональное программирование",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/func.png",
                "mark": 3,
                "0": 0,
                "1" : 5,
                "2" : 10,
                "3" : 15
            },
            "10": {
                "title": "Алгоритмическое соревнование",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/test.png",
                "mark": 3,
                "0": 0,
                "1" : 4,
                "2" : 8,
                "3" : 12
            },
            "11": {
                "title": "Работа с библиотеками",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/books.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "12": {
                "title": "Графика в python",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/videocard.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "13": {
                "title": "Соревнование \"Добро пожаловать в виртуальный мир\"",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/vr.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "14": {
                "title": "Кейс: \"Создание игры\"",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/Game.png",
                "mark": 3,
                "0": 0,
                "1" : 5,
                "2" : 10,
                "3" : 15
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
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "2": {
                "title": "Знакомство с Tinkercad",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/tinkercad.png",
                "mark": 1,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "3": {
                "title": "Сборка электрической схемы на макетной плате",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/plata.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "4": {
                "title": "Микроконтроллеры, плата Arduino, Arduino IDE",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/uno.png",
                "mark": 2,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "5": {
                "title": "Основы синтаксиса языка “Arduino Wiring“",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT//c++.png",
                "mark": 1,
                "0": 0,
                "1" : 4,
                "2" : 8,
                "3" : 12
            },
            "6": {
                "title": "Работа с последовательным портом",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/bin.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "7": {
                "title": "Построение логических схем",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/logic.png",
                "mark": 3,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "8": {
                "title": "Цифровой сигнал",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/1.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "9": {
                "title": "Аналоговый сигнал",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/123.png",
                "mark": 3,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "10": {
                "title": "Считывание аналогового значения",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/nbin.png",
                "mark": 2,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "11": {
                "title": "Подключение сервоприводов",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/motor.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "12": {
                "title": "Подключение дисплея",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/screen.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "13": {
                "title": "Кейс: «Создание МФУ»",
                "description": "Описание-Описание-Описание-Описание-Описание-Описание",
                "img": "S-IT/mfu.png",
                "mark": 3,
                "0": 0,
                "1" : 5,
                "2" : 10,
                "3" : 15
            }
        }
    },

    "4": {
        "title": "Веб-разработка",
        "topics": { 
            "1": {
            "title": "Введение в веб-разработку",
            "description": "Основы веб разработки",
            "img": "S-IT/internet.png",
            "mark": 1,
            "0": 0,
            "1" : 1,
            "2" : 2,
            "3" : 3
            },
            "2": {
                "title": "Основные теги HTML",
                "description": "Изучение основных тегов языка гипертекстовой разметки",
                "img": "S-IT/html.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "3": {
                "title": "Теги, парные и одинарные",
                "description": "Варианты тегов с различным функционалом",
                "img": "S-IT/html_tags.png",
                "mark": 2,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "4": {
                "title": "Атрибуты тегов",
                "description": "Расширенная настройка тегов",
                "img": "S-IT/plus.png",
                "mark": 3,
                "0": 0,
                "1" : 2,
                "2" : 4,
                "3" : 6
            },
            "5": {
                "title": "Каскадная таблица стилей",
                "description": "Изучение CSS, основных атрибутов и синтаксиса",
                "img": "S-IT/css.png",
                "mark": 3,
                "0": 0,
                "1" : 4,
                "2" : 8,
                "3" : 12
            },
            "6": {
                "title": "Наследование стилей",
                "description": "Возможность настраивать большое количество элементво через наследования",
                "img": "S-IT/alph.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "7": {
                "title": "Интеграция медиа ресурсов",
                "description": "Добавленеи видео, картинок и т.п. на сайт",
                "img": "S-IT/video.png",
                "mark": 3,
                "0": 0,
                "1" : 3,
                "2" : 6,
                "3" : 9
            },
            "8": {
                "title": "Позиционирование элементов",
                "description": "Расположение элементов на странице по расписанным правилам",
                "img": "S-IT/marker.png",
                "mark": 1,
                "0": 0,
                "1" : 4,
                "2" : 8,
                "3" : 12
            },
            "9": {
                "title": "Кейс: «Создание сайта-визитки»",
                "description": "Проверь свои способности в создании сайта-визитки",
                "img": "S-IT/doc.png",
                "mark": 3,
                "0": 0,
                "1" : 5,
                "2" : 10,
                "3" : 15
            } 
        }
    }
}
const container = document.getElementById('flex-container');


const branches = Object.keys(data); // Получаем количество веток в JSON

// Создаем блоки на основе веток
branches.forEach((branch, index) => {
    const block = document.createElement('div');
    block.textContent = data[branch].title; // Текст блока из title
    block.style.textAlign = 'center'; // Выравнивание текста по центру
    
    // Создаем контейнер для тем
    const topicsContainer = document.createElement('div');
    
    // Получаем темы для текущей ветки
    const topics = Object.keys(data[branch].topics);

    topics.forEach(topic => {
        const topicBlock = document.createElement('button');

        const topicData = data[branch].topics[topic];
        let mark_js = String(topicData.mark);

        if (mark_js == 3) {
            topicBlock.style.backgroundColor = '#4AB968';
        } else if (mark_js == 2) {
            topicBlock.style.backgroundColor = '#E6F355';
        }
        else if (mark_js == 1) {
            topicBlock.style.backgroundColor = '#F35555';
        } else {
            topicBlock.style.backgroundColor = '#D4D4D4';
        }

        // Добавляем изображение, если оно есть
        if (data[branch].topics[topic].img) {
            const img = document.createElement('img');
            img.src = "../img/Topics/" + data[branch].topics[topic].img; // Путь к изображению
            console.log(img.src)
            topicBlock.appendChild(img); // Добавляем изображение в кнопку
        }

        // Добавляем обработчик события для отображения информации
        topicBlock.addEventListener('click', (event) => {
            document.getElementById('info').style.display = 'block'; // Показываем блок информации

            document.getElementById('title').textContent = topicData.title;
            document.getElementById('description').textContent = topicData.description;
            document.getElementById('points').textContent = `${topicData[mark_js]}/${topicData["3"]}`; // Пример, как можно отобразить баллы

            if (mark_js == 3) {
                document.getElementById('mark').style.backgroundColor = '#4AB968';
            } else if (mark_js == 2) {
                document.getElementById('mark').style.backgroundColor = '#E6F355';
            } else if (mark_js == 1) {
                document.getElementById('mark').style.backgroundColor = '#F35555';
            } else {
                document.getElementById('mark').style.backgroundColor = '#D4D4D4';
            }

            document.getElementById('mark').textContent = mark_js; // Отображаем оценку

            // Позиционируем блок информации рядом с кнопкой
            const rect = event.target.getBoundingClientRect(); // Получаем размеры кнопки
            const infoBlock = document.getElementById('info');
            const style = infoBlock.style
            if (window.innerWidth > 700) {
                
                style.top = `${rect.top + window.scrollY}px`; // Устанавливаем позицию по Y

                style.position = "absolute";
                style.width = "300px";
                style.height = "auto";
                style.borderRadius = "20px"

                if (rect.x + 400 > window.innerWidth) {
                    style.left = `${rect.left - 300 - 50}px`;
                } else {
                    style.left = `${rect.left + 100}px`; // Устанавливаем позицию по X на левую границу кнопки
                }

            } else {
                style.left = `0px`; // Устанавливаем позицию по X на левую границу кнопки
                style.bottom = `0px`;

                style.position = "fixed";
                style.width = "100%";
                
                style.borderRadius = "20px"
                style.borderBottomLeftRadius = "0px";
                style.borderBottomRightRadius = "0px";
                style.height = "auto";
            }
    
            // Сбрасываем стиль всех кнопок тем
            const allTopicBlocks = document.querySelectorAll('#flex-container button');
            allTopicBlocks.forEach(block => {
                block.style.border = '1px solid #000000'; // Сбрасываем границу
            });

            // Увеличиваем границу и меняем цвет текущей кнопки 
            topicBlock.style.border = '3px solid rgb(0, 82, 97)'; // Увеличиваем границу
        });

        topicsContainer.appendChild(topicBlock); // Добавляем квадратик в контейнер тем
        });

    block.appendChild(topicsContainer); // Добавляем контейнер тем в блок
    container.appendChild(block); // Добавляем блок в контейнер
});

// Обработчик события для скрытия блока информации при клике на пустую область
document.addEventListener('click', (event) => {
    const infoBlock = document.getElementById('info');
    if (!infoBlock.contains(event.target) && !event.target.closest('button')) {
        infoBlock.style.display = 'none'; // Скрываем блок информации

        // Сбрасываем стиль всех кнопок тем
        const allTopicBlocks = document.querySelectorAll('#flex-container button');
        allTopicBlocks.forEach(block => {
            block.style.border = '1px solid #000000'; // Сбрасываем границу
        });
    }
});
