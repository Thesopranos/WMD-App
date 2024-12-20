document.getElementById('register-form').addEventListener('submit', function(event) {
	event.preventDefault();

	const firstname = document.getElementById('register-firstname').value;
	const lastname = document.getElementById('register-lastname').value;
	const username = document.getElementById('register-username').value;
	const email = document.getElementById('register-email').value;
	const password = document.getElementById('register-password').value;
	const dob = document.getElementById('register-dob').value;
	const notifications = document.getElementById('register-notifications').checked;
		// Şifre kurallarına uygun olup olmadığını kontrol eden regex
		const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$/;
		if (passwordRegex.test(password)) {
			// Eğer şifre kurallara uyuyorsa hata mesajını gizle
			fetch('/api/register/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': createCsrfToken()
				},
				body: JSON.stringify({
					firstname,
					lastname,
					username,
					email,
					password,
					dob,
					notifications
				})
			});
			showVerificationForm();  // Doğrulama ekranını göster
		} else {
			// Şifre kurallara uymuyorsa hata mesajını göster
			alert('Şifreniz en az bir büyük harf, bir küçük harf, bir rakam ve bir özel karakter içermelidir.');
			return;
		}
	});


const createCsrfToken = () => {
	const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
	return csrfToken;
}


const showVerificationForm = () => {
	document.getElementById('register-container').style.display = 'none';
	document.getElementById('verification-container').style.display = 'block';
}

// Doğrulama kodu formu işlemi
document.getElementById('verification-container').addEventListener('submit', function(event) {
	event.preventDefault();

	const enteredCode = document.getElementById('verification-code').value;
	const email = document.getElementById('register-email').value;

	fetch('/api/verify/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': createCsrfToken()
		},
		body: JSON.stringify({
			email: email,
			code: enteredCode
		})
	}).then(response => {
		if (response.ok) {
			window.location.href = '/login/';
		} else {
			alert('Doğrulama kodu hatalı.');
		}
	});

});
