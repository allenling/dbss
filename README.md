Whysos.info 源码    
====
环境:      
Centos6.4    
uwsgi    
nginx    
django-1.5.4     
postgresq    
redis      
**不包含服务器优化**   
**设计在wiki有说明**     

=====
### 本地配置
需要在本地建立local_settings.py来配置本地的一些内容    
1.DEFAULT\_FROM\_EMAIL = dbss.local\_settings.DEFAULT\_FROM\_EMAIL     
2.EMAIL\_HOST= dbss.local\_settings.EMAIL\_HOST     
3.EMAIL\_PORT = dbss.local\_settings.EMAIL\_PORT     
4.EMAIL\_HOST\_USER = dbss.local\_settings.EMAIL\_HOST\_USER            
5.EMAIL\_HOST\_PASSWORD = dbss.local\_settings.EMAIL\_HOST\_PASSWORD            
6.DATABASES = {     
    'default': {      
        ...    
        'USER': dbss.local_settings.DBROOT,        
        'PASSWORD': dbss.local_settings.DBPWD,          
        ...          
}                 
7.STATIC\_ROOT = dbss.local\_settings.STATIC\_ROOT             
8.MEDIA\_ROOT = dbss.local\_settings.MEDIA\_ROOT          
9.SECRET\_KEY = dbss.local\_settings.SECRET\_KEY，这个是自动生成的，所以不配置用自动生成的值也可以      

====
### 关于第三方库        
1.django-avatar的修改在fork的版本里面    
2.ckeditor是用的django-captcha是使用django-ckeditor-updated-4.2.7版本，修改的内容只限于ckeditor的静态文件,可以直接使用static里面的ckeditor。如果你想使用galleriffic，有个小小的bug，内容见[小bug](https://github.com/shaunsephton/django-ckeditor/issues/106)       
3.daemonize的修改见fork版本，或者直接使用当前目录下的daemonize.py文件     
4.django-simple-captcha在使用FormWizard的时候有个二次验证的问题，详情见[地址](http://blog.csdn.net/a_9884108/article/details/18795249)，github上的讨论[github](https://github.com/mbi/django-simple-captcha/issues/6)
5.django-haystack     
6.rest_framework     
7.django-registration     
8.django_rq      
9.django\_rq\_dashboard       
10.django\_cors\_headers        
**注册功能使用了SendClound服务，请确保在本地邮件配置能使用。**    

====
