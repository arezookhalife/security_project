from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import DetailView
from .forms import ProductForm
import logging

logger = logging.getLogger(__name__)


@login_required
@permission_required('shop.can_edit_product', raise_exception=True)
def edit_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_detail', pk=product.id)
        else:
            form = ProductForm(instance=product)

        return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

    except Exception as e:
            logger.error(f"❌ خطا در ویرایش محصول {product_id}: {e}")
            return render(request, "error.html", {"error": "خطای غیرمنتظره‌ای رخ داد"})


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    permission_required = 'shop.can_view_product'

