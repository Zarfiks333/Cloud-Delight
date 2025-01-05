document.addEventListener('DOMContentLoaded', function() {
    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
    
    removeFromCartButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const productId = button.getAttribute('data-product-id');
            console.log('Product ID to remove:', productId);  // Логируем передаваемый ID товара

            if (!productId) {
                console.error('Нет ID товара');
                return;
            }

            // Формируем правильный URL для удаления товара из корзины
            const url = `/cart/remove-from-cart/${productId}/`;

            fetch(url, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                if (data) {
                    console.log('Ответ от сервера:', data);
                    if (data.message) {
                        location.reload();  // Перезагружаем страницу, чтобы обновить корзину
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка при удалении товара из корзины:', error);
            });
        });
    });
});
