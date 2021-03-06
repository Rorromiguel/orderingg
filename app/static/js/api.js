(function () {
    /**
     * Obtiene una orden desde el backend
     *
     * @param {Number} orderId id de la orden
     */
    function getOrder(orderId) {
        return fetch(`/order/${ orderId }`)
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos desde el backend
     *
     */
    function getProducts() {
        return fetch("/product")
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Obtiene todos los productos pertenecientes a una orden desde el backend
     *
     */
    function getOrderProduct(orderId, productId) {
        return fetch(`/order/${ orderId }/product/${ productId }`)
            .then(function toJson(r) {
                return r.json();
            });
    }

    /**
     * Edita un producto de una orden
     *
     */
    function editProduct(orderId, productId, quantity) {
        const data = JSON.stringify({ quantity: quantity});

        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                method: "PUT",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    /**function deleteProduct(orderId, productId) {
        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                method: "DELETE",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }**/

    /**
     * Agrega un producto a una orden
     **/
    function addProduct(orderId, product, quantity) {
        const data = JSON.stringify({ quantity: quantity, product: product });

        return fetch(`/order/${ orderId }/product`,
            {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }


    /**
     * Borra un producto a una orden
     **/

    function deleteProduct(orderId, productId) {
        const data = JSON.stringify({ product: productId });

        return fetch(`/order/${ orderId }/product/${ productId }`,
            {
                method: "DELETE",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: data
            }
        ).then(function toJson(r) {
            return r.json();
        });
    }

    return {
        getOrder,
        getProducts,
        getOrderProduct,
        editProduct,
        deleteProduct,
        addProduct
    };
})();
