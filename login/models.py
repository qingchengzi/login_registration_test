from django.db import models

# Create your models here.

class User(models.Model):

    gender = (
        ('male','男'),
        ('female','女'),
    )

    name          = models.CharField(max_length=128,unique=True,verbose_name='用户名') #unique=True唯一数，这里表示用户名必须唯一;
    password      = models.CharField(max_length=256,verbose_name='密码')
    email         = models.EmailField(unique=True,verbose_name='邮箱')   #邮箱也必须唯一
    sex           = models.CharField(choices=gender,max_length=32,default='男',verbose_name='用户名') #单选框,定义了gender元组,默认为男
    c_time        = models.DateTimeField(auto_now_add=True,verbose_name='创建时间') #用户创建时间，auto_now_add=True表示自动添加当前时间为创建时间
    has_confirmed = models.BooleanField(default=False,verbose_name='邮箱是否验证') #邮箱注册确认字段

    def __str__(self):     #更清晰更直观的显示用户对象的信息
        return self.name   #显示的时候就会显示用户名的名字，而不是无法理解的对象内存地址

    class  Meta:
        ordering            = ['-c_time']  #按照创建时间排序，那个用户先创建就按照就排在前面
        verbose_name        = '用户' #直观显示的名字
        verbose_name_plural = '用户' #复数形式，中文无所谓，英文才区分和verbose_name一样就可以了


class ConfirmString(models.Model):
    code   = models.CharField(max_length=256,verbose_name='注册码')
    user   = models.OneToOneField('User',verbose_name='关联的用户')  #一对一关系，一个用户有一个对应的验证码
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    def __str__(self):
        return self.user.name + ": "+ self.code

    class Meta:
        ordering  = ['-c_time']
        verbose_name        = '确认码'
        verbose_name_plural = '确认码'


