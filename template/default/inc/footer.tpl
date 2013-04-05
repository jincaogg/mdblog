<script src="/res/strapdown.js"></script>
<script>
//使用marked直接转码没有做色
$.each($('xxmp'),function(k,v){
    var obj=$(v);
    var md_body_str=$(v).text();
    var html=marked.parser(marked.lexer(md_body_str));
    obj.closest('div').html(html);
});
</script>
<footer>
      <div class="container">
        <div class="row">
          <div class="span12">
            <center>
              <p>Copyright © 2013</p>
            </center>
          </div>
        </div>
      </div>
</footer>
</html>
