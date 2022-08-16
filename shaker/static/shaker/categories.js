document.addEventListener("DOMContentLoaded", function() {

    let category_selector = document.getElementById("select_category")
    category_selector.addEventListener("change", function() {

        let category = this.value
        console.log(category)
        get_by_category(category)

    })




});


async function get_by_category(category) {

    // await new Promise(r => setTimeout(r, 1020));
    let new_drinks_set = document.createElement('div');
    
    
    fetch(`https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=${category}`)
    .then(response => response.json())
    .then(drinks_info => {
        let new_drinks = drinks_info.drinks
        console.log(new_drinks)
        
        new_drinks.forEach(function (drink) {
            console.log(drink.strDrink);
            
            let drink_card = "<p>Hello</p>"
            console.log(drink_card)
            
            new_drinks_set.innerHTML = drink_card
        });
    })
    document.getElementById("list-of-cards").appendChild(new_drinks_set);
}




// drink_card = `
// <div class="card mb-3" style="max-width: 540px;">
// <div class="row g-0">
// <div class="col-md-4">
//     <a href="{% url 'drink_page' ${drink.strDrink} %}">
//         <img src="${drink.strDrinkThumb}" class="img-fluid rounded-start" alt="...">
//     </a>
// </div>
// <div class="col-md-8">
//     <div class="card-body">
//     <h5 class="card-title">{{ drink.strDrink }}</h5>
//     <p class="card-text">{{ drink.strCategory }}</p>
//     <p class="card-text">{{ drink.strGlass }}</p>
//     <p class="card-text"><small class="text-muted">{{ drink.strAlcoholic }}</small></p>
//     </div>
// </div>
// </div>
// </div>
// `