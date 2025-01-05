document.addEventListener('DOMContentLoaded', function () {
    const promoInput = document.getElementById('promo-input');
    const priceDisplay = document.getElementById('price');
    const promoForm = document.getElementById('promo-form'); // Получаем форму
    const productElement = document.getElementById('product');
    const discountedPrice = parseFloat(productElement.dataset.discountedPrice);
    const productCategorySlug = productElement.dataset.categorySlug;
    const productSlug = productElement.dataset.productSlug;

    // Проверяем, что элементы существуют
    if (!promoInput || !priceDisplay || !promoForm) {
        console.error('Не найдены необходимые элементы.');
        return;
    }

    // Начальная цена с учетом скидки, если есть
    let currentPrice = discountedPrice; // Цена с учетом скидки

    // Функция для обновления цены
    function updatePrice(newPrice) {
        // Проверяем, если новая цена целое число, выводим без десятичных
        priceDisplay.textContent = newPrice % 1 === 0 ? `${newPrice}₽` : `${newPrice.toFixed(2)}₽`;
    }

    function checkPromoCode(promoCode) {
        const url = `/product/category/${productCategorySlug}/${productSlug}/?promo_code=${promoCode}`;
    
        fetch(url, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Промокод недействителен.');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.promo_code_valid) {
                // Промокод валиден, обновляем цену
                if (data.discounted_price && !isNaN(data.discounted_price)) {
                    updatePrice(data.discounted_price);
                }
            } else {
                console.error("Ошибка: промокод недействителен.");
                resetPrice();
            }
        })
        .catch(error => {
            console.error('Ошибка при проверке промокода:', error);
            resetPrice();
        });
    }
    

    // Слушаем событие input на поле ввода промокода
    promoInput.addEventListener('input', function () {
        const promoCode = promoInput.value.trim(); // Получаем промокод из поля ввода
        if (promoCode.length > 0) {
            // Проверяем промокод только при наличии текста
            checkPromoCode(promoCode);
        } else {
            resetPrice(); // Если поле пустое, сбрасываем цену
        }
    });

    // Препятствуем отправке формы при нажатии Enter
    promoForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Предотвращаем отправку формы
    });

    // Функция для сброса цены
    function resetPrice() {
        // Восстанавливаем цену без изменений
        updatePrice(currentPrice);
    }

    // Устанавливаем начальную цену
    updatePrice(currentPrice);
});





document.addEventListener('DOMContentLoaded', function () {
    const buyButton = document.getElementById('buy-button');
    const promoInput = document.getElementById('promo-input');
    const productElement = document.getElementById('product');
    const productCategorySlug = productElement.dataset.categorySlug;
    const productSlug = productElement.dataset.productSlug;


    if (buyButton) {
        buyButton.addEventListener('click', function (event) {
            event.preventDefault();

            const promoCode = promoInput ? promoInput.value.trim() : "";

            fetch(`/product/buy/${productCategorySlug}/${productSlug}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken"), // Получаем CSRF-токен
                },
                body: JSON.stringify({ promo_code: promoCode }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        // Дополнительная логика после успешной покупки
                    } else {
                        alert("Произошла ошибка при покупке: " + data.message);
                    }
                })
                .catch(error => console.error("Ошибка при отправке запроса на покупку:", error));
        });
    }

    // Функция для получения CSRF-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";").map(c => c.trim());
            for (let cookie of cookies) {
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.split("=")[1]);
                    break;
                }
            }
        }
        return cookieValue;
    }
});





document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const productId = button.getAttribute('data-product-id');
            console.log('Product ID:', productId);  // Логируем передаваемый ID

            if (!productId) {
                console.error('Нет ID товара');
                return;
            }

            // Формируем правильный URL для корзины
            const url = `/cart/add-to-cart/${productId}/`;

            fetch(url, {
                method: 'GET',
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Ошибка сервера:', response.status);
                    return response.text();
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    alert(data.message);  // Покажем сообщение пользователю
                }
            })
            .catch(error => {
                console.error('Ошибка при добавлении товара в корзину:', error);
            });
        });
    });
});
