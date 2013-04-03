 <aside class='span3 aside'>
        <div class=''>
                <section >  
                    <form class='well form-search' method="get" action="https://www.google.com.hk/search" taget='_blank'>
                        <input type="hidden" name="domains" value="site:jincaogg.github.com">
                        <input type='text' name='q' size=5 class='input-medium search-query'>
                        <button type='submit' class='btn'>搜</button>
                    </form>
                </section>

         </div>

          <div>
                <section class='well'>
                    <h3>About</h3>
                    <div>
                    </div>
        
                </section>
                <section class='well'>
                    <h3>Top </h3>
                    <ol class='posts'>
                        <%foreach li in top_list%>
                            <li><a href="<%@li['url']>"><%@li['title']></a></li>
                        <%end%>
                    </ol>
                </section>
        </div>
</aside>

