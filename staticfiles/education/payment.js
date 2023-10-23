var stripe = Stripe('{{ STRIPE_PUBLIC_KEY }}');
var elements = stripe.elements();
var cardElement = elements.create('card');

cardElement.mount('#card-element');

var form = document.getElementById('payment-form');
var errorElement = document.getElementById('error-message');

form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
  }).then(function(result) {
    if (result.error) {
      // Обработка ошибок оплаты и отображаем сообщение об ошибке
      errorElement.textContent = result.error.message;
    } else {
      // Отправка информации о платеже на ваш сервер
      var amount = document.getElementById('amount').value;
      var csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value;

      fetch('/create_payment_view/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
          amount: amount,
          payment_method: result.paymentMethod.id,
        }),
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        // Получение client_secret из ответа сервера
        var clientSecret = data.client_secret;

        stripe.confirmCardPayment(clientSecret, {
          payment_method: result.paymentMethod.id,
        }).then(function(confirmResult) {
          console.log(confirmResult);  // Вывести ответ от сервера Stripe в консоль
          if (confirmResult.error) {
            // Обработка ошибок подтверждения платежа
            errorElement.textContent = confirmResult.error.message;
          } else if (confirmResult.paymentIntent.status === 'succeeded') {
            // Платеж успешно подтвержден
            window.location.href = '/success/'; // Перенаправление пользователя на страницу успеха
          } else {
            console.log('Статус платежа не "succeeded":', confirmResult.paymentIntent.status);
          }
        });
      })
      .catch(function(error) {
        console.error('Ошибка:', error);
      });
    }
  });
});

