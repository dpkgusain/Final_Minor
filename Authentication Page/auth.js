// Login Form
const loginForm = document.getElementById('login-form');
const emailInput = document.getElementById('email-input');
const passwordInput = document.getElementById('password-input');

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = emailInput.value;
  const password = passwordInput.value;

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      window.location.href = '/dashboard';
    } else {
      alert('Invalid email or password');
    }
  } catch (error) {
    console.error('Error logging in:', error);
    alert('An error occurred. Please try again later.');
  }
});

// Signup Form
const signupForm = document.getElementById('signup-form');
const signupEmailInput = document.getElementById('signup-email-input');
const signupPasswordInput = document.getElementById('signup-password-input');

signupForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = signupEmailInput.value;
  const password = signupPasswordInput.value;

  try {
    const response = await fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      window.location.href = '/dashboard';
    } else {
      alert('Error signing up. Please try again.');
    }
  } catch (error) {
    console.error('Error signing up:', error);
    alert('An error occurred. Please try again later.');
  }
});

// Toggle between login and signup forms
const loginLink = document.getElementById('login-link');
const signupLink = document.getElementById('signup-link');
const signupContainer = document.getElementById('signup-container');

loginLink.addEventListener('click', () => {
  signupContainer.style.display = 'none';
});

signupLink.addEventListener('click', () => {
  signupContainer.style.display = 'block';
});