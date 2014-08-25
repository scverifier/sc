KEYCODE_ESCAPE = 27

cancel = () ->
  window.location.href = '/data/genders'

$(document).ready(() ->
  $('#button-id-cancel').click(cancel)
)