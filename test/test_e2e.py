import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class Ordering(unittest.TestCase):
    # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        # start the Flask server in a thread
        threading.Thread(target=self.app.run).start()

        # give the server a second to ensure it is up
        time.sleep(1)

        self.driver = webdriver.Chrome()

    #def test_title(self):
    #    driver = self.driver
    #    driver.get(self.baseURL)
    #    add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
    #    add_product_button.click()
    #    modal = driver.find_element_by_id('modal')
    #    assert modal.is_displayed(), "El modal no esta visible"

    # Punto 1) c) Verifica que el bug de cargar un producto con cantidad negativa fue corregido
    def test_solved_BUG_of_negative_quantity(self):
        # Inicio la Orden y cargo en la BD
        o = Order(id=1)
        db.session.add(o)

        # Inicio el Producto y cargo en la BD
        p = Product(id=1, name = 'Armario', price = 800)
        db.session.add(p)

        db.session.commit()

        #Abro el browser con la URL
        driver = self.driver
        driver.get(self.baseURL)
        
        #Clickeo en el boton para abrir el modal
        driver.find_element_by_xpath("/html/body/main/div[1]/div/button").click()
        
        #Asigno cantidad -5 al campo cantidad
        cant = driver.find_element_by_id("quantity")
        cant.clear()
        cant.send_keys('-5')

        #Selecciono el producto
        select_prod = driver.find_element_by_id('select-prod')
        select_prod.select_by_visible_text('Armario')

        #Corroboro que se cargo el producto con cantidad negativa
        guardar = driver.find_element_by_id("save-button")
        self.assertFalse(guardar.is_enabled(), "Se pudo ingresar un producto con cantidad negativa")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.driver.close()

if __name__ == "__main__":
    unittest.main()

