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
                    #print type_str
                    input_file = open(filepath)
                    size=os.path.getsize(filepath)
                    mtime=os.path.getmtime(filepath)
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
        
        
        #print conf
        return conf,body 

class Db:
    '''采用内存数据库暂存文本以便后续分析'''

    conn=None
    cur=None
    keys=('type','date','url','title','cat','tags','body','md5','mtime','size')

    def __init__(self,db_file=':memory:'):
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
        #print sql_insert,values
        self.cur.execute(sql_insert,values)

    def select(self,where='1=1'):
        for one in self.cur.execute("select * from content where %s" % where):
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
        old_cwd=os.getcwd()
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
        #print txt,data
        return self.parseVar(txt,data)
    
    def parseInc(self,file_path):
        txt=open(file_path).read()
        include_re=re.compile(r'<%include +(.*)%>')
        parse_txt=include_re.sub(lambda m:self.parseInc(m.group(1)),txt)
        return parse_txt
    
    def parseVar(self,txt,data):
        var_re=re.compile(r'<%=([a-zA-Z0-9_]+)>')
        parse_txt=var_re.sub(lambda m:data.get(m.group(1),''),txt)
        #print parse_txt
        return parse_txt 
    
    def parseList(self,txt,data):
        #data={'data':[{'title':'ts','body':'tsetbody'},{'title':'ts2','body':'bodyddd3'}]}
        foreach_re=re.compile(r'<%foreach (\w+) in (\w+)%>')
        bl=re.compile(r'<%@([a-zA-Z0-9_\[\]\'\"]+)>')
        end_re=re.compile(r'<%end%>')
        rest=''
        #rept_t=''
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
        self.cur_dir=os.getcwd()
        self.dir_content=dir_content
        self.tp=Tpl(theme_name,dir_out,dir_tpl)

    def gen(self):
        self.db=Db()

        tp=self.tp 
        db=self.db 
        cur_dir=self.cur_dir
        
        #load db
        for i in Md().loop(os.path.join(cur_dir,self.dir_content)):
            db.add(i)

        #page gen
        pages=[]
        for i in db.select('type="page" order by mtime'):
            i=dict(i)
            pages.append(i)
            tp.write(cur_dir,i,'page.tpl')
        
        #gen index
        index={'news_list':[],'top_list':[],'title':'首页','page_nav':pages}
        for i in db.select('type="post" order by mtime desc limit 3'):
            i=dict(i)
            if len(i['body'])>1000:
                i['body']=i['body'][:1000]
            index['news_list'].append(i)
        
        for i in db.select('type="post" order by mtime desc limit 10'):
            index['top_list'].append(i)
        
        tp.write(cur_dir,index,'index.tpl','index.htm')
        
        alllist={'post_list':[],'top_list':index['top_list'],'page_nav':pages,'title':'列表'}
        #gen contents
        for i in db.select('type="post" order by mtime desc '):
            i=dict(i)
            i['page_nav']=pages
            tp.write(cur_dir,i,'content.tpl')
            if len(i['body'])>300:
                i['body']=i['body'][:300]
        
            alllist['post_list'].append(i)
        tp.write(cur_dir,alllist,'cat.tpl','list.htm')    
        
        #gen pages
        pages=[]
        for i in db.select('type="page" order by mtime'):
            i=dict(i)
            i['page_nav']=pages
            pages.append(i)
            tp.write(cur_dir,i,'page.tpl')
        
        #gen arctive 
        #gen tags

if __name__=='__main__':
    blog('default','content','public','template').gen()

