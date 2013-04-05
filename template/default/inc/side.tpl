<div class='span3'>
<aside class='aside'>
         <div class='well'>
                <section>  
                    <form class='form-search' method="get" action="https://www.google.com.hk/search?q=as" taget='_blank'>
                        <input type="hidden" name="q" value="site:redmast.com" />
                        <input type='text' name='q' size=5 class='search-query' placeholder='Search' style='width:80%' />
                        <button type='submit' class='btn' style='display:none'>Search</button>
                    </form>
                </section>
         </div>

          <div class='well'>
                <section>
                    <h3>About</h3>
                    <div>
                    </div>
        
                </section>
         </div>
         <div class='well'>
                <section>
                    <h3>Cats</h3>
                    <ol class='posts'>
                    <%foreach li in cats%>
                      <li><a href="/cat/<%@li['cat_str']>.htm"><%@li['cat_str']> [<%@li['count']>]</a></li>
                    <%end%>
                    </ol>

                </section>
         </div>
        <div class='well'>
                <section>
                    <h3>Tags</h3>
                    <ol class='posts'>
                    <%foreach li in tags%>
                      <li><a href="/tag/<%@li['tag_str']>.htm"><%@li['tag_str']> [<%@li['count']>]</a></li>
                    <%end%>
                    </ol>

                </section>
         </div>


         <div  class='well'>
                <section>
                    <h3>New </h3>
                    <ol class='posts'>
                        <%foreach li in top_list%>
                            <li><a href="/<%@li['url']>"><%@li['title']></a></li>
                        <%end%>
                    </ol>
                </section>
        </div>
</aside>
</div>
