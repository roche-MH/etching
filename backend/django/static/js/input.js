function srcURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.srcimg-upload-wrap').hide();
            $('.file-upload-image_src').attr('src', e.target.result);
            $('.file-upload-content_src').show();
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        removeUpload_src();
    }
}

function refURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.refimg-upload-wrap').hide();
            $('.file-upload-image_ref').attr('src', e.target.result);
            $('.file-upload-content_ref').show();
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        removeUpload_ref();
    }
}

function removeUpload_src() {
    $('.file_upload_input_src').replaceWith($('.file_upload_input_src').clone());
    $('.file-upload-content_src').hide();
    $('.srcimg-upload-wrap').show();
}
$('.srcimg-upload-wrap').bind('dragover', function () {
    $('.srcimg-upload-wrap').addClass('srcimg-dropping');
});
$('.srcimg-upload-wrap').bind('dragleave', function () {
    $('.srcimg-upload-wrap').removeClass('srcimg-dropping');
});

function removeUpload_ref() {
    $('.file_upload_input_ref').replaceWith($('.file_upload_input_ref').clone());
    $('.file-upload-content_ref').hide();
    $('.refimg-upload-wrap').show();
}
$('.refimg-upload-wrap').bind('dragover', function () {
    $('.refimg-upload-wrap').addClass('refimg-dropping');
});
$('.refimg-upload-wrap').bind('dragleave', function () {
    $('.refimg-upload-wrap').removeClass('refimg-dropping');
});
