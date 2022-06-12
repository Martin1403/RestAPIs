import uuid
from datetime import datetime
from uuid import UUID

from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from starlette import status
from starlette.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates


from orders import app
from orders.api.schemas import GetOrderSchema, CreateOrderSchema, GetOrdersSchema
from orders.api.models import order_dal

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def redirect():
    response = RedirectResponse(url='/docs')
    return response

'''
@app.get("/")
def home_page(request: Request):
    """
        Home.
    Rendering Home page.
    """
    return templates.TemplateResponse(
        "index.html", {"request": request})
'''


@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    """
        Get orders.
    The function returns all orders.
    """
    with order_dal() as od:
        all_orders = od.get_orders()
    return {'orders': all_orders}


@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)  # noqa: E501
def create_order(order_details: CreateOrderSchema):
    """
        Create order.
    The function creates a new order. [ small |medium | big]
    """
    order = order_details.dict()
    data = order.get("order").pop()
    product, size, quantity = data.get('product'), data.get('size'), data.get('quantity')
    with order_dal() as od:
        new_order = od.create_order(product=product, size=size.value, quantity=quantity)
    return new_order.json()


@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    """
        Get order by id.
    The function returns order by id.
    """
    with order_dal() as od:
        order = od.get_order(str(order_id))
    if order:
        return order.json()
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    """
        Update order.
    The function updates order by id. [ small |medium | big]
    """
    order = order_details.dict()
    data = order.get("order").pop()
    product, size, quantity = data.get('product'), data.get('size'), data.get('quantity')
    with order_dal() as od:
        order = od.update_order(
            order_id=str(order_id),
            product=product,
            size=size,
            quantity=quantity,
        )
    if order:
        return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_order(order_id: UUID):
    """
        Delete order.
    The function deletes order by id.
    """
    with order_dal() as od:
        order = od.delete_order(order_id=str(order_id))
        if order:
            return
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    """
            Cancel order.
        The function update status to cancel.
        """
    with order_dal() as od:
        order = od.cancel_order(order_id=str(order_id))
        if order:
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    """
            Pay order.
        The function updates status to progress.
        """
    with order_dal() as od:
        order = od.pay_order(order_id=str(order_id))
        if order:
            return order
    raise HTTPException(
        status_code=404, detail=f'Order with ID {order_id} not found'
    )
