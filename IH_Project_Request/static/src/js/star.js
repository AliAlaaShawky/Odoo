function setPriority(value) {
    const stars = document.querySelectorAll('.o_priority_star');
    stars.forEach(star => {
        const starValue = parseInt(star.getAttribute('data-value'), 10);
        if (starValue <= value) {
            star.classList.remove('fa-star-o');
            star.classList.add('fa-star');
        } else {
            star.classList.remove('fa-star');
            star.classList.add('fa-star-o');
        }
    });
    document.querySelector('input[name="priority"]').value = value;
}
function updateInputValue(input) {
    const datalist = document.getElementById('users_datalist');
    const options = datalist.options;
    const hiddenInput = document.getElementById('end_user_id');
    for (let i = 0; i < options.length; i++) {
        if (options[i].value === input.value) {
            hiddenInput.value = options[i].dataset.id;  // Set hidden input value to the user id
            break;
        }
    }
}

// document.getElementById('end_user_input').addEventListener('input', function() {
//     const datalist = document.getElementById('users_datalist');
//     const options = datalist.options;
//     const hiddenInput = document.getElementById('end_user_id');
//     for (let i = 0; i < options.length; i++) {
//         if (options[i].value === this.value) {
//             hiddenInput.value = options[i].dataset.id;  // Store the user id in the hidden input field
//             break;
//         }
//     }
// });
