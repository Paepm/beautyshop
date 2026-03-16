
SELECT *
FROM public.cart_cartproduct;

SELECT *
FROM public.shop_product;

SELECT *
FROM orders_order;

SELECT sp.name, sp.price_current, oi.quantity, oo.total_price
FROM public.orders_orderitem oi
INNER JOIN public.shop_product sp
ON oi.product_id = sp.id
INNER JOIN public.orders_order oo
ON oo.id = oi.order_id
WHERE oi.order_id = '177';

SELECT article_nr, name, stock
FROM public.shop_product
WHERE article_nr = 'ART-0011';

SELECT *
FROM public.auth_permission;

SELECT a.first_name, a.last_name, a.email, a.username, a.password
FROM public.accounts_customuser as a;

UPDATE public.accounts_customuser
SET email = 'deleted_datagrip@gmail.jokers'
WHERE username = 'test';

SELECT *
FROM public.shop_product
WHERE name = 'Folding Chair with Chromed Frame and Polycarbonate Seat';