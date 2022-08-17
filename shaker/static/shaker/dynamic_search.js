document.addEventListener('DOMContentLoaded', function() {

    let search_bar = document.querySelector('#search_bar')
    search_bar.addEventListener('keyup', function() {
        let typed = search_bar.value
        console.log(typed)
        get_drinks(typed)
    } )

});



function get_drinks(typed) {

    let new_drinks_set = ''

    fetch('api/drinks/all')
    .then(response => response.json())
    .then(drinks => {

        drinks.forEach(drink => {
            // check matches case-insensitively
            if (drink.name.toLowerCase().startsWith(typed.toLowerCase())) {
                console.log(drink.name)


                drink_card = `
                    <p> Hello, ${drink.name} </p>
                    
                    <div class="card mb-3" style="max-width: 540px;">
                    <div class="row g-0">
                    <div class="col-md-4">
                        <a href="/drinks/${drink.name}">
                            <img src="${drink.image_url}" class="img-fluid rounded-start" alt="...">
                        </a>
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                        <h5 class="card-title">${drink.name}</h5>
                        <p class="card-text">${drink.category}</p>
                        <p class="card-text">${drink.glass}</p>
                        <p class="card-text"><small class="text-muted">${drink.alcoholic} </small></p>
                        </div>
                    </div>
                    </div>
                </div>
                `
                // console.log(drink_card)

                new_drinks_set += drink_card
            }
            
        });
        console.log(new_drinks_set)
        document.querySelector('#list-of-cards').innerHTML = new_drinks_set
    })
}