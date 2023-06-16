from django.shortcuts import render,redirect
from django.http import HttpResponse ,HttpResponseRedirect
from project.models import *
from user_profile.models import *
from home.views import *
import datetime

# Create your views here.



### create project ###
#add
def createProject(req):
    if('username' in req.session):
        context={}
        allCategory=Category.objects.all()
        context['allCategory']=allCategory
        
        if(req.method=='POST'):
            ####### search bar 
            if 'search' in req.POST:
                    if req.POST['search']:
                        search_result = searchBar(req)
                        context = {}
                        context['search_result'] = search_result
                        return render(req,'home/search.html',context)
        ############################################
            myCategory = Category.objects.get(name=req.POST['get_category'])
            myEmail = MyUser.objects.get(id=req.session['user_id'])
            startDateObj = datetime.datetime.strptime(req.POST['start_date'], '%Y-%m-%d')
            endDateObj = datetime.datetime.strptime(req.POST['end_date'], '%Y-%m-%d')
            if endDateObj < startDateObj:
                context['end_err_msg']="End date must be after start date. Please enter a valid end date."
                return render(req,'createProject.html',context)
            new_proj = Projects.objects.create(title=req.POST['title'],details=req.POST['details'],category=myCategory,target=req.POST['target'],start_date=req.POST['start_date'],end_date=req.POST['end_date'],owner_id=myEmail,report_count=1)
            # new_proj = Projects.objects.get(title=req.POST['title'])
            # for image in req.FILES.getlist('image'):
            # print(req.FILES['image'])
            if 'tag' in req.POST:
                Tag.objects.create(project=new_proj,tag_name = req.POST['tag'].lower())
            if 'image' in req.FILES:
                for image in req.FILES.getlist('image'):
            # print(req.FILES['image'])
                    Image.objects.create(project=new_proj,picture = image)
            return HttpResponseRedirect('/user')
        return render(req,'createProject.html',context)
    else:
        return redirect("/Registeration")
        


def get_similar_project(id):
    # Get the tags of the project with the given ID.
    proj_tags = Tag.objects.filter(project=id).values_list('tag_name', flat=True)

    # Get other projects that have tags similar to the current project.
    sim_projs = Tag.objects.filter(tag_name__in=proj_tags).exclude(project=id).values_list('project', flat=True)

    # Get four random projects from the similar projects.
    random_proj = Projects.objects.filter(id__in=sim_projs).order_by('?')[:4]

    # context = {}
    return random_proj
    # return render(req, 'display_proj.html', context)

def image_slider(id):
    # context = {}
    images = Image.objects.filter(project=id)
    # context['images'] = images
    for im in images:
        print(im)
    return images

    # <div class="container bg-secondary">
    #   <h1>this is header</h1>
    #   {%for image in images%}
    #   <img src="{{image.picture.url}}">
    #   {%endfor%}
    # </div>


#### display project
def displayProject(req,id):
    if('username' in req.session):
        # req.session.clear()
        context={}
    ######## set the data into context to send it for display page
        
        ####### search bar 
        if 'search' in req.POST:
                if req.POST['search']:
                    search_result = searchBar(req)
                    context = {}
                    context['search_result'] = search_result
                    return render(req,'home/search.html',context)
        ############################################

        similar_projects = get_similar_project(id)
        getProject = Projects.objects.get(id=id)
        images = image_slider(id)
        getComment = Comment.objects.filter(project=id)
        getDonation= Donation.objects.filter(project=id)
        getOwnerProject=MyUser.objects.get(id=getProject.owner_id.id)  
        context['images']= images
        context['setProject']=getProject
        context['setComment']=getComment
        context['setOwnerProject']=getOwnerProject
        context['similar_projects'] = similar_projects

        sumDonate= 0
    ####################################################################
        
        ####### get all donate for 1 project
        for donate in getDonation:
            sumDonate+=donate.donate_amount
        context['setDonation']=sumDonate
        ###################################
        getUserID = MyUser.objects.get(email=getOwnerProject.email)

        ### check if this user had report project before or not 
        check_if_user_did_report=Report.objects.filter(project=id,user_id=getUserID)
        if(check_if_user_did_report):
           context['reportState']='done'
        ###################################

        ###### check if user rate the project before 
        check_if_user_did_rate=Rating.objects.filter(project=id,user_id=getUserID)
        print(check_if_user_did_rate)
        if(check_if_user_did_rate):
            context['rateState']='done'
        ############################################
        if(req.method=='POST'):
            ########## get report project from user            
            if('report' in req.POST):
                Report.objects.create(project=getProject,user_id=getUserID,report_state=req.POST['report'])

                
                return HttpResponseRedirect('/project/display/{}'.format(int(id)))
            
            ########## get report from user            
            if('reportComment' in req.POST):
                # commentUserID = MyUser.objects.get(email=req.POST['reportCommentUser'])
                Comment.objects.filter(project=getProject,user_id=req.POST['reportCommentUser']).update(report_comment=True)

                #project=projectID,user_id=userID,comment_body=req.POST['commentUser']
                return HttpResponseRedirect('/project/display/{}'.format(int(id)))
            
            ###### get donate from user
            if('donateUser' in req.POST):
                projectID=Projects.objects.get(id=id)
            # myCategory = Category.objects.get(name='help')
                userID = MyUser.objects.get(email=req.session['user_email'])
                if(req.POST['donateUser']):  ####### check donate not empty
                    Donation.objects.create(project=projectID,user_id=userID,donate_amount=req.POST['donateUser'])
                return HttpResponseRedirect('/project/display/{}'.format(int(id)))
            #############################

        
            ###### get Rate from user
            if('rateValue' in req.POST):
                
            # myCategory = Category.objects.get(name='help')
                userID = MyUser.objects.get(email=req.session['user_email'])
                print(userID)
                if(req.POST['rateValue']):  ####### check donate not empty
                    Rating.objects.create(project=getProject,user_id=getUserID,rate=req.POST['rateValue'])

                return HttpResponseRedirect('/project/display/{}'.format(int(id)))
            #############################
            ##### get comment from user
            if('commentUser' in req.POST):
                projectID=Projects.objects.get(id=id)
                userID = MyUser.objects.get(email=req.session['user_email'])
                if(req.POST['commentUser']): ####### check comment not empty
                    Comment.objects.create(project=projectID,user_id=userID,comment_body=req.POST['commentUser'])
            #############################        
                return HttpResponseRedirect('/project/display/{}'.format(int(id)))
        
        ########### check if u are owner of project or just user
        if(getOwnerProject.email==req.session['user_email']):
            project = Projects.objects.get(id=id)
            ############check if total donta more tha25% from target or can delete
            total_donations = Donation.objects.filter(project=id).aggregate(Sum('donate_amount'))['donate_amount__sum'] or 0
            deleteProject = True if total_donations > 0.25 * project.target else False
            context['deleteProject']=deleteProject
            return render(req,'displayprojectOwner.html',context)
        else:
            return render(req,'displayprojectUser.html',context)
        #######################################################
    else:
        return redirect("/Registeration")
        
              
def deleteProject(req,ID):
    if('username' in req.session):
        Projects.objects.filter(id=ID).delete()
        return HttpResponseRedirect('/')
    else:
         return HttpResponseRedirect('/Registeration')
    
def listAllProject(req):
    if('username' in req.session):
        if 'search' in req.POST:
                if req.POST['search']:
                    search_result = searchBar(req)
                    context = {}
                    context['search_result'] = search_result
                    return render(req,'home/search.html',context)
        context={}
        allProject=Projects.objects.all()
        context['allProject']=allProject
        return render(req,'projectContainer.html',context)
    else:
        return HttpResponseRedirect('/Registeration')
