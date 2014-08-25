checkUser = () ->
  $('#divAlertsContainer').children().hide()
  $('#btnUsernameCheck').button('loading')
  username = $('#id_username').val()
  $.ajax("/api/user/#{username}/?format=json",
    {
      success: checkuserHandler
    })

checkuserHandler = (data, status, xhr) ->
  $('#btnUsernameCheck').button('reset')
  showCheckUserAlert(data.exists)

showCheckUserAlert = (userExists) ->
  username_input = $('#id_username').parent()
  if userExists
    alertbox = $('#spAlertUserExists')
    username_input.addClass('has-success')
  else
    alertbox = $('#spAlertUserNotExists')
    username_input.addClass('has-error')
  alertbox.fadeIn(->
    setTimeout((=>alertbox.fadeOut()), delay=1000)
  )

usernameInputChanged = () ->
  val = $('#id_username').val()
  if val
    disabled = false
  else
    disabled = true
  $('#btnUsernameCheck').prop('disabled', disabled)
  $('#id_username').parent().removeClass('has-error').removeClass('has-success')
  $('#divAlertsContainer').children().hide()

formInputChanged = () ->
  $('#submit-id-verify').prop('disabled', not isFormValid())

isFormValid = () ->
  if not $('#id_username').val()
    return false
  # no checked radio buttons
  if $.grep($('[name=gender]'), (item) -> $(item).is(':checked')).length == 0
    return false
  return true

$(document).ready () ->
  console.log 'Document loaded'
  $('#btnUsernameCheck').click(checkUser)
  $('#id_username').on('input', usernameInputChanged)
  $('#divAlertsContainer').children().hide()
  usernameInputChanged()
  $('#verificationForm :input').on('input', formInputChanged)
  $('#verificationForm :input[type=radio]').change(formInputChanged)
