document.getElementById('register-form').addEventListener('submit', function(event) {
	event.preventDefault();

	const firstname = document.getElementById('register-firstname').value;
	const lastname = document.getElementById('register-lastname').value;
	const username = document.getElementById('register-username').value;
	const email = document.getElementById('register-email').value;
	const password = document.getElementById('register-password').value;
	const dob = document.getElementById('register-dob').value;
	const notifications = document.getElementById('register-notifications').checked;

	if (users.find(user => user.username === username)) {
		document.getElementById('register-error-message').textContent = 'Bu kullanıcı adı zaten alınmış.';
	} else {

		// Şifre kurallarına uygun olup olmadığını kontrol eden regex
		const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$/;

		if (passwordRegex.test(password)) {
			// Eğer şifre kurallara uyuyorsa hata mesajını gizle
			showVerificationForm();  // Doğrulama ekranını göster
		} else {
			// Şifre kurallara uymuyorsa hata mesajını göster
			alert('Şifreniz en az bir büyük harf, bir küçük harf, bir rakam ve bir özel karakter içermelidir.');
			return;
		}
	}
});

// Doğrulama kodu formu işlemi
document.getElementById('verification-form').addEventListener('submit', function(event) {
	event.preventDefault();

	const enteredCode = document.getElementById('verification-code').value;

	if (parseInt(enteredCode) === verificationCode) {
		// Burada kullanıcının kaydının doğrulandığı işlemleri gerçekleştirebilirsiniz.
		alert('Başarıyla kaydoldunuz! Şimdi giriş yapabilirsiniz.');
		showLoginForm(); // Giriş ekranını göster
	} else {
		document.getElementById('verification-error-message').textContent = 'Geçersiz doğrulama kodu!';
	}
});
