from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
import datetime
import json
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.

def index(request):
    user=User.objects.get(username=request.user.username)
    if request.user.is_authenticated:
        print("user loggedin")
        print(request.method)
        if  request.method == "POST":
            Date=request.POST.get('date',False)
            if 'expense' in request.POST:
                print("inside expense")
                text=str(request.POST['TypeofExpense'])
                amount=int(request.POST['AmountSpent'])
                expense=Expense(TypeoOfExpense=text, MoneySpent=amount,Date=Date,SpentBy=request.user)
                expense.save()
            elif 'Income' in request.POST:
                text=request.POST['TypeofIncome']
                amount=int(request.POST['AmountEarned'])
                income=Income(TypeoOfIncome=text, MoneyEarned=amount,Date=Date,EarnedBy=request.user)
                income.save()
            return HttpResponseRedirect(reverse('details'))
        
        else:
            return render(request,"index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

# helps to view our incomes and expenses date wise 
def details_tab(request):
    expenses=Expense.objects.filter(SpentBy=request.user).order_by('Date')[::-1]
    incomes=Income.objects.filter(EarnedBy=request.user).order_by('Date')[::-1]
    l={}
    # l is dictionary l={date:[{expense on that day}],...}
    #expense  
    for expense in expenses:
        if expense.Date not in l.keys():
            v=[]
            v.append({ "amountspent":expense.MoneySpent, "spenttype":expense.TypeoOfExpense })
            l[expense.Date]=v
        else:
            v=[]
            v.append({"amount":expense.MoneySpent, "type":expense.TypeoOfExpense})
            l[expense.Date]=l[expense.Date]+v
    #income
    g={}
    # g is dictionary g={date:[{income on that day}],...}
    for income in incomes:
        if income.Date not in g.keys():
            v=[]
            v.append({ "amountEarned":income.MoneyEarned, "Earnedtype":income.TypeoOfIncome})
            g[income.Date]=v
        else:
            v=[]
            v.append({ "amountEarned":income.MoneyEarned, "Earnedtype":income.TypeoOfIncome })
            g[income.Date]=g[income.Date]+v
    
    
    #SumIncomeExpenseInADay : list [ date, expense on that date, [ income on that date]
    SumIncomeExpenseInADay=[]

    for i in l:
        exp=Expense.objects.filter(SpentBy=request.user).filter(Date=i)
        ex=0
        for e in exp:
            ex=ex+e.MoneySpent
        f=[]
        f=[ i, ex, 0]
        SumIncomeExpenseInADay.append(f)

    #money earned
    for i in g:
        inc=Income.objects.filter(EarnedBy=request.user).filter(Date=i)
        incr=0
        for j in inc:
            incr+=j.MoneyEarned
        flag=0
        for date,expense,income in SumIncomeExpenseInADay:
            if date == i:
                index=SumIncomeExpenseInADay.index([date,expense,income])
                SumIncomeExpenseInADay[index][-1]=incr
                print(SumIncomeExpenseInADay)
                flag=1
                break
        if flag==0:
            f=[]
            f=[ i,0, incr]
            SumIncomeExpenseInADay.append(f)
            
    
    return render(request,"details.html",{"l":l,"g":g,"total":SumIncomeExpenseInADay})

    

def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("details"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
    
#diagramatic representation of data
def piechart(request,date,totalIncome,totalExpense):
    year=int(date[0:4])
    month=int(date[5:7])
    day=int(date[8:])
    date_object = datetime.date(year,month,day)

    incomes=Income.objects.filter(EarnedBy=request.user).filter(Date=date_object)
    expenses=Expense.objects.filter(SpentBy=request.user).filter(Date=date_object)
    Income_labels,Income_data,Expense_labels,Expense_data = [],[],[],[]
    
    for income in incomes:
        Income_labels.append(income.TypeoOfIncome)
        Income_data.append(income.MoneyEarned)
    for exxpense in expenses:
        Expense_labels.append(income.TypeoOfIncome)
        Expense_data.append(income.MoneyEarned)
    
    piecharts={'Income_data':Income_data,
                'Income_labels':Income_labels,
                "Expense_data":Expense_data,
                "Expense_labels":Expense_labels,
                "date":date,
                "total_data":[totalIncome,totalExpense],
                "total_labels":["TotalIncome","TotalExpense"]}

    return render(request, 'pie_chart.html', piecharts)

