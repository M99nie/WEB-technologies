const API_URL = 'http://127.0.0.1:5000/api';

// Элементы DOM
const carsContainer = document.getElementById('carsContainer');
const loadingElement = document.getElementById('loading');
const messageElement = document.getElementById('message');
const editModal = document.getElementById('editModal');


// 1. ПОЛУЧЕНИЕ ВСЕХ АВТОМОБИЛЕЙ (GET)
async function loadAllCars() {
    showLoading(true);
    clearMessage();

    try {
        const response = await fetch(`${API_URL}/cars`);

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        const cars = await response.json();
        displayCars(cars);
        showMessage(`Загружено ${cars.length} автомобилей`, 'success');

    } catch (error) {
        console.error('Ошибка при загрузке автомобилей:', error);
        showMessage(`Ошибка при загрузке: ${error.message}`, 'error');
        carsContainer.innerHTML = '<div class="error-message">Не удалось загрузить данные. Проверьте подключение к API.</div>';
    } finally {
        showLoading(false);
    }
}


// 2. ПОИСК ПО ID (GET)
async function searchCar() {
    const carId = document.getElementById('searchId').value.trim();

    if (!carId) {
        showMessage('Введите ID автомобиля для поиска', 'error');
        return;
    }

    showLoading(true);
    clearMessage();

    try {
        const response = await fetch(`${API_URL}/cars/${carId}`);

        if (response.status === 404) {
            throw new Error('Автомобиль с таким ID не найден');
        }

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        const car = await response.json();
        displayCars([car]);
        showMessage(`Найден автомобиль: ${car.firm} ${car.model}`, 'success');

    } catch (error) {
        console.error('Ошибка при поиске автомобиля:', error);
        showMessage(error.message, 'error');
        carsContainer.innerHTML = '';
    } finally {
        showLoading(false);
    }
}


// 3. ДОБАВЛЕНИЕ АВТОМОБИЛЯ (POST)
async function addNewCar() {
    const newCar = {
        firm: document.getElementById('newFirm').value.trim(),
        model: document.getElementById('newModel').value.trim(),
        year: parseInt(document.getElementById('newYear').value),
        power: parseInt(document.getElementById('newPower').value),
        color: document.getElementById('newColor').value.trim(),
        price: parseInt(document.getElementById('newPrice').value)
    };

    // Валидация
    if (!newCar.firm || !newCar.model || !newCar.year || !newCar.power || !newCar.color || !newCar.price) {
        showMessage('Заполните все поля!', 'error');
        return;
    }

    if (newCar.year < 1900 || newCar.year > 2024) {
        showMessage('Введите корректный год выпуска (1900-2024)', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch(`${API_URL}/cars`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newCar)
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        const result = await response.json();

        // Очищаем форму
        document.getElementById('newFirm').value = '';
        document.getElementById('newModel').value = '';
        document.getElementById('newYear').value = '';
        document.getElementById('newPower').value = '';
        document.getElementById('newColor').value = '';
        document.getElementById('newPrice').value = '';

        showMessage(`Автомобиль успешно добавлен! ID: ${result.id}`, 'success');

        // Перезагружаем список
        loadAllCars();

    } catch (error) {
        console.error('Ошибка при добавлении автомобиля:', error);
        showMessage(`Ошибка при добавлении: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

// 4. ОТКРЫТИЕ ОКНА РЕДАКТИРОВАНИЯ
function openEditModal(car) {
    document.getElementById('editId').value = car.id;
    document.getElementById('editFirm').value = car.firm;
    document.getElementById('editModel').value = car.model;
    document.getElementById('editYear').value = car.year;
    document.getElementById('editPower').value = car.power;
    document.getElementById('editColor').value = car.color;
    document.getElementById('editPrice').value = car.price;

    editModal.style.display = 'flex';
}

// 5. СОХРАНЕНИЕ ИЗМЕНЕНИЙ (PUT)=
async function saveCarChanges() {
    const carId = document.getElementById('editId').value;
    const updatedCar = {
        firm: document.getElementById('editFirm').value.trim(),
        model: document.getElementById('editModel').value.trim(),
        year: parseInt(document.getElementById('editYear').value),
        power: parseInt(document.getElementById('editPower').value),
        color: document.getElementById('editColor').value.trim(),
        price: parseInt(document.getElementById('editPrice').value)
    };

    // Валидация
    if (!updatedCar.firm || !updatedCar.model || !updatedCar.year || !updatedCar.power || !updatedCar.color || !updatedCar.price) {
        showMessage('Все поля должны быть заполнены!', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cars/${carId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedCar)
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        closeModal();
        showMessage(`Автомобиль успешно обновлен!`, 'success');

        // Перезагружаем список
        loadAllCars();

    } catch (error) {
        console.error('Ошибка при обновлении автомобиля:', error);
        showMessage(`Ошибка при обновлении: ${error.message}`, 'error');
    }
}

// 6. УДАЛЕНИЕ АВТОМОБИЛЯ (DELETE)
async function deleteCar(carId, carName) {
    if (!confirm(`Вы уверены, что хотите удалить автомобиль "${carName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cars/${carId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        showMessage(`Автомобиль "${carName}" успешно удален`, 'success');

        // Перезагружаем список
        loadAllCars();

    } catch (error) {
        console.error('Ошибка при удалении автомобиля:', error);
        showMessage(`Ошибка при удалении: ${error.message}`, 'error');
    }
}

// 7. ОТОБРАЖЕНИЕ АВТОМОБИЛЕЙ В HTML
function displayCars(cars) {
    if (!cars || cars.length === 0) {
        carsContainer.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666; font-size: 18px;">Автомобили не найдены</div>';
        return;
    }

    carsContainer.innerHTML = cars.map(car => `
        <div class="car-card" data-id="${car.id}">
            <div class="car-id">ID: ${car.id}</div>
            <div class="car-brand">${car.firm}</div>
            <div class="car-model">${car.model}</div>

            <div class="car-details">
                <div class="detail-row">
                    <span class="detail-label">Год выпуска:</span>
                    <span class="detail-value">${car.year}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Мощность:</span>
                    <span class="detail-value">${car.power} л.с.</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Цвет:</span>
                    <span class="detail-value">${car.color}</span>
                </div>
            </div>

            <div class="car-price">$${car.price.toLocaleString()}</div>

            <div class="car-actions">
                <button class="edit-btn" onclick="openEditModal(${JSON.stringify(car).replace(/"/g, '&quot;')})">
                    ✏️ Редактировать
                </button>
                <button class="delete-btn" onclick="deleteCar(${car.id}, '${car.firm} ${car.model}')">
                    🗑️ Удалить
                </button>
            </div>
        </div>
    `).join('');
}


function showLoading(show) {
    loadingElement.style.display = show ? 'block' : 'none';
    if (!show) {
        carsContainer.style.display = 'grid';
    } else {
        carsContainer.style.display = 'none';
    }
}

function showMessage(text, type) {
    messageElement.textContent = text;
    messageElement.className = `message ${type}`;
    messageElement.style.display = 'block';

    // Автоматически скрыть сообщение через 5 секунд
    if (type === 'success') {
        setTimeout(() => {
            messageElement.style.display = 'none';
        }, 5000);
    }
}

function clearMessage() {
    messageElement.style.display = 'none';
    messageElement.textContent = '';
}

function closeModal() {
    editModal.style.display = 'none';
}

// Закрытие модального окна по клику вне его
window.onclick = function(event) {
    if (event.target === editModal) {
        closeModal();
    }
}

// Закрытие по Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});


// 9. ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ СТРАНИЦЫ
document.addEventListener('DOMContentLoaded', function() {
    // Загружаем все автомобили при старте
    loadAllCars();

    // Добавляем обработчик отправки формы редактирования
    document.getElementById('editForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveCarChanges();
    });

    // Добавляем обработчик Enter в поле поиска
    document.getElementById('searchId').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchCar();
        }
    });
});