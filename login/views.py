from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives

from . import models
from . import forms
# Create your views here.
import hashlib
import datetime

from mysite import settings

def hash_code(s,salt='mysite'):
    h = hashlib.md5(salt.encode('utf-8'))
    h.update(s.encode("utf-8"))
    return h.hexdigest()

def make_confirm_string(user): #生成验证码，user指接收那个用户的,将生成的数据注册码保存到数据库，且返回
    now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name,now) #将用户名和当前时间传入到hash_code中进行MD5加密
    models.ConfirmString.objects.create(code=code,user=user) #将随机生成的MD5和用户名保存到ConfirmString数据表中

    return code  #返回注册码


def send_email(email,code):
    subject, from_email, to = '来自www.liujiangblog.com的注册文件', 'xxx@sina.com', 'xxx@qq.com'
    text_content = '感谢注册www.tiantain.com，专注于Python和Django技术的分享！'
    html_content = '''
                   <p>感谢您注册<a href="http://{0}/confirm/?code={1}" target=blank>www.liujiangblog.com</a></p>
                   <p>请点击链接完成注册确认!</p>
                   <p>此链接有效期为{2}天！</p>
                   '''.format('127.0.0.1:8000',code,settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def index(request):
    pass
    return render(request,'login/index.html')


def login_old(request):
    '''这是原始的验证方法，已经被下面的login替代了'''
    if request.method=="POST":
        login_form = forms.UserForm(request.POST)
        useranme = request.POST.get('username',None)
        password = request.POST.get('password',None)
        message  = '所有的字段都必须填写'
        if useranme and password:
            useranme = useranme.strip()  #用户名两边去除空
            try:
                user = models.User.objects.get(name=useranme)
            except:
                message = "用户不存在"
                return render(request,'login/login.html',{'message':message})
            if user.password ==password:
                return redirect('/index/')
            else:
                message = '密码错误'
                return render(request,'login/login.html',{'message':message})
        else:
            return render(request,'login/login.html',{'message':message})
    return render(request,'login/login.html')


def login(request):
    '''
    #django提供了，在当前环境下面返回的所有局部变量函数locals(),好处就是自己可以不用构造字典，坏处就是会向模板穿多余的变量导致模板中变量冗余，降低效率
    #locals()里面会自动将login_form传入到模板中，在模板html中直接使用login_form变量名
    :param request:
    :return:
    '''
    if request.session.get('is_login',None): #如果已经登录，就不能重复登录了，跳转到/index/页面
        return redirect('/index/')

    if request.method =="POST":
        login_form = forms.UserForm(request.POST)
        message = '所有的字段都必须填写'
        if login_form.is_valid(): #是否合法判断
            username = login_form.cleaned_data.get('username') #login_form中会生成cleaned_data的字典
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message ='用户不存在'
                return render(request,'login/login.html',locals()) #django提供了，在当前环境下面返回的所有局部变量函数locals(),好处就是自己可以不用构造字典，坏处就是会向模板穿多余的变量导致模板中变量冗余，降低效率

            if not user.has_confirmed: #用户未进行邮箱确认
                message = '该用户还未通过邮件确认，不能登录'
                return  render(request,'login/login.html',locals())

            if user.password == hash_code(password): #密文密码对比
                request.session['is_login']= True   #登录成功后写入session数据
                request.session['user_id'] = user.id#向session会话中写入数据，根据自己需求写入,字典格式可以自定义任何数据
                request.session['user_name']=user.name
                return redirect('/index/')
            else:
                message = '密码错误'
                return render(request,'login/login.html',locals())
        else:
            return render(request,'login/login.html',locals())
    login_form = forms.UserForm() #如果不是post就不用提供参数，构造一个空表单
    return render(request,'login/login.html',locals())


def register(request):
    if request.session.get('is_login',None):#如果当前用户已经登录了，就
        # 不允许注册
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST) #生成表单，把request.POST作为参数提供
        message = '请检查填写的内容!'
        if register_form.is_valid():
            username  = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email     = register_form.cleaned_data['email']
            sex       = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不相同'
                return render(request,'login/register.html',locals())
            else:
                # same_name_user = models.User.objects.get(name=username) #get()方法如果没有找到或者找到两个以上就会报错,zh，需要使用try except抓取异常,如果不想用try except抓取异常就使用filter
                same_name_user   = models.User.objects.filter(name=username)#filter不存在就返回空列表，不会报错
                if same_name_user:
                    message = '用户名已经存在，请重新选择'
                    return render(request,'login/register.html',locals())
                same_email_user = models.User.objects.filter(email=email) #判断邮箱是否已经注册
                if same_email_user:
                    message = '该邮箱地址已经被注册，请使用别的邮箱！'
                    return render(request,'login/register.html',locals())
            #保存注册用户信息到数据库中
            new_user = models.User.objects.create()
            new_user.name     = username
            new_user.password = hash_code(password2)
            new_user.email    = email
            new_user.sex      = sex
            new_user.save()

            code       = make_confirm_string(new_user) #根据新用户生成验证码
            send_email(email,code) #将随机生成的验证码通邮箱发送给用户

            message ='请前往注册邮箱，进行确认!'
            return render(request,'login/confirm.html',locals()) #注册完毕后，跳转到登录页面


    register_form = forms.RegisterForm() #渲染出注册表单
    return render(request,'login/register.html',locals())


def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/') #如果没有登录状态，就没有登出的概念
    request.session.flush() #清除当前用户的使用session，会清除当前用户的所有session
    return redirect('/index/') #退出就返回主页


def user_confirm(request): #用户的通过邮箱进行验证注册
    code    = request.GET.get('code',None)
    message = ''
    try:
        confirm =  models.ConfirmString.objects.get(code=code) #获取确认码表中，是否有这个验证码
    except:
        message = '无效的请求'
        return render(request,'login/confirm.html',locals())

    c_time =  confirm.c_time   #获取生成确认码时的时间
    now    =  datetime.datetime.now() #获取当前时间
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):#创建时间加上7天，当前时间now已经超过了
        confirm.user.delete() #将确认码关联的数据删除，以为确认码已经失效
        message = "您的邮件已经过期！请重新注册"
        return render(request,'login/confirm.html',locals())
    else:
        confirm.user.has_confirmed = True #如果在7天内，就把数据表中的has_confirmed改为True
        confirm.user.save() #保存用户
        confirm.delete() #确认码，已经确认了就需要删除
        message  = '感谢确认，请使用账户登录!'
        return render(request,'login/confirm.html',locals())
