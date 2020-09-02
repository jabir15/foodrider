$('body').on("click", '.update-cart.fa-minus', function(event) { 
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log(cart, productId)
    cart[productId]['quantity'] -= 1
    if (cart[productId]['quantity'] <= 0){
        console.log('Remove item',action, productId)
        delete cart[productId]
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    updateCartValue()
    $( "#cartsummary" ).load('/cart-summary/' + " .summary-table" );
});

var updateBtns = document.getElementsByClassName('update-cart fa-plus')
for (var i=0; i<updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var prevC = document.getElementsByClassName('amado-btn-minus')
        var prevR = prevC.length ? prevC[prevC.length-1].dataset.restaurant : document.getElementsByClassName('restaurant-name')[0].id 
        var restaurantId = this.dataset.restaurant
        var productId = this.dataset.product
        var action = this.dataset.action
        
        if (prevR === restaurantId) {
            console.log('Equal to equal to')
            addCookieItem(productId,action)
        }else {
            console.log('Not equal is running...')
            cart = {}
            addCookieItem(productId,action)
            prevC = document.getElementsByClassName('amado-btn-minus')
            prevR = prevC.length ? prevC[prevC.length-1].dataset.restaurant : document.getElementsByClassName('restaurant-name')[0].id 
        }
    });
}

function addCookieItem (productId, action){
    console.log('Not logged in.. Guest user!')
    if (action=='add'){
        if (cart[productId] == undefined) {
                cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }
    console.log('Cart:',cart)
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    updateCartValue()
    $( "#cartsummary" ).load('/cart-summary/' + " .summary-table" );
}
    
function updateCartValue(){
    var cartvalue = 0
    for (i=0; i<Object.values(cart).length; i++){
        cartvalue += Object.values(cart)[i]["quantity"]
    }
    document.getElementsByClassName('cart-basket')[0].innerText = cartvalue
}
