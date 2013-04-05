<%include inc/header.tpl%>
<%include inc/nav.tpl%>

<xmp theme='united' style='display:none;'>
</xmp>
<div class='main'>
    <div class='container'>
        <div class='row'>
             <div class='span9'>
                <h3><%=list_title></h3>
                <%foreach li in post_list%>
                    <div class='row'>
                        <div class='span7'><a href="/<%@li['url']>"><%@li['title']></a></div>
                        <div class='span2'><small><%@li['date']></small></div>
                    </div>
                    <hr></hr>
                <%end%>
             </div>
             <%include inc/side.tpl%>
        </div>
    </div>
     
    
</div>
<%include inc/footer.tpl%>
