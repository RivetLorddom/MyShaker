document.addEventListener('DOMContentLoaded', function() {
    show_ingredient = document.querySelector('#ingredient')
    show_glass = document.querySelector('#glass')
    show_category = document.querySelector('#category')
    
    want_to_show = [
        show_ingredient = document.querySelector('#ingredient'),
        show_glass = document.querySelector('#glass'),
        show_category = document.querySelector('#category')
    ]
  
    want_to_show.forEach(field => {
        field.addEventListener('click', () => show_form(field.id)) 
    })
})


function show_form(id) {
    console.log(id)
    form_to_show = document.querySelector(`#add_${id}`)
    form_to_show.style.display = 'block'
    document.getElementById(`focus_add_${id}`).focus()

}