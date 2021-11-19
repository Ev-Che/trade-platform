<h1>Endpoints</h1>
<ul>
    <li>/auth/users/ - (GET) get all users, (POST) create user.</li>
    <li>/auth/jwt/create/ - (GET) get JWT token.</li>
    <br>
    <li>/stocks/ - all CRUD with stocks</li>
    <li>/stocks/id/ - (GET) retrieve stock with id</li>
    <br>
    <li>/prices/ - all CRUD with prices</li>
    <li>/prices/id/ - (GET) retrieve stock with id</li>
    <br>
    <li>/currencies/ - all CRUD with prices</li>
    <li>/currencies/id/ - (GET) retrieve stock with id</li>
    <br>
    <li>/favorites/ - (GET) get user favorites</li>
    <li>/favorites/ - (POST)<br>
data: {user: user_id, favorive_stock: stock_id}<br>
add stock with stock_id to user favorives</li>
    <li>/favorites/id/ - (DELETE) delete favorite</li>
    <br>
    <li>/inventory/ - (GET) get user inventory</li>
    <br>
    <li>/offers/ - (GET) get all offers</li>
    <li>/offers/ - (POST) data:{'stock': id, 'entry_quantity': quantity, 'order_type': 'S' or 'B', }<br>
get all offers</li>
</ul>
