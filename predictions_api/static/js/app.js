jQuery(document).ready(function () {
    $('.basicAutoComplete').autoComplete({
        resolver: 'custom',
        minLength: 0,
        events: {
/*            typed:function(newValue, callback) {
                console.log("new value",newValue)
                $.ajax({
                    url: 'http://localhost:5000/predict?value='+newValue+'&max_sequence_len=3&nested_list_len=4' ,
                    type: "post",
                    contentType: "application/json",
                    dataType: "json",
                    beforeSend: function () {
                        $('.overlay').show()
                    },
                    complete: function () {
                        $('.overlay').hide()
                    }
                }).done(function (jsondata, textStatus, jqXHR) {
                    callback(jsondata['data'])
               }).fail(function (jsondata, textStatus, jqXHR) {
                    console.log(jsondata)
                });
            }, */
            search: function (qry, callback) {
                // let's do a custom ajax call
                console.log("qry value",qry)
               $.ajax({
                   url: 'http://localhost:5000/predict?value='+qry+'&max_sequence_len=3&nested_list_len=4' ,
                   type: "post",
                   contentType: "application/json",
                   dataType: "json",
                   beforeSend: function () {
                       $('.overlay').show()
                   },
                   complete: function () {
                       $('.overlay').hide()
                   }
               }).done(function (jsondata, textStatus, jqXHR) {
                   callback(jsondata['data'])
              }).fail(function (jsondata, textStatus, jqXHR) {
                   console.log(jsondata)
               });
            }
        }
    });
})