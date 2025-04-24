let achievements = {
  "Кормилец": {
      "description": "Принеси вкусняшки к чаю",
      "type": "Achivment",
      "img": "Food",
      "status": false,
      "point": 9
  },
  "Волонтер": {
      "description": "Стань волонтером кванториума",
      "type": "Achivment",
      "img": "GoodBoy",
      "status": true,
      "point": 25
  },
  "Денис": {
      "description": "Допрыгни до потолка",
      "type": "Achivment",
      "img": "Denis",
      "status": false,
      "point": -5
  },
  "Местный Жуков": {
      "description": "Хорошо покажи себя в роли тимлида",
      "type": "Achivment",
      "img": "teamlid",
      "status": true,
      "point": 25
  },
  "Эврика!": {
      "description": "Найди неожиданное и эффективное решение проблемы",
      "type": "Achivment",
      "img": "idea",
      "status": false,
      "point": 18
  },
  "Победитель": {
      "description": "Займи призовое место в не групповом соревновании",
      "type": "Test",
      "img": "Medal",
      "status": false,
      "point": 25
  },
  "Отличник": {
      "description": "Получи максимально возможную оценку за год",
      "type": "Test",
      "img": "Profy",
      "status": true,
      "point": 50
  },
  "Как?": {
      "description": "Получи максимально возможное количество баллов",
      "type": "Test",
      "img": "que",
      "status": false,
      "point": 0
  },
  "Превозмог": {
      "description": "Выйди со своим проектом на коллаборацию",
      "type": "Test",
      "img": "Star",
      "status": false,
      "point": 100
  },
  "Активный": {
      "description": "Сходи на мероприятие кванториума",
      "type": "Achivment",
      "img": "event",
      "status": true,
      "point": 12
  },
  "Командный игрок": {
      "description": "Прими активное участие в командной работе",
      "type": "Achivment",
      "img": "group",
      "status": true,
      "point": 12
  },
  "Это моё?": {
      "description": "Создай свой кейс или проект",
      "type": "Achivment",
      "img": "Hummer",
      "status": true,
      "point": 15
  },
  "Мастер": {
      "description": "Принеси настольную игру",
      "type": "Achivment",
      "img": "GameMaster",
      "status": false,
      "point": 9
  },
  "Оратор": {
      "description": "Покажи всем, как надо говорить на публике",
      "type": "Achivment",
      "img": "micro",
      "status": true,
      "point": 25
  }
}





const hexGrid = document.getElementById('hexGrid');

// Генерация угольников
for (const key in achievements) {
    const achivment = achievements[key];
    const li = document.createElement('li');
    li.className = 'hex';

    if (achivment.point != 0) {
      li.innerHTML = `
          <a class="hexIn">
              <img src="../img/achivment/${achivment.img}.png" alt="${key}">
              <h1 id="title">${key}</h1>
              <p id="description">${achivment.description}<br><b><small>Награда:<br>${achivment.point} б.</small><b></p>
          </a>
      `;} else {
        li.innerHTML = `
          <a class="hexIn">
              <img src="../img/achivment/${achivment.img}.png" alt="${key}">
              <h1 id="title">${key}</h1>
              <p id="description">${achivment.description}</p>
          </a>
      `;}

    const color = li.querySelector("*")
    if (achivment.status == true) {
      if (achivment.type == "Achivment") {
        color.style.backgroundColor = "#00FFC3";
      } else if (achivment.type == "Test") {
        color.style.backgroundColor = "#FF3333";
      }
    } else {
      color.style.backgroundColor = "gray";
    }
    hexGrid.appendChild(li);
}