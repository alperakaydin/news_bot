$(document).ready(function(){
       $(function (){
           $("#category-selector").click(function (){
               var liste = [];
               liste = $(":checked");//.attr("value");
               alert(liste.length);
               for ( var i = 0; i < liste.length; i++ ) {
                   console.log(liste[i]["value"]);
                   var val_category = liste[i]["value"];
                   console.log(val_category);
                   deneme = "ekonomi"
                   $("div[id!='{{ deneme }}']").hide();
               }

           });



            $("#haber-gonder").click(function (){
               var id = $(this).attr("data-id") ;
               var link = '/news/index/'+ id ;
                $.ajax({
                    type:'get',
                    url:link,
                    success:function (data) {
                        console.log(data);
                    }
                });
            });

            $("#run-bot").click(function (){

                $.ajax({
                    type:'get',
                    url:'/news/run',
                    success:function (data) {
                        console.log(data);
                    }
                });
            });
        });





        });