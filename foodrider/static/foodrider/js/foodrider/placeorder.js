const order_total = JSON.parse(document.getElementById('order-total').textContent);
var form = document.getElementById('place-order')
form.addEventListener('submit', function(e){
    e.preventDefault()
    if (!order_total || order_total === '0') { 
        console.log('Please add items to cart!')
        alert("Please add some items to cart!");
        return false;
    }
    form.submit()
});
//     } else {
//         var userDataFrom = {
//             'fname': form.first_name.value,
//             'lname': form.last_name.value,
//             'email': form.email.value,
//             'phone': form.phone_number.value,
//             'address':form.street_address.value,
//             'paymentmethod': form.paymentmethods.value,
//             'total': order_total,
//         }
//         orderPlaced(userDataFrom)
//     }

// })


// function orderPlaced(userDataFrom) {
//     var url = '/order-placed/'
    
//     const request = new Request(
//         url,
//         {
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrftoken,
//             },
//         }
//     );

//     fetch (request, {
//         method: 'POST',
//         mode: 'same-origin',
//         body: JSON.stringify({
//             'formdata': userDataFrom,
//         }),
//     })
//     .then((response) => {
//         return response.json()
//     })
//     .then((data)=>{
//         // console.log(data['tid'])
//         cart = {}
//         document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
//         var confirm = 'order-confirmed/'
//         var tid = data['tid']
//         // console.log(home_url + confirm + tid)
//         location.href=home_url + confirm + tid
//     })
// }