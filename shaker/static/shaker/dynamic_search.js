document.addEventListener('DOMContentLoaded', function() {


    let search_bar = document.querySelector('#search_bar')
    let category_selector = document.querySelector("#select_category")
    var typed = search_bar.value
    var category = 'All drinks'

    // Searching by name
    search_bar.addEventListener('keyup', function() {
        typed = search_bar.value
        if (typed === '' && category === 'All drinks') {
            document.querySelector('#list_of_cards').style.display = 'block'
            document.querySelector('#dynamic_search').style.display = 'none'
        } else {
            document.querySelector('#dynamic_search').style.display = 'block'
            document.querySelector('#list_of_cards').style.display = 'none'
            // console.log(typed)
            get_drinks(typed, category)
        }
    } )


    // Searching by category
    category_selector.addEventListener('change', function() {

        category = this.value
        if (category === 'All drinks' && typed === '') {
            document.querySelector('#list_of_cards').style.display = 'block'
            document.querySelector('#dynamic_search').style.display = 'none'
        } else {
            document.querySelector('#dynamic_search').style.display = 'block'
            document.querySelector('#list_of_cards').style.display = 'none'
            // console.log(category)
            get_by_category(category, typed)
        }
    })
})



function get_drinks(typed, category) {

    let new_drinks_set = ''

    fetch('api/drinks/all')
    .then(response => response.json())
    .then(drinks => {

        if (category === 'All drinks') {
            drinks.forEach(drink => {
                // check matches case-insensitively
                if (drink.name.toLowerCase().includes(typed.toLowerCase())) {   
                    // add another drink card to the set
                    new_drinks_set += create_drink_card(drink)
                }
            })
        } else {
            drinks.forEach(drink => {
                if (drink.name.toLowerCase().includes(typed.toLowerCase()) && drink.category === category) {   
                    new_drinks_set += create_drink_card(drink)
                }
            })
        };
        document.querySelector('#dynamic_search').innerHTML = new_drinks_set
    })
}


function get_by_category(category, typed) {
    
    let new_drinks_set = ''
    
    fetch('api/drinks/all')
    .then(response => response.json())
    .then(drinks => {
        if (typed === '') {
            drinks.forEach(drink => {
                if (drink.category === category) {
                    new_drinks_set += create_drink_card(drink)
                }
            })
        } else {
            drinks.forEach(drink => {
                if (drink.category === category && drink.name.toLowerCase().includes(typed.toLowerCase())) {
                    new_drinks_set += create_drink_card(drink)
                }
            })
        }
        document.querySelector('#dynamic_search').innerHTML = new_drinks_set
    })
}


function create_drink_card(drink) {
    let tag = 'Alcoholic'
    if (!drink.alcoholic) {
        tag = 'Non-alcoholic'
    } 
    let image = drink.image_url
    if (!image) {
        image = '/static/shaker/cheers.png'
    }
    let drink_card = `
        <div class="card mb-3" style="max-width: 540px;">
            <div class="row g-0">
                <div class="col-md-4">
                    <a href="/drinks/${drink.name}">
                        <img src="${image}" class="img-fluid rounded-start" alt="...">
                    </a>
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">${drink.name}</h5>
                        <p class="card-text">${drink.category}</p>
                        <p class="card-text">${drink.glass}</p>
                        <p class="card-text"><small class="text-muted">${tag} </small></p>
                    </div>
                </div>
            </div>
        </div>
    `
    return (drink_card)
}