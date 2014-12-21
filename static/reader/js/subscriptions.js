function subscribe_or_unsubscribe(source_id) {
  if(subscribed_info[source_id]) {
    console.log('Unsubscribing ...');
    $('#source-button-' + source_id).text("Unsubscribing");
    $.ajax({
      url: '/reader/query/subscriptions/unsubscribe/' + source_id
    }).done(function(data) {
      $('#source-button-' + source_id).text("Subscribe");
      subscribed_info[source_id] = false;
    });
  } else {
    console.log('Subscribing ...');
    $('#source-button-' + source_id).text("Subscribing");
    $.ajax({
      url: '/reader/query/subscriptions/subscribe/' + source_id
    }).done(function(data) {
      $('#source-button-' + source_id).text("Unsubscribe");
      subscribed_info[source_id] = true;
    });
  }
}
