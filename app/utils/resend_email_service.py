import resend
from app.core.config import settings

resend.api_key = settings.RESEND_API_KEY

async def send_order_ready_email(to_email: str, order: dict):
    
    html_content = f"""
    <h2>Your Order #{order['id']} is Ready!</h2>
    <p><strong>Shop:</strong> {order['shop_name']}</p>
    <p><strong>Total Amount:</strong> ₹{order['total_amount']}</p>

    <h3>Items:</h3>
    <ul>
        {''.join([
            f"<li>{i['name']} × {i['quantity']} — ₹{i['subtotal']}</li>"
            for i in order['items']
        ])}
    </ul>

    <p><strong>Delivery Address:</strong> {order['delivery_address']}</p>
    <p>Thank you for ordering!</p>
    """

    return resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": f"Your Order #{order['id']} is Ready",
        "html": html_content
    })


async def send_order_picked_email(to_email: str, order: dict):

    html_content = f"""
    <h2>Your Order #{order['id']} is Picked!</h2>
    <p><strong>Shop:</strong> {order['shop_name']}</p>
    <p><strong>Total Amount:</strong> ₹{order['total_amount']}</p>

    <h3>Items:</h3>
    <ul>
        {''.join([
            f"<li>{i['name']} × {i['quantity']} — ₹{i['subtotal']}</li>"
            for i in order['items']
        ])}
    </ul>

    <p><strong>Delivery Address:</strong> {order['delivery_address']}</p>
    <p>Thank you for Shoping with us!</p>
    """

    return resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": f"Your Order #{order['id']} is Picked",
        "html": html_content
    })

