let userId = 0;
const API_BASE_URL = 'http://localhost:8000';

// Данные для гостя 
const GuestGroupRatingData = [
  {'id': 4, 'name': 'Алексей ', 'surname': 'Романов ', 'points': 75}, 
  {'id': 7, 'name': 'Максим ', 'surname': 'Морозов ', 'points': 50}, 
  {'id': 2, 'name': 'Дмитрий ', 'surname': 'Кузнецов ', 'points': 25}, 
  {'id': 8, 'name': 'Ольга ', 'surname': 'Волкова ', 'points': 25}, 
  {'id': 1, 'name': 'Даниил', 'surname': 'Леонов', 'points': 0}, 
  {'id': 3, 'name': 'Мария ', 'surname': 'Романова ', 'points': 0},
  {'id': 5, 'name': 'Андрей ', 'surname': 'Сидоров ', 'points': 0}, 
  {'id': 6, 'name': 'Юрий ', 'surname': 'Петров ', 'points': 0}, 
  {'id': 9, 'name': 'Сергей ', 'surname': 'Соколов ', 'points': 0}, 
  {'id': 10, 'name': 'Татьяна ', 'surname': 'Иванова ', 'points': 0}
];
const GuestKvantRatingData = [
  {'student_id': 4, 'name': 'Алексей ', 'surname': 'Романов ', 'group': 'С-IT-1', 'points': 75}, 
  {'student_id': 12, 'name': 'Алексей ', 'surname': 'Сидоров ', 'group': 'C-IT-3', 'points': 75}, 
  {'student_id': 7, 'name': 'Максим ', 'surname': 'Морозов ', 'group': 'C-IT-1', 'points': 50}, 
  {'student_id': 11, 'name': 'Наталья ', 'surname': 'Кузнецова ', 'group': 'C-IT-2', 'points': 50}
];
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
        return {
            groupRating: GuestGroupRatingData,
            kvantRating: GuestKvantRatingData
        };
    }

    try {
        const [userRes, groupRes, kvantRes] = await Promise.all([
            fetch(`${API_BASE_URL}/get_student/${userId}`),
            fetch(`${API_BASE_URL}/get_group_raiting/${userId}`),
            fetch(`${API_BASE_URL}/get_kvant_raiting/${userId}`)
        ]);

        if (!userRes.ok || !groupRes.ok || !kvantRes.ok) {
            throw new Error('Ошибка HTTP запроса');
        }

        const [user, group, kvant] = await Promise.all([userRes.json(), groupRes.json(), kvantRes.json()]);

        if (user.status && group.status && kvant.status) {
            userData = {
                name: user.name,
                group: user.group,
                points: user.points
                };
            return {
            groupRating: group.group_rating,
            kvantRating: kvant.kvant_rating 
            };
        } else {
            userData = {
                name: "Гость",
                group: "C-IT-1",
                points: "0"
                };
            return {
            groupRating: GuestGroupRatingData,
            kvantRating: GuestKvantRatingData
            };
        }
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        return {
            groupRating: GuestGroupRatingData,
            kvantRating: GuestKvantRatingData
        };
    }
}

// Создание элемента студента
function createStudentElement(student, index, isLeader = false) {
    const studentDiv = document.createElement('div');
    studentDiv.className = 'student';

    const points = student.points ?? student.point ?? 0;
    const fullName = `${student.surname ?? ''} ${student.name ?? ''}`.trim();

    if (isLeader) {
        const topId = ['zero', 'first', 'second', 'third'][index] || '';
        studentDiv.innerHTML = `
            <div class="rank" id="${topId}"><div class="text">${points} б.</div></div>
            <div class="name"><div class="text">${fullName}</div></div>
            <div class="point"><div class="text">${student.group || ''}</div></div>
        `;
    } else {
        studentDiv.innerHTML = `
            <div class="rank"><div class="text">${index + 1}</div></div>
            <div class="name"><div class="text">${fullName}</div></div>
            <div class="point"><div class="text">${points} б.</div></div>
        `;
    }

    return studentDiv;
}

// Заполнение рейтингов
function renderRatings(data) {
    const groupContainer = document.getElementById('group-rating');
    const topContainer = document.getElementById('top');
    
    // Групповой рейтинг
    // groupContainer.innerHTML = '';
    data.groupRating.forEach((student, index) => {
        groupContainer.appendChild(createStudentElement(student, index));
    });

    // Топ лидеров
    if (topContainer) {
        // topContainer.innerHTML = '';
        const topStudents = [...data.kvantRating]
            .sort((a, b) => (b.points ?? b.point ?? 0) - (a.points ?? a.point ?? 0))
            .slice(0, 4);
            
        topStudents.forEach((student, index) => {
            topContainer.appendChild(createStudentElement(student, index, true));
        });
    }
}

// Инициализация страницы
async function initPage() {
    initTelegramWebApp();
    
    const ratingData = await fetchData();
    
    document.getElementById('Name').textContent = `Привет, ${userData.name}!`;
    document.getElementById('Group').textContent = `Группа: ${userData.group}`;
    document.getElementById('Point').textContent = `Баллы: ${userData.points}`;
    
    renderRatings(ratingData);
}

document.addEventListener('DOMContentLoaded', initPage);