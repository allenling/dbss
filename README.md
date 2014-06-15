dbss
====
Whysos.info source    
环境: Centos6.4+uwsgi+nginx+django-1.5.4    
**设计在wiki有说明**    
=====
### 本地配置
需要在本地建立local_settings.py来配置本地的一些内容，内容见settings.py     

====
### 关于第三方库        
1.django-avatar的修改在fork的版本里面    
2.django-ckeditor是用的django-captcha是使用django-ckeditor-updated-4.2.7版本，修改的内容只限于ckeditor的静态文件 可以直接使用static里面的ckeditor。如果你想使用galleriffic， 有个小小的bug，内容见[小bug](https://github.com/shaunsephton/django-ckeditor/issues/106)      
3.daemonize的修改见fork版本，或者直接使用当前目录下的daemonize.py文件     
4.django-simple-captcha在使用FormWizard的时候有个二次验证的问题，详情见[地址](http://blog.csdn.net/a_9884108/article/details/18795249)，github上的讨论[github](https://github.com/mbi/django-simple-captcha/issues/6)

====
#### wiki历史     
**2014.6.13 加入更新索引策略说明**      
**2014.6.15 加入计算方法设计说明**     
