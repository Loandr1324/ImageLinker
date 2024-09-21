//const resetBtn = document.getElementById('cleare')

//resetBtn.addEventListener('click', function(){
//    document.getElementById("main-form").reset();
//
//    let forms = document.querySelectorAll('.main-form__item')
//    forms.forEach(function(item){
//        item.classList.remove('main-form__item--haserror')
//    })
//})

document.querySelectorAll('.main-form input, .main-form select').forEach(input => {
    input.addEventListener('focus', checkPreviousFields);
    input.addEventListener('change', checkPreviousFields);
    input.addEventListener('input', removeErrorOnInput); // Удаляем ошибку на вводе
});

// Добавляем обработчик для отправки формы
//document.querySelector('.main-form').addEventListener('submit', function(event) {
//    let allValid = true;  // Флаг, чтобы отслеживать, есть ли ошибки
//
//    // Проверяем все поля формы
//    document.querySelectorAll('.main-form input[required], .main-form select[required]').forEach(input => {
//        if (input.type === 'radio') {
//            // Если это radio, проверяем, выбрана ли хотя бы одна из группы
//            let radios = document.querySelectorAll(`input[name="${input.name}"]`);
//            let checked = Array.from(radios).some(radio => radio.checked);
//
//            if (!checked) {
//                let parent = input.closest('.main-form__item');
//                parent.classList.add('main-form__item--haserror');
//                allValid = false;  // Если ни одна радиокнопка не выбрана, запрещаем отправку
//            }
//        } else if (!input.value) {
//            // Для обычных input и select
//            let parent = input.closest('.main-form__item');
//            parent.classList.add('main-form__item--haserror');
//            allValid = false;  // Если нашли пустое поле, запрещаем отправку
//        }
//    });
//
//    // Если хотя бы одно поле не заполнено, предотвращаем отправку формы
//    if (!allValid) {
//        event.preventDefault();  // Останавливаем отправку формы
//    }
//});

// Функция для проверки предыдущих полей
function checkPreviousFields(event) {
    let prevElements = getPreviousRequiredFields(this);

    prevElements.forEach(element => {
        let parent = element.closest('.main-form__item');

        if (element.type === 'radio') {
            // Проверяем радиокнопки
            let radios = document.querySelectorAll(`input[name="${element.name}"]`);
            let checked = Array.from(radios).some(radio => radio.checked);

            if (!checked) {
                parent.classList.add('main-form__item--haserror');
            }
        } else if (!element.value) {
            parent.classList.add('main-form__item--haserror');
        }
    });
}

// Функция для удаления ошибки при вводе текста или изменении значения
function removeErrorOnInput(event) {
    let parent = this.closest('.main-form__item');

    if (this.type === 'radio') {
        let radios = document.querySelectorAll(`input[name="${this.name}"]`);
        let checked = Array.from(radios).some(radio => radio.checked);

        if (checked) {
            parent.classList.remove('main-form__item--haserror');
        }
    } else if (this.value) {
        parent.classList.remove('main-form__item--haserror');
    }
}

// Функция для получения всех предыдущих input и select с атрибутом required
function getPreviousRequiredFields(currentElement) {
    let allElements = Array.from(document.querySelectorAll('.main-form input[required], .main-form select[required]'));
    let index = allElements.indexOf(currentElement);

    // Возвращаем все элементы до текущего
    return allElements.slice(0, index);
}


/* NUMBER INPUT FILTER */
// Функция для форматирования числа с пробелами для тысяч и запятой для дробной части
function formatNumberInput(value) {
    // Удаляем все символы, кроме цифр, минуса и запятой
    value = value.replace(/[^0-9,-]/g, '');

    // Проверяем, есть ли запятая и обрабатываем целую и дробную части отдельно
    let parts = value.split(',');
    let integerPart = parts[0];
    let decimalPart = parts[1] ? ',' + parts[1] : '';

    // Форматируем целую часть с разделением пробелами каждые 3 цифры
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');

    // Возвращаем объединенное число
    return integerPart + decimalPart;
    
}

// Обработчик событий для всех инпутов с классом numberInput
document.querySelectorAll('.main-form__item--number input').forEach(function(input) {
    input.addEventListener('input', function() {

        // Форматируем текущее значение
        const formattedValue = formatNumberInput(this.value);

        // Обновляем значение поля инпута отформатированным числом
        this.value = formattedValue;
    });
});


