function validateDateOfBirth() {
  var inputDate = document.getElementById("dob").value;
  var xhr = new XMLHttpRequest();

  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
      var response = JSON.parse(xhr.responseText);
      displayValidationResult(response.message);
    }
  };

  xhr.open("GET", "validate_date.php?dob=" + inputDate, true);
  xhr.send();
}

function displayValidationResult(message) {
  var errorSpan = document.getElementById("dobError");
  errorSpan.innerHTML = message;

  if (message === "") {
    // If no error message, submit the form
    document.getElementById("myForm").submit();
  }
}
