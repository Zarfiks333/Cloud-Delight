document.addEventListener("DOMContentLoaded", () => {
    // Находим все блоки с товаром и кнопки прокрутки
    const productWrappers = document.querySelectorAll('.container');

    productWrappers.forEach((wrapper) => {
        const services = wrapper.querySelector('.services, .product');
        const leftArrow = wrapper.querySelector('.left-arrow');
        const rightArrow = wrapper.querySelector('.right-arrow');
        
        if (!services || !leftArrow || !rightArrow) return;

        const cardWidth = 255 + 40; // ширина карточки + gap
        let currentPosition = 0;
        
        // Получаем максимальную позицию для прокрутки
        const totalWidth = services.scrollWidth;
        const containerWidth = services.parentElement.offsetWidth;
        const maxPosition = -(totalWidth - containerWidth);

        // Прокрутка влево
        leftArrow.addEventListener("click", () => {
            if (currentPosition < 0) {
                currentPosition += cardWidth;
                services.style.transform = `translateX(${currentPosition}px)`;
            }
        });

        // Прокрутка вправо
        rightArrow.addEventListener("click", () => {
            if (currentPosition > maxPosition) {
                currentPosition -= cardWidth;
                services.style.transform = `translateX(${currentPosition}px)`;
            }
        });
    });
});



















document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const mainContent = document.querySelector('main'); // Основной контент страницы
    const originalUrl = window.location.href; // Сохраняем текущий URL

    // Сохраняем оригинальный HTML контент для восстановления
    const originalMainContent = mainContent.innerHTML;

    if (searchInput) {
        // Отменяем отправку формы при нажатии Enter
        searchInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Отменяем действие по умолчанию (отправка формы)
            }
        });

        searchInput.addEventListener('input', function () {
            const query = searchInput.value.trim();
            
            // Если поле поиска пустое
            if (!query) {
                // Восстанавливаем оригинальный контент
                mainContent.innerHTML = originalMainContent;
                searchResults.innerHTML = ''; // Очищаем блок с результатами поиска

                // Возвращаем старый URL, без query параметра
                window.history.replaceState({}, '', originalUrl);
                return;
            }

            // Меняем URL на страницу поиска, но не перезагружаем страницу
            window.history.pushState({}, '', '/search/?q=' + encodeURIComponent(query));

            // Удаляем весь основной контент страницы
            mainContent.innerHTML = '';

            // Выполняем AJAX-запрос для поиска
            fetch('/search/?q=' + encodeURIComponent(query), {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Если пришли результаты, вставляем их в контейнер
                if (data.results_html) {
                    searchResults.innerHTML = data.results_html;
                } else {
                    searchResults.innerHTML = '<p>Ничего не найдено.</p>';
                }
            })
            .catch(error => console.log('Ошибка поиска:', error));
        });
    }
});
