<div class="navbar navbar-inverse navbar-fixed-top">
 <div class="navbar-inner">
  <div class="container">
    <a data-toggle="collapse" data-target=".nav-collapse" class="btn btn-navbar">
        <i class="icon icon-reorder"></i>菜单</a>
    <a href="/index.htm" class="brand">RedMast</a>
   <div class="nav-collapse collapse">
    <ul class="nav">
     <li class=""><a href="/index.htm">首页</a></li>
     <li><a href="/list.htm">列表</a></li>
     <%foreach li in page_nav%>
         <li><a href="/<%@li['url']>"><%@li['title']></a></li>
     <%end%>
    </ul>
   </div>
  </div>
 </div>
</div>


