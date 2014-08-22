checkUser = () ->
  $('.statusSpan').hide()
  $('#imgCheckStatusLoading').show()
  $('#btnCheckUser').attr('readonly', true)
  username = $('#id_username').val()
  console.log username
  $.ajax("/api/user/#{username}/?format=json",
    {
      success: checkuserHandler
    })

checkuserHandler = (data, status, xhr) ->
  $('#imgCheckStatusLoading').hide()
  if data.exists
    $('#spUserExists').show()
  else
    $('#spUserNotExists').show()
  $('#btnCheckUser').attr('readonly', false)

$(document).ready () ->
  console.log 'Document loaded'
  $('#btnCheckUser').click(checkUser)