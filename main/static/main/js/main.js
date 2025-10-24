document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.copy-promo').forEach(button => {
        button.addEventListener('click', function () {
            const promo = this.getAttribute('data-promo');
            if (navigator.clipboard) {
                navigator.clipboard.writeText(promo).then(() => {
                    alert('Промокод скопирован: ' + promo);
                }).catch(() => {
                    alert('Ошибка копирования');
                });
            } else {
                alert('Ваш браузер не поддерживает копирование');
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.add-to-cart-form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const url = form.getAttribute('action');
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            const button = form.querySelector('button');

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams(new FormData(form))
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if(button) {
                        const parent = button.parentElement;
                        parent.innerHTML = '<p class="added-to-cart-msg">Товар добавлен в корзину</p>';
                    }
                } else {
                    alert('Ошибка при добавлении товара');
                }
            })
            .catch(() => alert('Ошибка сети'));
        });
    });
});