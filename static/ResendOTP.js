function ResendOTP(email, ResendOTPmessage) {
	
	mess = document.getElementById(ResendOTPmessage);
    console.log(email)
	mess.innerText = "Sending...";
	$.ajax({
		type: 'GET',
		url: '/resend_OTP',
		data: {user:email},
		success: function(data){
			mess.innerText = data;

		}
	})
}