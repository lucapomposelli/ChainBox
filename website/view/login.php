<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
namespace Fincode;

require_once '../src/config.inc.php';
employeeIsLogged();

echo getHeader('Login');
?>

<div class="w3-container w3-card-4">
	<div class="w3-border">
		<div class="w3-container w3-blue">
			<h3 class="w3-center">FinCode Login</h3>
		</div>
		<form action="dashboard.php" method="POST" onsubmit="return validateLogin();" class="w3-container w3-padding">
			<div class="w3-section">
				<input type="text" id="username" name="username" placeholder="Utente" class="w3-cell w3-input w3-border">
			</div>
			<div class="w3-section">
				<input type="password" id="password" name="password" placeholder="Password" autocomplete="off" class="w3-cell w3-input w3-border">
			</div>
			<span id="errorLogin" class="w3-text-red"></span>
			<button type="submit" class="w3-button w3-medium w3-blue w3-hover-dark-gray w3-right">Accedi</button>
		</form>
		<div class="w3-container w3-border-top">
			<span class="w3-tiny w3-right w3-padding-16">&copy; 2021 CM Consulting Network S.p.A.</span>
		</div>
	</div>
</div>

<?php echo loadJQueryScripts(); ?>

<script type="text/javascript">
    function validateLogin() {
        valid = true;
		$('#errorLogin').html('');

		username = $('#username').val();
		if (username == 0 || username == null) {
			$('#errorLogin').html('Inserire il campo username');
			valid = false;
		} else {
			password = $('#password').val();
			if (password == 0 || password == null) {
				$('#errorLogin').html('Inserire il campo password');
				valid = false;
			}
		}

		if (valid) {
			$.ajax({
				url: '../src/ajax.php',
				method: 'POST',
				dataType: 'json',
				async: false,
				data: {
					target: 'doLogin',
					username: username,
					password: password
				},
				success: function(res) {
					if (res.error) {
						$('#errorLogin').text(res.error);
						valid = false;
					}
				},
				error: function(res) {
					console.log(res);
					alert('Si è verificato un errore nella richiesta di chiamata AJAX!');
				}
			});
		}

		return valid;
	}
</script>

<?php echo getFooter(); ?>