from .models import *
from system.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError

class ManageProducts:
    # Manage Product Types
    
    def fetch_all_product_types():
        """
        Retrieve all product types from the database with detailed exception handling.

        This function fetches all records from the `Product_type` model and returns them as a queryset.
        It includes comprehensive exception handling to manage various types of errors that may occur during the query.

        Returns:
            tuple:
                - QuerySet or None: A queryset containing all `Product_type` records if successful,
                or `None` if an error occurs.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            product_types, message = fetch_all_product_types()
            if product_types:
                print(message)
                for product in product_types:
                    print(f"ID: {product.pk}, Type: {product.type}, Description: {product.description}")
            else:
                print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues and logs the error.
                Example: Issues with the database engine or query execution.
                Message: "An unexpected error in Database occurred! Please try again later."
            - **OperationalError**: Handles server-related errors such as connection issues or timeouts.
                Message: "An unexpected error in server occurred! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries or schema mismatches.
                Message: "An unexpected error in server occurred! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries or constraint violations.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for unexpected errors, ensuring the application remains stable.
                Message: "An unexpected error occurred! Please try again later."
                
            **All the error gets logged in system.models.ErrorLogs. This helps to identify the errors in the system.

        Notes:
            - The returned queryset allows you to access individual objects and their attributes.
            - The `message` provides user-friendly feedback on the success or failure of the operation.

        """
        try:
            product_types = Product_type.objects.all()
            return product_types, "Fetched all product types successfully!"

        # Handle database-related errors
        except DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
            ErrorLogs.objects.create(error_type="DatabaseError", error_message=str(db_err))
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle Operational errors, e.g., connection issues
        except OperationalError as op_err:
            print(f"Operational error occurred: {op_err}")
            ErrorLogs.objects.create(error_type="OperationalError", error_message=str(op_err))
            return None, "An unexpected error in server occurred! Please try again later."

        # Handle programming errors, e.g., invalid queries
        except ProgrammingError as prog_err:
            print(f"Programming error occurred: {prog_err}")
            ErrorLogs.objects.create(error_type="ProgrammingError", error_message=str(prog_err))
            return None, "An unexpected error in server occurred! Please try again later."

        # Handle integrity errors, e.g., data inconsistency
        except IntegrityError as integrity_err:
            print(f"Integrity error occurred: {integrity_err}")
            ErrorLogs.objects.create(error_type="IntegrityError", error_message=str(integrity_err))
            return None, "Same type exists in Database!"

        # Handle general exceptions (fallback for unexpected errors)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            ErrorLogs.objects.create(error_type="UnexpectedError", error_message=str(e))
            return None, "An unexpected error occurred! Please try again later."


    
    def create_product_type(type,description):
        try:
            # first check if the type already exists
            pass
        except:
            pass

    def update_product_type(product_type_pk,type,description):
        pass

    def delete_product_type(product_type_pk):
        pass

    

    # Manage Product Category
    def create_product_category(product_type_pk,category,description):
        pass

    def update_product_category(product_category_pk,product_type_pk,category,description):
        pass

    def delete_product_category(product_category_pk):
        pass

    def fetch_all_product_categories():
        pass
    
    # Manage Product Sub Category
    def create_product_sub_category(product_category_pk,sub_category,description):
        pass
    def update_product_sub_category(product_type_id,category,description):
        pass 


