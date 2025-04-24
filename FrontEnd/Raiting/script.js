let kvants_raiting = [{'id': 6, 'name': 'Никита ', 'surname': 'Иванов', 'group': 'C-IT-1', 'point': 198}, {'id': 2, 'name': 'Анна ', 'surname': 'Сидорова ', 'group': 'C-IT-1', 'point': 64}, {'id': 4, 'name': 'Ирина ', 'surname': 'Попова ', 'group': 'C-IT-3', 'point': 62}, {'id': 1, 'name': 'Александр', 'surname': 'Петров ', 'group': 'C-IT-2', 'point': 61}]

let groups_raiting = [{'id': 6, 'name': 'Никита ', 'surname': 'Иванов', 'point': 198}, {'id': 2, 'name': 'Анна ', 'surname': 'Сидорова ', 'point': 64}, {'id': 1, 'name': 'Александр', 'surname': 'Петров ', 'point': 50}, {'id': 5, 'name': 'Наталья ', 'surname': 'Кузнецова ', 'point': 45}, {'id': 7, 'name': 'Сергей ', 'surname': 'Попов ', 'point': 34}, {'id': 9, 'name': 'Анна ', 'surname': 'Романова ', 'point': 25}, {'id': 10, 'name': 'Мария ', 'surname': 'Соколова ', 'point': 17}, {'id': 11, 'name': 'Ольга ', 'surname': 'Васильева ', 'point': 15}, {'id': 12, 'name': 'Вика ', 'surname': 'Антонова ', 'point': 8}, {'id': 13, 'name': 'Никита ', 'surname': 'Рубцов ', 'point': 2}]





const groupContainer = document.getElementById('group');
const leadersContainer = document.getElementById('leaders').querySelector('#top');

// Заполнение студентов в группе
groups_raiting.forEach((student, index) => {
    index += 1
    const studentDiv = document.createElement('div');
    studentDiv.className = 'student';
    studentDiv.innerHTML = `
        <div class="rank"><div class="text">${index}</div></div>
        <div class="name"><div class="text">${student.surname} ${student.name}</div></div>
        <div class="score"><div class="text">${student.point} б.</div></div>
    `;
    groupContainer.appendChild(studentDiv);
});

// Заполнение лидеров
kvants_raiting.forEach((student, index) => {
    const studentDiv = document.createElement('div');
    studentDiv.className = 'student';
    studentDiv.id = index === 0 ? 'zero' : index === 1 ? 'first' : index === 2 ? 'second' : index === 3 ? 'third' : '';
    studentDiv.innerHTML = `
        <div class="rank"><div class="text">${student.point} б.</div></div>
        <div class="name"><div class="text">${student.surname} ${student.name}</div></div>
        <div class="score"><div class="text">${student.group}</div></div>
    `;
    leadersContainer.appendChild(studentDiv);
});