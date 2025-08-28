from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date
from .forms import RecordForm
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now
from collections import defaultdict
from datetime import date
from django.db.models import Sum
from django.shortcuts import render
from .models import Record
from operator import attrgetter
from django.db.models.functions import ExtractYear
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
# Create your views here.
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm

@login_required
def record_list(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    records = Record.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    ).order_by('-date')

    # ✅ 統計總收入、總支出與結餘
    total_income = records.filter(record_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = records.filter(record_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # years = range(today.year - 3, today.year + 1)
    available_years = (
        Record.objects.filter(user=request.user)
        .annotate(year=ExtractYear('date'))
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')  # 可選：年份由新到舊
    )
    months = range(1, 13)

    return render(request, 'spend_record/records.html', {
        'records': records,
        'selected_year': year,
        'selected_month': month,
        # 'years': years,
        'years': available_years,
        'months': months,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    })

# def record_list(request):
#     today = date.today()
#     year = int(request.GET.get('year', today.year))
#     month = int(request.GET.get('month', today.month))

#     records = Record.objects.filter(
#         user=request.user,
#         date__year=year,
#         date__month=month
#     ).order_by('-date')

#     years = range(today.year - 3, today.year + 1)
#     months = range(1, 13)
#     return render(request, 'spend_record/records.html', {
#         'records': records,
#         'selected_year': year,
#         'selected_month': month,
#         'years': years,
#         'months': months
#     })

@login_required
def add_record(request):
    form = RecordForm(request.POST or None)
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    # form.fields['category'].queryset = Category.objects.all()
    if form.is_valid():
        record = form.save(commit=False)
        record.user = request.user
        record.save()
        return redirect('record_list')

    return render(request, 'spend_record/add_record.html', {'form': form})

@login_required
def category_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name, user=request.user)
            # Category.objects.create(name=name)
            messages.success(request, '分類新增成功')
            return redirect('category_list')
        else:
            messages.error(request, '請輸入分類名稱')
    categories = Category.objects.filter(user=request.user)
    # categories = Category.objects.all()  # 假設所有分類都可以被查看
    return render(request, 'spend_record/category_list.html', {'categories': categories})

# @login_required
# def category_add(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         if name:
#             Category.objects.create(name=name, user=request.user)
#             messages.success(request, '分類新增成功')
#             return redirect('category_list')
#         else:
#             messages.error(request, '請輸入分類名稱')
#     return render(request, 'spend_record/category_add.html')

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    # category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('category_list')


@login_required
def edit_record(request, pk):
    record = get_object_or_404(Record, pk=pk, user=request.user)
    # record = get_object_or_404(Record, pk=pk)
    form = RecordForm(request.POST or None, instance=record)
    date_str = record.date.strftime('%Y/%m/%d')
    # form.fields['date'].queryset = date_str
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    # form.fields['category'].queryset = Category.objects.all()
    if form.is_valid():
        form.save()
        return redirect('record_list')
    return render(request, 'spend_record/add_record.html', {'form': form, 'edit': True})

@login_required
def delete_record(request, pk):
    record = get_object_or_404(Record, pk=pk, user=request.user)
    # record = get_object_or_404(Record, pk=pk)
    record.delete()
    return redirect('record_list')

@login_required
def analysis(request):
    user = request.user
    today = date.today()
    year_start = date(today.year, 1, 1)

    # ⏳ 篩選時間區間
    # start_date = request.GET.get("start_date", year_start.strftime("%Y-%m-%d"))
    # end_date = request.GET.get("end_date", today.strftime("%Y-%m-%d"))
    start_date = request.POST.get("start_date", year_start.strftime("%Y-%m-%d"))
    end_date = request.POST.get("end_date", today.strftime("%Y-%m-%d"))
    records = Record.objects.filter(
        user=user,
        date__range=[start_date, end_date]
    )

    income_records = records.filter(record_type='income')
    expense_records = records.filter(record_type='expense')

    total_income = income_records.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expense_records.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # 📊 Pie Chart: 分類支出比例
    category_sums = expense_records.values('category__name').annotate(total=Sum('amount'))
    pie_labels = [item['category__name'] or '未分類' for item in category_sums]
    pie_data = [float(item['total']) for item in category_sums]

    # 📈 Bar Chart: 月收入與支出比較
    month_income = [0]*12
    month_expense = [0]*12
    for record in records:
        month = record.date.month - 1
        if record.record_type == 'income':
            month_income[month] += float(record.amount)
        else:
            month_expense[month] += float(record.amount)
    month_labels = [f"{i+1}月" for i in range(12)]
    monthly_balance = [inc - exp for inc, exp in zip(month_income, month_expense)]
    # 🧾 分類花費明細
    breakdown = defaultdict(list)
    for record in expense_records:
        key = record.category.name if record.category else '未分類'
        breakdown[key].append(record)

    # ✨ 每個細項根據日期排序（由新到舊）
    category_breakdown = []
    for key, records in breakdown.items():
        sorted_records = sorted(records, key=attrgetter('date'), reverse=True)  # reverse=True 表示新到舊
        total = sum(r.amount for r in sorted_records)
        category_breakdown.append((key, total, sorted_records))
    # breakdown = defaultdict(list)
    # for record in expense_records:
    #     key = record.category.name if record.category else '未分類'
    #     breakdown[key].append(record)

    # category_breakdown = [(key, sum(r.amount for r in val), val) for key, val in breakdown.items()]

    # ✅ 新增：付款方式總覽（消費方式 → 總金額 + 細項）
    payment_breakdown = []
    payment_dict = defaultdict(list)
    for r in expense_records:
        key = r.get_payment_method_display()  # 顯示中文名稱
        payment_dict[key].append(r)

    for method, records in payment_dict.items():
        sorted_records = sorted(records, key=attrgetter('date'), reverse=True)
        total = sum(r.amount for r in sorted_records)
        payment_breakdown.append((method, total, sorted_records))

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'month_labels': month_labels,
        'month_income': month_income,
        'month_expense': month_expense,
        'monthly_balance': monthly_balance,
        'category_breakdown': category_breakdown,
        'payment_breakdown': payment_breakdown,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'spend_record/analysis.html', context)