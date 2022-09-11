# booking-api
Booking API for Technical Test

/api/rooms/
Retorna todos los registros de habitaciones y permite el filtro mediante query string.
 - Se podría usar en una página de inicio y otra de habitaciones.

rooms/<int:pk>/
Retornará toda la información de una habitación en específico.
 - Puede usarse al construir la página de detalle de habitación.

rooms/<int:pk>/bookings/
Get. btiene todas las reservaciones realizadas en esa habitación.
 - Tiene la finalidad de usarse para restringir las fechas que el usuario pueda seleccionar en el FrontEnd.

bookings/
Get. Obtiene todas las reservaciones realizadas por el usuario (debe iniciar sesión).
 - Puede usarse para construir el perfil del usuario dentro de la página.
Post. Permite separar una habitación para pagarla posteriormente.

bookings/<int:pk>/
Get. Retorna los datos de una reservación en específico.
 - Luego de ingresar los datos de reservación, el usuario debe poder revisar el detalle antes de proceder con el pago.

bookings/pay/
Post. Crea un Pago
 - Se usará como webhook para esperar una respuesta por parte de la pasarela de pagos al finalizar el proceso de pago.
 - La reservación relacionada con el pago cambiará su status a pagado.