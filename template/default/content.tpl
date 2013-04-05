<%include inc/header.tpl%>
<%include inc/nav.tpl%>

<div class='container'>
  <div class='row'>
    <div class='span12'>
        <h2><%=title></h2>
        <small><%=date></small>
        <hr/>
        <div class="span2 toc-container">
         <div data-spy="affix" data-offset-top="185" style="width:140px;" class="toc"></div>
        </div>
    </div>
  </div>
</div>
<xmp theme="united" style="display:none;">
<%=body>
</xmp>
<div class='container'>
<div>
<style>
#disqus_thread{ 
    border-top: 1px solid #CCCCCC;
    padding-top: 30px;
}
.toc{
    position: fixed; 
    display: block;
    top: 90px; 
    border: 1px solid rgb(204, 204, 204);
    padding: 12px; 
    width: 190px;
    background-color: rgb(255, 255, 238); 
    right: 140px;
    display:none;
}

</style>
<div id="disqus_thread"></div>

<script type="text/javascript">
        /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
        var disqus_shortname = 'redmast'; // required: replace example with your forum shortname

        /* * * DON'T EDIT BELOW THIS LINE * * */
        (function() {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();


window.onload = function () {
        // Looks for an element with the class "toc" and appends an empty list
        $(".toc").append("<ol id='toc'></ul>");
        var TOC = $("ol#toc");
        
        $.each($('#content h2'), function(k, v) {
          var heading = $(v); // get the heading
          var headingText = $(v).text(); // get the value of the heading
          // make a URI-friendly id for the heading
          var headingID = encodeURIComponent(headingText);
          $(v).attr("id", headingID); //assign the new id
          // change the heading text to include a number for prettier headings
          heading.text((k+1) +". " + headingText);
          // create a link in the list for the heading
          TOC.append("<li><a href=\"#" + headingID +"\">" + headingText + "</a></li>" );
        });
        // Put a title on the table of contents
        $(".toc").prepend("<h3>目录</h3>");
      }

</script>
</div>    
</div>
<%include inc/footer.tpl%>
