import os
import unittest

from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))


class OrderingTestCase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"

    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Falló el POST")
        p = Product.query.all()
        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")


    # Punto 1) a) No se pueda crear instancia de OrderProduct si quantity negativo
    def test_instance_of_OrderProduct_with_negative_quantity(self):
        # Inicio la Orden y cargo en la BD
        o = Order(id=1)
        db.session.add (o)

        # Inicio el Producto y cargo en la BD
        p = Product(id=1, name='Armario', price=800)
        db.session.add(p)

        #Inicio la Order del Producto y cargo en la BD
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=-1, product=p)
        db.session.add(orderProduct)

        db.session.commit()

        #Consulto todas las Ordenes de Producto
        ordp = OrderProduct.query.all()

        #Corroboro que se halla cargado la Orden con Cantidad Negativa
        self.assertEqual(len(ordp),1, "Se creo el prod con cantidad negativa")

    # Punto 1) b) Funcionamiento del GET
    def test_GET_function(self):
        # Inicio la Orden y cargo en la BD
        o = Order(id=1)
        db.session.add (o)

        # Inicio el Producto y cargo en la BD
        p = Product(id=1, name='Silla', price=200)
        db.session.add(p)

        #Inicio la Order del Producto y cargo en la BD
        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=8, product=p)
        db.session.add(orderProduct)

        db.session.commit()

        #Consulto la Orden
        respGET=self.client.get('/order/1/product/1')
        
        #Corroboro que se halla cargado la Orden
        self.assert200(respGET, "No existe la orden")

        #Consulto el producto
        data = Product.query.all()
        print(data)
        
        #Corroboro que se halla cargado el Producto
        self.assertEqual(len(data),1, "No se cargo el producto")


    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()

