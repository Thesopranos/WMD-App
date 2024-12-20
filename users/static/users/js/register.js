const firstname = document.getElementById('register-firstname');
const lastname = document.getElementById('register-lastname');
const username = document.getElementById('register-username');
const email = document.getElementById('register-email');
const password = document.getElementById('register-password');
const dob = document.getElementById('register-dob');
const notifications = document.getElementById('register-notifications');
firstname.value = 'Mehmet';
lastname.value = 'Yılmaz';
username.value = 'mertcaki';
email.value = 'mertllcaki@gmail.com';
password.value = 'Mert1234!';
dob.value = '2000-01-01';
notifications.checked = true;

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
			}) .then(response => {
				return response.json(); // JSON verisini parse et
			}) .then(data => {
				console.log(data);
				if (data.success) {
					showVerificationForm();
				} else {
				document.getElementById('register-message').innerText = data.message;
				}
			}
			);

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
		return response.json();
	} ).then(data => {
		if (data.success) {
			document.getElementById('verification-message').innerText = data.message;
			setTimeout(() => {
				window.location.href = '/login/';
			}, 1000);
		} else {
			document.getElementById('verification-message').innerText = data.message;
		}
	});

});
