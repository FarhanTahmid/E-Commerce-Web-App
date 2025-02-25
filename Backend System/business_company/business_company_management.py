from business_company.models import Business_Identity


class Buisiness_Handling:
    
    def create_business(**kwargs):
        """Creates a new business."""
        # function returns messages and the function status.
        
        if(Business_Identity.objects.exists()):
            message="A business already exists!"
            func_status=False
            return message,func_status
        else: 
            new_business=Business_Identity.objects.create(
                platform_product_key=kwargs['product_key'],
                business_name=kwargs['business_name'],
                business_logo=kwargs['business_logo'],
                business_description=kwargs['business_description']
            )
            new_business.save()
            message="New business created!"
            func_status=True
            return message,func_status
        
            
            