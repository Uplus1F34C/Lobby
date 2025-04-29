const kvants_raiting = [{'id': 6, 'name': 'Никита ', 'surname': 'Иванов', 'group': 'C-IT-1', 'point': 198}, {'id': 2, 'name': 'Анна ', 'surname': 'Сидорова ', 'group': 'C-IT-1', 'point': 64}, {'id': 4, 'name': 'Ирина ', 'surname': 'Попова ', 'group': 'C-IT-3', 'point': 62}, {'id': 1, 'name': 'Александр', 'surname': 'Петров ', 'group': 'C-IT-2', 'point': 61}]

const groups_raiting = [{'id': 6, 'name': 'Никита ', 'surname': 'Иванов', 'point': 198}, {'id': 2, 'name': 'Анна ', 'surname': 'Сидорова ', 'point': 64}, {'id': 1, 'name': 'Александр', 'surname': 'Петров ', 'point': 50}, {'id': 5, 'name': 'Наталья ', 'surname': 'Кузнецова ', 'point': 45}, {'id': 7, 'name': 'Сергей ', 'surname': 'Попов ', 'point': 34}, {'id': 9, 'name': 'Анна ', 'surname': 'Романова ', 'point': 25}, {'id': 10, 'name': 'Мария ', 'surname': 'Соколова ', 'point': 17}, {'id': 11, 'name': 'Ольга ', 'surname': 'Васильева ', 'point': 15}, {'id': 12, 'name': 'Вика ', 'surname': 'Антонова ', 'point': 8}, {'id': 13, 'name': 'Никита ', 'surname': 'Рубцов ', 'point': 2}]

  
// Получаем контейнеры для вставки данных
const groupContainer = document.getElementById('group');
const leadersContainer = document.getElementById('leaders').querySelector('#top');

function createStudentElement(student, index, isLeader = false) {
const studentDiv = document.createElement('div');
studentDiv.className = 'student';

// Добавляем спец. классы для первых мест в рейтинге лидеров
if (isLeader) {
    studentDiv.id = ['zero', 'first', 'second', 'third'][index] || '';
}

studentDiv.innerHTML = isLeader
    ? `
    <div class="rank"><div class="text">${student.point} б.</div></div>
    <div class="name"><div class="text">${student.surname} ${student.name}</div></div>
    <div class="score"><div class="text">${student.group}</div></div>
    `
    : `
    <div class="rank"><div class="text">${index}</div></div>
    <div class="name"><div class="text">${student.surname} ${student.name}</div></div>
    <div class="score"><div class="text">${student.point} б.</div></div>
    `;

return studentDiv;
}

// Заполняем рейтинг группы
groups_raiting.forEach((student, index) => {
groupContainer.appendChild(createStudentElement(student, index + 1));
});

// Заполняем топ лидеров
kvants_raiting.forEach((student, index) => {
leadersContainer.appendChild(createStudentElement(student, index, true));
});