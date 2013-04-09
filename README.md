mdblog
======

静态博客生成程序

[详细](http://redmast.com/post/Other/github_markdown.htm)


###文件目录:

    - bin 脚本存放目录
    
    - content md文档存放目录，可以直接放到dropbox上
        -page pages存放
        -post posts存放
        
    - public 公共访问的目录，这个目录就是需要同步到你的网站根目录
    
    - template 模板存放

###使用：
    
    1. >git clone https://github.com/jincaogg/mdblog.git 
    
    2. 将md文档拷贝到content 下的page或者post目录下
    
    3. >bin/blog.py
    
    4. 将public目录下的所有内容同步到 github 或者其他可访问的目录