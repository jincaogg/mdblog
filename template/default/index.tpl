<%include inc/header.tpl%>
<%include inc/nav.tpl%>
<xmp theme='united' style='display:none;'>
</xmp>
<div class='main'>
    <div class='container'>
        <div class='row'>
             <div class='span9'>
                <%foreach li in news_list%>
                <article>
                 <small><%@li['date']></small>
                <h1><a href="<%@li['url']>"><%@li['title']></a></h1>
                <div><pre>
                <%@li['body']></pre>
                </div>
                </article>
                <%end%>
             </div>
            <%include inc/side.tpl%>
        </div>
    </div>
     
    
</div>
<%include inc/footer.tpl%>
