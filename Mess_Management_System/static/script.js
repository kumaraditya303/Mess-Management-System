function fileValidation() {
    var fileInput = document.getElementById('customfile');
    var filePath = fileInput.value;
    var allowedExtensions = /(\.jpg|\.jpeg)$/i;
    if (!allowedExtensions.exec(filePath)) {
        alert('Please upload file having extensions .jpeg or .jpg only.');
        fileInput.value = '';
        return false;
    }
    document.getElementsByClassName('custom-file-label').text = fileInput.files[0].name;
}