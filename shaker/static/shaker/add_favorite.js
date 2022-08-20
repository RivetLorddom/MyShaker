document.addEventListener('DOMContentLoaded', function() {

    button = document.querySelector(".favorite_button")
    favorite_state(button.id)
    button.addEventListener('click', () => favoriting(button.id))
})


async function favorite_state(mixed_id) {

    await new Promise(r => setTimeout(r, 120))

    id_array = mixed_id.split('-')
    drink_id = id_array[0]
    user_id = id_array[1]

    fetch(`/api/users/${user_id}`)
    .then(response => response.json())
    .then(user => {
        if (user['favorites'].includes(Number(drink_id))) {
            // console.log("You like it")
            document.getElementById(mixed_id).innerHTML = `<img src="/static/shaker/star-black.png" alt=""></img>`
        } else {
            // console.log("You dont like it")
            document.getElementById(mixed_id).innerHTML = `<img src="/static/shaker/star-grey.png" alt=""></img>`
        }
    })
}


function favoriting(mixed_id) {

    id_array = mixed_id.split('-')
    drink_id = Number(id_array[0])
    user_id = Number(id_array[1])
    fetch(`/api/users/${user_id}`)
    .then(response => response.json())
    .then(user => {
        favorites = user['favorites']
        if (favorites.includes(drink_id)) {
            del_favorite(user_id, drink_id, favorites)
        } else {
            add_favorite(user_id, drink_id, favorites)
        }
    })
    // refresh the button state
    favorite_state(mixed_id)

}


function add_favorite(user_id, drink_id, favorites) {
    favorites.push(drink_id)
    // console.log("trying to like")
    // console.log(favorites)
    fetch(`/api/users/${user_id}`, {
        method: "PUT",
        body: JSON.stringify({
            favorites: favorites
        })
    })
}

function del_favorite(user_id, drink_id, favorites) {
    // delete drink from the list of favorites
    // console.log("Trying to unlike")
    // console.log(favorites)
    for (var i = 0; i < favorites.length; i++) {
        if (favorites[i] === drink_id) {
            favorites.splice(i, 1);
        }
    }

    console.log(favorites)
    fetch(`/api/users/${user_id}`, {
        method: "PUT",
        body: JSON.stringify({
            favorites: favorites
        })
    })
}

