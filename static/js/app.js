jQuery(document).ready(function () {
    $('.basicAutoComplete').autoComplete({
        resolver: 'custom',
        minLength: 0,
        events: {
        search: function (qry, callback) {
               // let's do a custom ajax call
               let regex = /[^a-zA-Z ]+/
                  if(qry.match(regex))
                  {
                    callback([]);
                  }
                  else
                  {
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
                         callback($.map(jsondata['data'], function (item) {
                               return item.toString()
                         }));
                    }).fail(function (jsondata, textStatus, jqXHR) {
                          console.log(jsondata)
                      });
                  }
            },
        },
       formatResult: function (item) {
            let myItem = item.split(",");
            let percentage = (myItem[1] * 100).toFixed(2); 
  			return {
  				id: myItem[0],
      			text: myItem[0],
      			html: '<p>'+ myItem[0] + '</p><p>' + percentage +'%</p>'
      			
    		}
    	},
    	
    });
})