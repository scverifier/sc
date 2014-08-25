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
  if userExists
    alertbox = $('#spAlertUserExists')
    $('#id_username').parent().addClass('has-success')
  else
    control = $('#spAlertUserNotExists')
    $('#id_username').parent().addClass('has-error')
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


$(document).ready () ->
  console.log 'Document loaded'
  $('#btnUsernameCheck').click(checkUser)
  $('#id_username').on('input', usernameInputChanged)
  $('#divAlertsContainer').children().hide()
  usernameInputChanged()
