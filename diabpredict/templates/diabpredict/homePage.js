const icon = document.getElementById('icon');

const button = document.getElementById('get-started-button');
const buttonsContainer = document.getElementById('category-button-container');
button.addEventListener('click', () => {
    buttonsContainer.style.display = 'inline-flex';
    button.style.display = 'none';
});

const patientButton = document.getElementById('login-button');
patientButton.addEventListener('click', () => {
    console.log('patient button is clicked');
})
const providerButton = document.getElementById('signup-button');
providerButton.addEventListener('click', () => {
    console.log('provider button is clicked');
})