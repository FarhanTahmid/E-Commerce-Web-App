from django.db.models import Sum, Count, F, Window
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
import datetime
from .models import *


class SalesManagement:

    def get_sales_for_year(year=None):

        """
        Fetch total sales for a specific year or current year if none specified.
        
        Args:
            year (int, optional): The year to get sales for. Defaults to current year.
            
        Returns:
            dict: Contains the year and total sales amount
        """
        
        if year is None:
            year = timezone.now().year
            
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        
        yearly_sales = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date,
            order_status__in=['success','delivered','shipped','Shipped','Delivered','Success']  
        ).aggregate(
            total_sales=Sum('total_amount'),
            order_count=Count('order_id')
        )
        
        return {
            'year': year,
            'total_sales': yearly_sales['total_sales'] or 0,
            'order_count': yearly_sales['order_count'] or 0
        }
    
    def get_sales_for_month(year=None, month=None):
        """
        Fetch total sales for a specific month or current month if none specified.
        
        Args:
            year (int, optional): The year to get sales for. Defaults to current year.
            month (int, optional): The month to get sales for. Defaults to current month.
            
        Returns:
            dict: Contains the year, month and total sales amount
        """
        if year is None:
            year = timezone.now().year
        if month is None:
            month = timezone.now().month
            
        start_date = datetime.date(year, month, 1)
        
        # Calculate the last day of the month
        if month == 12:
            end_date = datetime.date(year, month, 31)
        else:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        
        monthly_sales = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date,
            order_status__in=['success','delivered','shipped','Shipped','Delivered','Success']
        ).aggregate(
            total_sales=Sum('total_amount'),
            order_count=Count('order_id')
        )
        
        return {
            'year': year,
            'month': month,
            'total_sales': monthly_sales['total_sales'] or 0,
            'order_count': monthly_sales['order_count'] or 0
        }
    
    def get_highest_selling_product(period_days=30):
        """
        Find the highest selling product based on quantity sold.
        
        Args:
            period_days (int, optional): Number of days to look back. Defaults to 30.
            
        Returns:
            dict: Information about the highest selling product
        """
        cutoff_date = timezone.now() - datetime.timedelta(days=period_days)
        
        # Get completed orders only
        completed_orders = Order.objects.filter(
            order_date__gte=cutoff_date,
            order_status__in=['success','delivered','shipped','Shipped','Delivered','Success']
        )
        
        # Get order IDs to filter order details
        order_ids = completed_orders.values_list('id', flat=True)
        
        # Find highest selling product by quantity
        top_products = OrderDetails.objects.filter(
            order_id__in=order_ids
        ).values(
            'product_sku',
            'product_sku__product_id__product_name' 
        ).annotate(
            total_quantity=Sum('quantity'),
            total_sales=Sum('subtotal')
        ).order_by('-total_quantity')[:5]  # Get top 5 for more context
        
        if not top_products:
            return {'message': 'No products sold in the specified period'}
        
        highest_selling = top_products[0]
        
        return {
            'period_days': period_days,
            'product_id': highest_selling['product_sku'],
            'product_name': highest_selling['product_sku__product__name'],
            'total_quantity_sold': highest_selling['total_quantity'],
            'total_sales_amount': highest_selling['total_sales'],
            'top_products': list(top_products)
        }
    
    def get_highest_selling_brand(period_days=30):
        """
        Find the highest selling brand based on total sales amount.
        
        Args:
            period_days (int, optional): Number of days to look back. Defaults to 30.
            
        Returns:
            dict: Information about the highest selling brand
        """
        cutoff_date = timezone.now() - datetime.timedelta(days=period_days)
        
        # Get completed orders only
        completed_orders = Order.objects.filter(
            order_date__gte=cutoff_date,
            order_status__in=['success','delivered','shipped','Shipped','Delivered','Success']
        )
        
        # Get order IDs to filter order details
        order_ids = completed_orders.values_list('id', flat=True)
        
        # Find highest selling brand
        # This assumes Product_SKU model has a relationship to a Brand model
        top_brands = OrderDetails.objects.filter(
            order_id__in=order_ids
        ).values(
            'product_sku__product_id__product_brand',  # Assuming there's a brand field or relation
            'product_sku__product_id__product_brand__brand_name'  # Assuming Brand has a name field
        ).annotate(
            total_sales=Sum('subtotal'),
            total_quantity=Sum('quantity'),
            order_count=Count('order_id', distinct=True)
        ).order_by('-total_sales')[:5]  # Get top 5 for more context
        
        if not top_brands:
            return {'message': 'No brands sold in the specified period'}
        
        highest_selling = top_brands[0]
        
        return {
            'period_days': period_days,
            'brand_id': highest_selling['product_sku__product__brand'],
            'brand_name': highest_selling['product_sku__product__brand__name'],
            'total_sales_amount': highest_selling['total_sales'],
            'total_quantity_sold': highest_selling['total_quantity'],
            'order_count': highest_selling['order_count'],
            'top_brands': list(top_brands)
        }
    
class OrderSummary:

    def get_orders_for_month(year=None, month=None, include_status=True):
        """
        Fetch orders for a specific month or current month if none specified.
        
        Args:
            year (int, optional): The year to get orders for. Defaults to current year.
            month (int, optional): The month to get orders for. Defaults to current month.
            include_status (bool, optional): Whether to include status breakdown. Defaults to True.
            Ststus as in further details
            
        Returns:
            dict: Contains the orders for the month with optional status breakdown
        """
        if year is None:
            year = timezone.now().year
        if month is None:
            month = timezone.now().month
            
        start_date = datetime.date(year, month, 1)
        
        # Calculate the last day of the month
        if month == 12:
            end_date = datetime.date(year, month, 31)
        else:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        
        orders = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date
        )
        
        result = {
            'year': year,
            'month': month,
            'order_count': orders.count(),
            'total_amount': orders.aggregate(total=Sum('total_amount'))['total'] or 0
        }
        
        if include_status:
            status_breakdown = orders.values('order_status').annotate(
                count=Count('order_id'),
                total=Sum('total_amount')
            )
            
            result['status_breakdown'] = {
                status['order_status']: {
                    'count': status['count'],
                    'total': status['total']
                } for status in status_breakdown
            }
            
        return result
    
    def get_orders_for_year(year=None, include_monthly_breakdown=True):
        """
        Fetch orders for a specific year or current year if none specified.
        
        Args:
            year (int, optional): The year to get orders for. Defaults to current year.
            include_monthly_breakdown (bool, optional): Whether to include monthly breakdown. Defaults to True.
            
        Returns:
            dict: Contains the orders for the year with optional monthly breakdown
        """
        if year is None:
            year = timezone.now().year
            
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        
        orders = Order.objects.filter(
            order_date__gte=start_date,
            order_date__lte=end_date
        )
        
        result = {
            'year': year,
            'order_count': orders.count(),
            'total_amount': orders.aggregate(total=Sum('total_amount'))['total'] or 0
        }
        
        if include_monthly_breakdown:
            monthly_breakdown = orders.annotate(
                month=TruncMonth('order_date')
            ).values('month').annotate(
                count=Count('order_id'),
                total=Sum('total_amount')
            ).order_by('month')
            
            result['monthly_breakdown'] = {
                item['month'].month: {
                    'count': item['count'],
                    'total': item['total']
                } for item in monthly_breakdown
            }
            
        return result
    

