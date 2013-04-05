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
                <div class='md_div'><xmp class='uneditable md_body' style='display:block'>
                <%@li['body']></xmp>
                </div>
                </article>
                <%end%>
             </div>
            <%include inc/side.tpl%>
        </div>
    </div>
     
    
</div>
<script type='text/javascript'>
marked.setOptions({
	gfm: true,
	tables: true,
	breaks: false,
	pedantic: false,
	sanitize: false,
	smartLists: false,
	silent: false,
	highlight: null,
	langPrefix: 'lang-'   
    
});
$.each($('article .md_body'), function(k, v) {
    var obj=$(v);
    var md_body_str=$(v).text();
    var html=marked.parser(marked.lexer(md_body_str));
    obj.closest('div').html(html);
});
</script>

<%include inc/footer.tpl%>
