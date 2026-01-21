document.addEventListener('DOMContentLoaded', () => {
    
    // --- Elements ---
    const form = document.getElementById('signupForm');
    const nameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirmPassword');
    const statusDiv = document.getElementById('formStatus');
    const toggleButtons = document.querySelectorAll('.toggle-password');

    // --- 1. Password Visibility Toggle ---
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const iconEye = btn.querySelector('.icon-eye');
            const iconOff = btn.querySelector('.icon-eye-off');

            if (input.type === 'password') {
                input.type = 'text';
                iconEye.classList.add('hidden');
                iconOff.classList.remove('hidden');
                btn.setAttribute('aria-label', 'Hide password');
            } else {
                input.type = 'password';
                iconEye.classList.remove('hidden');
                iconOff.classList.add('hidden');
                btn.setAttribute('aria-label', 'Show password');
            }
        });
    });

    // --- 2. Validation Logic ---
    const setError = (input, message) => {
        const errorSpan = document.getElementById(input.id + 'Error'); // e.g. nameError
        input.classList.add('invalid');
        errorSpan.textContent = message;
        input.setAttribute('aria-invalid', 'true');
    };

    const clearError = (input) => {
        const errorSpan = document.getElementById(input.id + 'Error');
        input.classList.remove('invalid');
        errorSpan.textContent = '';
        input.removeAttribute('aria-invalid');
    };

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    };

    // --- 3. Live Validation (Clear errors on type) ---
    [nameInput, emailInput, passInput, confirmInput].forEach(input => {
        input.addEventListener('input', () => {
            clearError(input);
            statusDiv.textContent = ''; // Clear global status
        });
    });

    // --- 4. Form Submission ---
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        let isValid = true;
        
        // Validate Name
        if (nameInput.value.trim() === '') {
            setError(nameInput, 'Full name is required');
            isValid = false;
        }

        // Validate Email
        if (emailInput.value.trim() === '') {
            setError(emailInput, 'Email is required');
            isValid = false;
        } else if (!validateEmail(emailInput.value)) {
            setError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }

        // Validate Password (Min 8 chars)
        if (passInput.value.length < 8) {
            setError(passInput, 'Password must be at least 8 characters');
            isValid = false;
        }

        // Validate Confirm Password
        if (confirmInput.value !== passInput.value) {
            setError(confirmInput, 'Passwords do not match');
            isValid = false;
        }

        if (isValid) {
            handleSignupSuccess();
        }
    });

    // --- 5. Success/Storage Logic ---
    async function handleSignupSuccess() {
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // 1. Disable button to prevent double-submit
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating account...';

    // 2. Prepare Data
    const payload = {
        username: nameInput.value,
        email: emailInput.value,
        password: passInput.value // Ensure your site uses HTTPS!
    };

    try {
        // --- API BOILERPLATE START ---
        // Replace 'https://api.yourdomain.com/register' with your actual endpoint
        const response = await fetch('http://127.0.0.1:8000/api/auth/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add Authorization header here if needed (e.g., Bearer token)
                // 'Authorization': 'Bearer ' + token 
            },
            body: JSON.stringify(payload)
        });

        // Parse JSON response
        const data = await response.json();

        // Check for server errors (4xx or 5xx status)
        if (!response.ok) {
            // Throw error to be caught by catch() block below
            throw new Error(data.message || 'Something went wrong. Please try again.');
        }
        // --- API BOILERPLATE END ---

        // 3. Handle Success
        statusDiv.className = 'form-status success';
        statusDiv.textContent = 'Account created! Redirecting...';
        
        // Optional: Save token if returned
        if (data.token) {
            localStorage.setItem('authToken', data.token);
        }

        // Redirect after short delay
        setTimeout(() => {
            window.location.href = '/dashboard.html';
        }, 1000);

    } catch (error) {
        // 4. Handle Errors
        console.error('Signup Error:', error);
        
        statusDiv.className = 'form-status error';
        statusDiv.textContent = error.message; // Show server error message to user
        
        // Reset button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign up';
    }
}})