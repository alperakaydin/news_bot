function worker(){
    $.ajax({
        type:'get',
        url:'/news/api/data',
        success:function (data) {
            console.log(data);
            $("#borsa_count").text(data.borsaCount);
            $("#gundem_count").text(data.gundemCount);
            $("#yasam_count").text(data.yasamCount);
            $("#spor_count").text(data.sporCount);
            $("#teknoloji_count").text(data.teknolojiCount);
            $("#otomobil_count").text(data.otomobilCount);
            $("#selected_count").text(data.selectedCount);

            var sharedNum = $("#shared_count").text();
            console.log("sharedNum : ", sharedNum)
            if (sharedNum < data.shareCount){
                console.log("sharedNum : ", sharedNum)
                alert("sharedNum : ", sharedNum)
                 $('.modal-body').text("Paylaşılan yeni bir haberiniz var ..");
                        var modal = $('#exampleModal');
                        modal.modal('show');


                $("#shared_count").text(data.shareCount);
            }



        },
        complete: function (){
            setTimeout(worker, 2000);
        }

    })
};

$(document).ready(function(){
    var shareNewsNumber = 0;

     //Notification close

     //Notification close


    setTimeout(worker, 200);

    $("button").click(function(){

        jQuery("#message-notification").fadeIn("slow");

        var id = $(this).attr("data-id") ;
        var element = $(this);
        console.log(id);

        if (( $(this).attr("class") === "btn btn-outline-success btn-sm haber-sec" )){

            var link = '/news/api/add'+ id ;
            $.ajax({
                type:'get',
                url:link,
                success:function (data) {
                    if(data.error === false){
                        console.log(data);
                        element.parent().parent().parent().parent().css("border-color","red").css("box-shadow", "5px 10px 18px grey");
                        $("."+data.source) .remove();
                        $(".source-check").append("<span class='badge badge-dark ml-2 "+data.source+"'>" + data.source +" " + "<span class='badge badge-light'>"+ data.count +"</span> </span>");
                        element.removeClass("btn btn-outline-success btn-sm haber-sec");
                        element.addClass("btn btn-outline-danger btn-sm").text("Kaldır!");

                        $("span."+data.category).text(data.categoryCount);
                    }
                    else{
                        $('.modal-body').text(data.message);
                        var modal = $('#exampleModal');
                        modal.modal('show');
                    }

                }

            });


        }

        else if( $(this).attr("class") === "btn btn-outline-danger btn-sm" ){
            $(this).removeClass("btn btn-outline-danger btn-sm");
            $(this).addClass("btn btn-outline-success btn-sm haber-sec").text("Haberi Seç");
            $(this).parent().parent().parent().parent().css("border-color",defaultStatus).css("box-shadow", defaultStatus);

            var link = '/news/api/delete'+ id ;
            $.ajax({
                type:'get',
                url:link,
                success:function (data) {
                    console.log(data);
                    $("."+data.source) .remove();
                    $(".source-check").append("<span class='badge badge-dark "+data.source+"'>" + data.source +" " + "<span class='badge badge-light'>"+ data.count +"</span> </span>");
                }
            });

        }
        else if( $(this).attr("class") === "btn btn-outline-danger btn-sm selected-button-cikar" ){
            var link = '/news/api/delete'+ id ;
            $.ajax({
                type:'get',
                url:link,
                success:function (data) {
                    console.log(data);
                }
            });

            $(this).parent().parent().parent().parent().parent().hide();

        }


    });

    $(".dropdown-item").click(function (){
        var news_id = $(this).attr("news-id");
        var username = $(this).attr("user-username");
        var this_link = '/news/api/yoneticiadd&'+news_id+'&'+username
        alert(this_link);
        $.ajax({
            type:'get',
            url:this_link,

            success:function (data){
                alert(data.message);
                if(data.error === true){
                    $('.modal-body').text(data.message);
                        var modal = $('#exampleModal');
                        modal.modal('show');
                }
            }
        })
       alert("dropdown");
    });





    $("#run-bot").click(function (){
        $.ajax({
            type:'get',
            url:'/news/run',
            success:function (data) {
                window.location.reload();
                console.log(data);
            }

        })

    });


    $("#category-selector").click(function () {

        var liste = [];
        liste = $(":checked");//.attr("value");
        alert(liste.length);
        for (var i = 0; i < liste.length; i++) {
            console.log(liste[i]["value"]);
            var val_category = liste[i]["value"];
            console.log(val_category);
            deneme = "ekonomi"
            $("div[id!='{{ deneme }}']").hide();
        }

    });
    $(function (){
    });


});