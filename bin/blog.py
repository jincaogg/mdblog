#!/usr/bin/env python
#-*-coding:utf8-*-
import os,re,sqlite3
import sys
import os.path

class Md:
    def loop(self,startdir,ext='.md'):
        '''
        遍历指定目录中的指定后缀的文件并返回解析后的迭代器
        '''
        old_cwd=os.getcwd()
        os.chdir(startdir)
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if os.path.splitext(filename)[1] == ext:
                    filepath = os.path.join(dirpath, filename)
                    print(" input:" + filepath)
                    path_split=os.path.split(dirpath)
                    type_str=(path_split[1],'default')['.'==path_split[0]]
                    input_file = open(filepath)
                    size=os.path.getsize(filepath)
                    mtime=os.path.getctime(filepath)
                    text = input_file.read()
                    input_file.close()
                    
                    (conf,body)=self.look(text)
                    conf['size']=size
                    conf['mtime']=mtime
                    conf['cat']=type_str
                    conf['body']=body
                    conf['url']=filepath.replace('.md','.htm')[2:]#.replace(os.path.sep,'_').replace(r'.','')
                    yield conf
        os.chdir(old_cwd)

    def look(self,text):
        '''
        解析文本头的参数
        '''
        key_str=('type','date','title','tags')

        re_str=r'^('+'|'.join(key_str)+'): *(.*?) *\n.*?'
        match_str=r'^ *$'
        ress=re.search(match_str,text,re.M)
        #print ress.start(),ress.end()
        res=re.findall(re_str,text[0:ress.start()],re.M+re.I)
        body=text[ress.end():]
        conf={}
        for k,v in res:
            k=str.lower(k)
            conf[k]=v
        
        for k in key_str:
            if k not in conf:
                conf[k]=''
        
        if conf['type']=='':
            conf['type']='post'
        return conf,body 

class Db:
    '''采用内存数据库暂存文本以便后续分析'''

    conn=None
    cur=None
    keys=('type','date','url','title','cat','tags','body','md5','mtime','size')

    def __init__(self,keys=('type','date','url','title','cat','tags','body','md5','mtime','size'),
                      db_file=':memory:'):
        self.keys=keys
        self.connect(db_file)
        self.create()
    
    def connect(self,db_file=':memory:'):
        self.conn=sqlite3.connect(db_file)
        self.conn.text_factory = str
        self.conn.row_factory=sqlite3.Row
        self.cur=self.conn.cursor()
       
    def create(self):
        self.connect()
        fields=','.join(self.keys)
        create_sql="create table content(%s);" % fields
        self.cur.executescript(create_sql)
        
    def add(self,row):
        #print row
        fields=[]
        values=[]
        vals=[]
        for k in  self.keys:
            if k in row:
                vals.append('?')
                fields.append(k)
                v=row[k]
                values.append(v)
        sql_insert="insert into content(%s) values(%s)" % (','.join(fields),','.join(vals))
        self.cur.execute(sql_insert,values)

    def select(self,where='1=1',fields='*'):
        for one in self.cur.execute("select %s from content where %s" % (fields,where)):
            yield one

class Tpl:
    '''简单模板实现'''
    dir_out='' # 所有静态文件输出到public 目录
    old_cwd=''
    tpl_dir=''
    theme=''

    def __init__(self,theme_name='default',dir_out='public',dir_tpl='template'):
        self.theme=theme_name 
        self.dir_out=dir_out
        old_cwd=os.path.dirname(os.path.realpath(__file__))+'/../'
        tpl_dir=os.path.join(old_cwd,dir_tpl,theme_name)
        #print tpl_dir
        os.chdir(tpl_dir)
        self.old_cwd=old_cwd
        self.tpl_dir=tpl_dir

    def __del__(self):
        os.chdir(self.old_cwd)

    def parse(self,file_path,data):
        txt=self.parseInc(file_path)
        txt=self.parseList(txt,data)
        return self.parseVar(txt,data)
    
    def parseInc(self,file_path):
        txt=open(file_path).read()
        include_re=re.compile(r'<%include +(.*)%>')
        parse_txt=include_re.sub(lambda m:self.parseInc(m.group(1)),txt)
        return parse_txt
    
    def parseVar(self,txt,data):
        var_re=re.compile(r'<%=([a-zA-Z0-9_]+)>')
        parse_txt=var_re.sub(lambda m:data.get(m.group(1),''),txt)
        return parse_txt 
    
    def parseList(self,txt,data):
        #data={'data':[{'title':'ts','body':'tsetbody'},{'title':'ts2','body':'bodyddd3'}]}
        foreach_re=re.compile(r'<%foreach (\w+) in (\w+)%>')
        bl=re.compile(r'<%@([a-zA-Z0-9_\[\]\'\"]+)>')
        end_re=re.compile(r'<%end%>')
        rest=''
        i=foreach_re.search(txt)
        if i!= None :    
            (i_str,idata_str)=i.groups()
            rept_t=''
            if not idata_str in data:
                li_data=()
            else:
                li_data=data[idata_str]
            start_h=i.span()[0]
            start=i.span()[1]
            j=end_re.search(txt[start:])
            end=j.span()[0]
            end_e=j.span()[1]
            rept=txt[start:start+end].replace('<%@'+i_str,'<%@li_rand_1986')
            #print rept 
            list_arr=[]
            global li_rand_1986 
            li_rand_1986=[]
            for li_rand_1986 in li_data:
                #print li 
                rept_t+=bl.sub(lambda m:eval(m.group(1)),rept)
            del(li_rand_1986)
            rest+=txt[0:start_h]+rept_t+txt[start+end_e:]
            rest=self.parseList(rest,data)
        if rest=='':
            return txt
        else:
            return rest

    def write(self,cur_dir,row,tpl='content.tpl',filename=''):
        if filename=='' :
            filename=row['url']

        to_file=os.path.join(cur_dir,self.dir_out,filename)
        to_dir=os.path.dirname(to_file)
        if not os.path.isdir(to_dir):
            os.makedirs(to_dir)

        print 'output:',to_file
        post=self.parse(tpl,row) 
        f=file(to_file,'w')
        f.write(post)
        f.close()

class blog:
    '''
    MD Blog 生成工具
    '''
    dir_content=''
    db=None
    cur_dir=None
    tp=None

    def __init__(self,theme_name='default',dir_content='content',dir_out='public',dir_tpl='template'):
        self.cur_dir=os.path.dirname(os.path.realpath(__file__))+'/../'
        self.dir_content=dir_content
        self.tp=Tpl(theme_name,dir_out,dir_tpl)

    def gen(self):
        self.db=Db()

        db_tags=Db(('type','date','url','title','cat','tag','mtime'));

        tp=self.tp 
        db=self.db 
        cur_dir=self.cur_dir
        
        #load db
        for i in Md().loop(self.dir_content):
            db.add(i)
            tags=i['tags'].split(',')
            if len(tags)>0:
                for tag in tags:
                    row={'tag':tag.strip()}                    
                    for f in db_tags.keys:
                        if f != 'tag':
                            row[f]=i[f]
                    db_tags.add(row)
                    
       
        top_list=[]
        for i in db.select('type="post" order by mtime desc limit 10'):
            top_list.append(i)

        #page gen
        pages=[]
        for i in db.select('type="page" order by mtime'):
            i=dict(i)
            pages.append(i)
            tp.write(cur_dir,i,'page.tpl')

        #gen cats
        cats=[]
        for i in db.select('type="post" group by cat','count(1) as post_count,cat as cat_str'):
            i=dict(i)
            i['count']=str(i['post_count'])
            cats.append(i)
        #
        tags=[]
        for i in db_tags.select('type="post" group by tag order by count(1) desc','count(1) as tag_count,tag as tag_str'):
            i=dict(i)
            i['count']=str(i['tag_count'])
            if len(i['tag_str'])>0:
                tags.append(i)

        #gen cats
        for i in cats:
            cat_list=[]
            for j in db.select('type="post" and cat="%s" order by mtime ' %  i['cat_str']):
                j=dict(j)
                cat_list.append(j)
            
            catlist={'post_list':cat_list,'top_list':top_list,'page_nav':pages,'cats':cats,'tags':tags,'list_title':i['cat_str'],'title':'分类：'+i['cat_str']}
            tp.write(cur_dir,catlist,'cat.tpl','cat/%s.htm' % i['cat_str'])    
        
        #gen tags
        for i in tags:
            tag_list=[]
            for j in db_tags.select('type="post" and tag="%s" order by mtime' % i['tag_str']):
                j=dict(j)
                tag_list.append(j)
            taglist={'post_list':tag_list,'top_list':top_list,'page_nav':pages,'cats':cats,'tags':tags,'list_title':i['tag_str'],'title':'Tag：'+i['tag_str']}
            tp.write(cur_dir,taglist,'cat.tpl','tag/%s.htm' % i['tag_str'])

        #gen index
        index={'news_list':[],'top_list':top_list,'title':'首页','page_nav':pages,'cats':cats,'tags':tags}
        for i in db.select('type="post" order by mtime desc limit 3'):
            i=dict(i)
            if len(i['body'])>300:
                i['body']="\n"+i['body'].decode('utf-8')[:300].encode('utf-8').lstrip()
            index['news_list'].append(i)
        tp.write(cur_dir,index,'index.tpl','index.htm')
        
        #gen content list
        alllist={'post_list':[],'top_list':index['top_list'],'page_nav':pages,'cats':cats,'tags':tags,'cat_str':'所有文章','title':'列表'}
        
        for i in db.select('type="post" order by mtime desc '):
            i=dict(i)
            i['page_nav']=pages
            tp.write(cur_dir,i,'content.tpl')
            if len(i['body'])>200:
                i['body']='\n'+i['body'][:150].lstrip()
        
            alllist['post_list'].append(i)
        tp.write(cur_dir,alllist,'cat.tpl','list.htm')    
        
        #gen pages
        pages=[]
        for i in db.select('type="page" order by mtime'):
            i=dict(i)
            i['page_nav']=pages
            pages.append(i)
            tp.write(cur_dir,i,'page.tpl')

if __name__=='__main__':
    cur_dir=os.path.dirname(os.path.realpath(__file__))+'/../'
    #content='/Users/jc/Dropbox/Apps/mdblog/content/'
    content=cur_dir+'content'
    blog('default',content,'public','template').gen()
