$('#slider1, #slider2, #slider3,#slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function(){
    let id = $(this).attr('pid').toString();
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id : id
        },
        success:function(data){
            document.getElementById('quantity').innerText = data.quantity
            document.getElementById('total_amt').innerText = data.total_amt
            document.getElementById('amt').innerText = data.amt
        }
    })
})

$('.minus-cart').click(function(){
    let id = $(this).attr('pid').toString();
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById('quantity').innerText = data.quantity
            document.getElementById('total_amt').innerText = data.total_amt
            document.getElementById('amt').innerText = data.amt
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var elm = this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById('total_amt').innerText = data.total_amt
            document.getElementById('amt').innerText = data.amt
            elm.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})