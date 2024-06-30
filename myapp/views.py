from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import PurchaseRequest, Quotation, PurchaseOrder

from django.shortcuts import render, redirect, get_object_or_404

from .forms import PurchaseRequestForm, QuotationForm, PurchaseOrderForm,LoginForm

from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')  # Use named URL patterns

def user_logout_view(request):
    logout(request)
    return redirect('login')  # Use named URL patterns

@login_required(login_url="/login")
def index(request):

    return render(request, 'pages/index.html')


# Create a new purchase request
def create_purchase_request(request):
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST)
        if form.is_valid():
            purchase_request = form.save(commit=False)
            purchase_request.user = request.user
            purchase_request.save()
            return redirect('purchase_request_detail', pk=purchase_request.pk)
    else:
        form = PurchaseRequestForm()
    return render(request, 'pages/purchase_request/create.html', {'form': form})

# View details of a purchase request
def purchase_request_detail(request, pk):
    purchase_request = get_object_or_404(PurchaseRequest, pk=pk)
    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST, request.FILES)
        if quotation_form.is_valid():
            quotation = quotation_form.save(commit=False)
            quotation.purchase_request = purchase_request
            quotation.save()
            return redirect('purchase_request_detail', pk=purchase_request.pk)
    else:
        quotation_form = QuotationForm()
    return render(request, 'purchase_request_detail.html', {
        'purchase_request': purchase_request,
        'quotation_form': quotation_form,
    })

# Update a purchase request
def update_purchase_request(request, pk):
    purchase_request = get_object_or_404(PurchaseRequest, pk=pk)
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST, instance=purchase_request)
        if form.is_valid():
            form.save()
            return redirect('purchase_request_detail', pk=purchase_request.pk)
    else:
        form = PurchaseRequestForm(instance=purchase_request)
    return render(request, 'purchase_request_form.html', {'form': form})

# Delete a purchase request
def delete_purchase_request(request, pk):
    purchase_request = get_object_or_404(PurchaseRequest, pk=pk)
    if request.method == 'POST':
        purchase_request.delete()
        return redirect('user_purchase_requests')
    return render(request, 'delete_confirm.html', {'object': purchase_request})

# List of pending purchase requests for admin
def admin_pending_requests(request):
    pending_requests = PurchaseRequest.objects.filter(status='Pending')
    return render(request, 'pages/admin/admin_pending_requests.html', {'pending_requests': pending_requests})

# Review and manage purchase requests
def review_purchase_request(request, pk):
    purchase_request = get_object_or_404(PurchaseRequest, pk=pk)
    if request.method == 'POST':
        if 'approve' in request.POST:
            purchase_request.status = 'Approved'
            purchase_request.save()
            PurchaseOrder.objects.create(
                purchase_request=purchase_request,
                supplier_name=purchase_request.quotations.first().supplier_name,
                product_name=purchase_request.product_name,
                quantity=purchase_request.quantity,
                price=purchase_request.quotations.first().price
            )
        elif 'decline' in request.POST:
            purchase_request.status = 'Declined'
            purchase_request.save()
        return redirect('pending_requests')
    return render(request, 'pages/admin/review_purchase_request.html', {'purchase_request': purchase_request})

# View, update, and delete purchase orders
def purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all()
    return render(request, 'pages/purchase_order/index.html', {'purchase_orders': purchase_orders})

def purchase_order_detail(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'pages/purchase_order/purchase_order_detail.html', {'purchase_order': purchase_order})

def update_purchase_order(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        if form.is_valid():
            form.save()
            return redirect('pages/purchase_order/purchase_order_detail', pk=purchase_order.pk)
    else:
        form = PurchaseOrderForm(instance=purchase_order)
    return render(request, 'pages/purchase_order/create.html', {'form': form})

def delete_purchase_order(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        purchase_order.delete()
        return redirect('purchase_order_list')
    return render(request, 'delete_confirm.html', {'object': purchase_order})

# List of all purchase requests for a user
def user_purchase_requests(request):
    purchase_requests = PurchaseRequest.objects.filter(user=request.user)
    return render(request, 'pages/purchase_request/index.html', {'purchase_requests': purchase_requests})
