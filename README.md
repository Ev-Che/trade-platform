<h1>Endpoints</h1>
<ul>
    <li>api/auth/users/ - (GET) get all users, (POST) create user.</li>
    <li>api/auth/jwt/create/ - (GET) get JWT token.</li>
    <br>
    <li>api/items/stocks/ - all CRUD with stocks</li>
    <li>api/items/stocks/id/ - (GET) retrieve stock with id</li>
    <br>
    <li>api/items/prices/ - all CRUD with prices</li>
    <li>api/items/prices/id/ - (GET) retrieve stock with id</li>
    <br>
    <li>api/items/currencies/ - all CRUD with prices</li>
    <li>api/items/currencies/id/ - (GET) retrieve stock with id</li>
    <br>
    <li>api/container/favorites/ - (GET) get user favorites</li>
    <li>api/container/favorites/ - (POST)<br>
data: {favorive_stock: stock_id}<br>
add stock with stock_id to user favorives</li>
    <li>api/container/favorites/id/ - (DELETE) delete favorite</li>
    <br>
    <li>api/container/inventory/ - (GET) get user inventory</li>
    <br>
    <li>api/offers/ - (GET) get all offers</li>
    <li>api/offers/ - (POST) data:{'stock': id, 'entry_quantity': quantity, 'order_type': 'S' or 'B', }<br>
get all offers</li>
    <br>
    <li>api/trades/ - (GET) get get trades for user where he is seller or buyer.</li>
</ul>
