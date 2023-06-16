from django.shortcuts import render , redirect
from django.http import HttpResponse ,HttpResponseRedirect
from project.models import *
from user_profile.models import *
from django.db.models import Sum
from django.db.models import Q
import re
from django.contrib.auth import login,authenticate,logout

# Create your views here.
def myHome(req):
    if( 'username' in req.session):
        top_rated_projects = top_rated_project(req)
        latest_projects = latest_project(req)
        
        myCategory=allCategory(req)
        admin_projects_selected = admin_projects(req)
        
        if req.method=='POST':
            if 'search' in req.POST:
                if req.POST['search']:
                    search_result = searchBar(req)
                    context = {}
                    context['search_result'] = search_result
                    return render(req,'home/search.html',context)
        
        context={}
        context['allCategory']=myCategory
        context['top_rated_projects'] = top_rated_projects
        context['latest_projects'] = latest_projects
        context['admin_projects_selected'] = admin_projects_selected

        return render(req,'home.html',context)
    else:
        return redirect("/Registeration")


def getCategory(req,cate):
        if( 'username' in req.session):
            if 'search' in req.POST:
                if req.POST['search']:
                    search_result = searchBar(req)
                    context = {}
                    context['search_result'] = search_result
                    return render(req,'home/search.html',context)
            context={}
            req.session['categoryN']=cate
            context['category']=Category.objects.filter(name=cate)
            context['projects']=Projects.objects.filter(category=cate)
            
            return render(req,'category.html',context)
        else:
            return redirect("/Registeration")

def allCategory(req):
      context={}
      all_category=Category.objects.all()
      return all_category
    

def admin_projects(req):
    admin_selected = Adminproject.objects.all()[:5]
    proj_list = []
    for obj in admin_selected:
        proj = Projects.objects.get(id=obj.id)
        proj_list.append(proj)
    return proj_list


def top_rated_project(req):
    top_rated_projects = Projects.objects.order_by('-total_rate')[:5]
    return  top_rated_projects

def latest_project(req):
    latest_projects = Projects.objects.order_by('-created_at')[:5]
    return latest_projects


def check_donation_percentage(id):
    project = Projects.objects.get(id=id)
    total_donations = Donation.objects.filter(project=id).aggregate(Sum('donate_amount'))['donate_amount__sum'] or 0
    return True if total_donations < 0.25 * project.target else False



def get_projects_with_donations(owner_id):
    projects = Projects.objects.filter(owner_id=owner_id)
    result = []
    for project in projects:
        total_donations = Donation.objects.filter(project=project.id).aggregate(Sum('donate_amount'))['donate_amount__sum'] or 0
        project_dict = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'target': project.target,
            'total_donations': total_donations,
        }
        result.append(project_dict)
    return result



def searchBar(request):

    search_word = request.POST['search']
    tag_data = Tag.objects.filter(tag_name__icontains=search_word)
    project_data = Projects.objects.filter(Q(title__icontains=search_word) | Q(tag__in=tag_data)).distinct()
    return project_data


def Registeration(req):
    if( 'username' not in req.session):
        context = {}
        
        if req.method == "POST":
            
            first_name = req.POST["first_name"]
            last_name = req.POST["last_name"]
            email = req.POST["email"]
            if not re.match("[^@]+@[^@]+\.[^@]+", email):
                context['email_valid_err_msg']="not a valid email."
            check_email= MyUser.objects.filter(email=email).exists()
            if check_email:
                context['email_err_msg']="email already in usage"
                # return HttpResponseRedirect("/Registeration",context)
            password = req.POST["password"]
            cpassword = req.POST["cpassword"]
            if password != cpassword:
                context['pass_err_msg']="Password and Confirm Password don't match"
            phone = req.POST["phone"]
            if not re.match("^01[0125][0-9]{8}$", phone):
                context['phone_err_msg'] = "Invalid phone number. Please enter a valid egyptian phone number"
            image = req.FILES["image"]
            if context == {}:
                MyUser.objects.create(
                    first_name=first_name,last_name=last_name, password=password, email=email,phone_number=phone,image=image
                )
                return HttpResponseRedirect("/Login")
            
                # return HttpResponseRedirect("/Registeration",context)
        return render(req, "register.html", context)

    else:
        return redirect("/")
    

def Login(req):
    if( 'username' not in req.session):
        context = {}
        if req.method == "POST":
            myuser = MyUser.objects.filter(
                email=req.POST["email"], password=req.POST["password"]
            )

            if len(myuser) != 0:
                req.session["username"] = myuser[0].first_name
                req.session["user_id"] = myuser[0].id
                req.session["user_email"] = myuser[0].email
                # userobj = authenticate(email=req.POST['email'],password=req.POST['password'])
                # userobj2 = authenticate(username='admin',password=123)
                # print(userobj)
                # print(userobj2)
                # # if userobj is not None:
                # #     login(req,userobj)
                # #     return HttpResponseRedirect("/admin")
                    
                # # else :    
                return HttpResponseRedirect("/")
            else:
                if MyUser.objects.filter(email = req.POST['email']):
                    context["pass_err_msg"] = "Wrong Password"
                else:
                    context['email_err_msg'] = "Wrong Email"
        return render(req, "login.html", context=context)
    else:
        return redirect("/")

def Logout(req):
    logout(req)
    return redirect("/Registeration")
