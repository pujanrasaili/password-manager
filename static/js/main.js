// COPY TO CLIPBOARD
function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast();
    });
}

// SHOW TOAST
function showToast() {
    const toast = document.getElementById('toast');
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

// TOGGLE PASSWORD VISIBILITY
function togglePassword(id, password) {
    const el = document.getElementById('pw-' + id);
    if (el.textContent === '••••••••••••') {
        el.textContent = password;
    } else {
        el.textContent = '••••••••••••';
    }
}

// SEARCH PASSWORDS
function searchPasswords() {
    const query = document.getElementById('search').value.toLowerCase();
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const site = card.dataset.site.toLowerCase();
        const username = card.dataset.username.toLowerCase();
        if (site.includes(query) || username.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// GENERATE PASSWORD
function generatePassword() {
    fetch('/generate')
        .then(res => res.json())
        .then(data => {
            const field = document.getElementById('passwordField');
            field.value = data.password;
            checkStrength(data.password);
        });
}

// PASSWORD STRENGTH CHECKER
function checkStrength(password) {
    const fill = document.getElementById('strengthFill');
    const label = document.getElementById('strengthLabel');
    if (!fill || !label) return;

    let score = 0;
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    if (score <= 2) {
        fill.style.width = '33%';
        fill.style.background = '#ef4444';
        label.textContent = '⚠️ Weak';
        label.style.color = '#ef4444';
    } else if (score <= 3) {
        fill.style.width = '66%';
        fill.style.background = '#f59e0b';
        label.textContent = '🟡 Medium';
        label.style.color = '#f59e0b';
    } else {
        fill.style.width = '100%';
        fill.style.background = '#22c55e';
        label.textContent = '✅ Strong';
        label.style.color = '#22c55e';
    }
}

// CONFIRM DELETE
function confirmDelete(id) {
    if (confirm('Are you sure you want to delete this password?')) {
        window.location.href = '/delete/' + id;
    }
}

// CHECK STRENGTH ON INPUT
const pwField = document.getElementById('passwordField');
if (pwField) {
    pwField.addEventListener('input', () => checkStrength(pwField.value));
}