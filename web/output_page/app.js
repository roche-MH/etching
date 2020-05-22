$(document).ready(function(){
    
    push = false;
       
$('ul li a').click(function(){
       
       $(".tab").removeClass("active");
       
       $(this).addClass("active");
           
          $(".container").removeClass("actives");
       
       var contentId = $(this).attr("href");
       
       
       $('.container[id="'+contentId+'"]').addClass("actives");
       
       if(!push)
           
       history.pushState({}, '', contentId);
      
       push = false;
       
       return false;
      
   }); 
   
 
$(window).on("popstate", function() {
      
    push = true;
    
   var h = (window.location.href.indexOf("/") > -1) ? window.location.href.split("/").pop() : false;
       
   if(h == 'home.php') {
               
    $('ul li a[href="Home"]').click();
           
           
   } else {
           
       $('ul li a[href="'+h+'"]').click();
           
       
       }
       
   });
   
   


});

function titleClick(img) {
    location.href="file:///C:/Users/user/Desktop/vnlljs%20prtc/js_study/etching_v1/srchprtc.html";
}

function OutputUpload(img) {
    location.href="https://blog.naver.com/handuelly";
}