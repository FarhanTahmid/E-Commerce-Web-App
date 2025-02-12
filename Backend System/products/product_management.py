from .models import *
from system.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.manage_error_log import ManageErrorLog
from e_commerce_app import settings
import os
from system.system_log import SystemLogs
from django.utils import timezone

class ManageProducts:
    
    # Manage Product Category
    def fetch_product_categories(product_category_pk=""):

        """
    Retrieve all product categories from the database with detailed exception handling.

    This function fetches all records from the `Product_Category` model and returns them as a queryset if no
    product_category_pk is provided. If provided, then fetches that particular product category.
    It includes comprehensive exception handling to manage various types of errors that may occur during the query.

    Args:
        product_category_pk (int, optional): The primary key (ID) of a specific product category to be fetched. Defaults to None.

    Returns:
        tuple:
            - QuerySet or None: A queryset containing all `Product_Category` records if successful,
              or `None` if an error occurs.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        product_categories, message = fetch_product_categories()
        if product_categories:
            print(message)
            for category in product_categories:
                print(f"ID: {category.pk}, Name: {category.category_name}, Description: {category.description}")
        else:
            print(message)

        product_category, message = fetch_product_categories(product_category_pk=1)
        if product_category:
            print(message)
            print(f"ID: {product_category.pk}, Name: {product_category.category_name}, Description: {product_category.description}")
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

    Notes:
        - All errors are logged in `ErrorLogs` for debugging and analysis.
        - The returned queryset allows you to access individual objects and their attributes.
        - The `message` provides user-friendly feedback on the success or failure of the operation.
    """        
        try:
            if product_category_pk != "":
                return Product_Category.objects.get(pk=product_category_pk), "Product categories successfully!"
            else:
                product_category = Product_Category.objects.all()
                return product_category, "Fetched all product categories successfully!" if len(product_category) > 0 else "No product categories found"

        # Handle database-related errors
        except DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
            new_error=ErrorLogs.objects.create(error_type="DatabaseError", error_message=str(db_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle Operational errors, e.g., connection issues
        except OperationalError as op_err:
            print(f"Operational error occurred: {op_err}")
            new_error=ErrorLogs.objects.create(error_type="OperationalError", error_message=str(op_err))
            new_error.save()
            return None, "An unexpected error in server occurred! Please try again later."

        # Handle programming errors, e.g., invalid queries
        except ProgrammingError as prog_err:
            print(f"Programming error occurred: {prog_err}")
            new_error=ErrorLogs.objects.create(error_type="ProgrammingError", error_message=str(prog_err))
            new_error.save()
            return None, "An unexpected error in server occurred! Please try again later."

        # Handle integrity errors, e.g., data inconsistency
        except IntegrityError as integrity_err:
            print(f"Integrity error occurred: {integrity_err}")
            new_error=ErrorLogs.objects.create(error_type="IntegrityError", error_message=str(integrity_err))
            new_error.save()
            return None, "Same type exists in Database!"

        # Handle general exceptions (fallback for unexpected errors)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            new_error=ErrorLogs.objects.create(error_type="UnexpectedError", error_message=str(e))
            new_error.save()
            return None, "An unexpected error occurred! Please try again later."

    def create_product_category(request,product_category_name,description):

        """
        Create a new product category with detailed exception handling.

        This function attempts to add a new product category to the database. It first checks for
        existing categories to avoid duplicates. If the category does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            product_category (str): The name of the product category to be added.
            description (str): A description of the product category.

        Returns:
            tuple:
                - bool: `True` if the category was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product_category("Electronics", "All electronic items.")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating Product Category! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating Product Category! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating Product Category! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating Product Category! Please try again later."
                
            **All errors are logged in `system.models.ErrorLogs` for debugging and analysis.

        Notes:
            - The function ensures that product category names are checked in a case-insensitive manner to prevent duplicates.
            - If a duplicate category is found, it will not be added, and an appropriate message will be returned.
        """

        try:
            # Fetch existing product categories
            product_categories, message = ManageProducts.fetch_product_categories()
            if product_categories:
                # Check for duplicate types (case-insensitive)
                if any(p.category_name.lower() == product_category_name.lower() for p in product_categories):
                    return False, "Same type exists in Database!"

            # Create a new product type if no duplicates are found
            product_category = Product_Category.objects.create(category_name=product_category_name, description=description)
            product_category.save()
            SystemLogs.updated_by(request,product_category)
            SystemLogs.admin_activites(request,f"Created Product Category {product_category_name}",message="Created")
            return True, f"New Product category. {product_category_name} successfully added!"


        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating Product Category! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating Product Category! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating Product Category! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while creating Product Category! Please try again later.")

    def update_product_category(request,product_category_pk,new_category_name,description):
        """
        Update an existing product category with detailed exception handling.

        This function attempts to update the details of a product category. It checks for duplicate
        category names before making the update, and if successful, saves the new category details.
        The function includes comprehensive exception handling to log and report any errors that occur.

        Args:
            product_category_pk (int): The primary key (ID) of the product category to be updated.
            new_category_name (str): The new name for the product category.
            description (str): The updated description for the product category.

        Returns:
            tuple:
                - bool: `True` if the category was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product_category(1, "New Category Name", "Updated description.")
            print(message)

        Exception Handling:
            - **Product_Category.DoesNotExist**: Handles the case where the category to be updated does not exist.
                Message: "Product Category does not exist!"
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating Product Category! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating Product Category! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating Product Category! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating Product Category! Please try again later."
                
            **All errors are logged in `system.models.ErrorLogs` for debugging and analysis.

        Notes:
            - The function ensures that the updated category name is checked for duplicates before updating.
            - If the category does not exist, an error message will be returned.
        """
        try:
            # Fetch existing product types
            product_categories, message = ManageProducts.fetch_product_categories()
            # Get the product type object
            product_category = Product_Category.objects.get(pk=product_category_pk)
            if product_categories:
                # Check for duplicate types (case-insensitive)
                for p in product_categories:
                    if p != product_category and p.category_name.lower() == new_category_name.lower():
                        return False, "Same type exists in Database!" 
        
            # Update the product type if changed
            if product_category.category_name.lower() != new_category_name.lower():
                product_category.category_name = new_category_name  # Ensure this is a string
            if product_category.description.lower() != description.lower():
                product_category.description = description
            product_category.save()
            SystemLogs.updated_by(request,product_category)
            SystemLogs.admin_activites(request,f"Updated Product Category, {new_category_name}",message="Updated")
            return True, "Product Category updated successfully!"
        
        except Product_Category.DoesNotExist:
            return False, "Product Category does not exist!"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")
            
            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating Product Category! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating Product Category! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating Product Category! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating Product Category! Please try again later.")

    def delete_product_category(request,product_category_pk):

        """
        Delete a product category from the database with detailed exception handling.

        This function attempts to delete a product category based on the provided primary key (ID).
        If the category exists, it is deleted. The function handles various errors and logs them for debugging.

        Args:
            product_category_pk (int): The primary key (ID) of the product category to be deleted.

        Returns:
            tuple:
                - bool: `True` if the product category was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_product_category(1)
            print(message)

        Exception Handling:
            - **Product_Category.DoesNotExist**: Handles the case where the category to be deleted does not exist.
                Message: "Product Category does not exist!"
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting Product Category! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting Product Category! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting Product Category! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as foreign key constraints or data corruption.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting Product Category! Please try again later."
                
            **All errors are logged in `system.models.ErrorLogs` for debugging and analysis.

        Notes:
            - The function attempts to fetch the product category using its primary key and deletes it if found.
            - If the category does not exist, an error message will be returned.
        """

        try:
            get_product_category = Product_Category.objects.get(pk=product_category_pk)
            SystemLogs.admin_activites(request,f"Deleted Product Category {get_product_category.category_name}",message="Deleted")
            get_product_category.delete()
            return True, "Product Category deleted successfully!"
        except Product_Category.DoesNotExist:
            return False, "Product Category does not exist!"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__
            error_message = str(error)
            ManageErrorLog.create_error_log(error_type, error_message)
            print(f"{error_type} occurred: {error_message}")
            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting Product Category! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting Product Category! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting Product Category! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting Product Category! Please try again later.")
    
    # Manage Product Sub Category
    def fetch_product_sub_category(product_sub_category_pk=""):
        try:
            if product_sub_category_pk != "":
                product_sub_category = Product_Sub_Category.objects.get(pk=product_sub_category_pk)
                return product_sub_category, "Product sub-categories successfully!"
            else:
                product_sub_category = Product_Sub_Category.objects.all()
                return product_sub_category, "Fetched all product sub-categories successfully!" if len(product_sub_category) > 0 else "No product sub-categories found"
        # Handle database-related errors
        except DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
            new_error = ErrorLogs.objects.create(error_type="DatabaseError", error_message=str(db_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle Operational errors, e.g., connection issues
        except OperationalError as op_err:
            print(f"Operational error occurred: {op_err}")
            new_error = ErrorLogs.objects.create(error_type="OperationalError", error_message=str(op_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle programming errors, e.g., invalid queries
        except ProgrammingError as prog_err:
            print(f"Programming error occurred: {prog_err}")
            new_error = ErrorLogs.objects.create(error_type="ProgrammingError", error_message=str(prog_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle integrity errors, e.g., data inconsistency
        except IntegrityError as integrity_err:
            print(f"Integrity error occurred: {integrity_err}")
            new_error = ErrorLogs.objects.create(error_type="IntegrityError", error_message=str(integrity_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle general exceptions (fallback for unexpected errors)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            new_error = ErrorLogs.objects.create(error_type="UnexpectedError", error_message=str(e))
            new_error.save()
            return None, "An unexpected error occurred! Please try again later."
        
    def fetch_all_product_sub_categories_for_a_category(product_category_pk):
        """
        Fetch all product sub-categories for a given product category.

        This function retrieves all sub-categories associated with a specified product category.
        It handles various exceptions that might occur during the database operations and logs
        the errors for further analysis.

        Args:
            product_category_pk (int): The primary key (ID) of the product category.

        Returns:
            tuple:
                - QuerySet: A QuerySet of Product_Sub_Category objects if the operation is successful.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            sub_categories, message = fetch_all_product_sub_categories_for_a_category(1)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in Database occurred! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in Database occurred! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as data inconsistency.
                Message: "An unexpected error in Database occurred! Please try again later."
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.

        """
        try:
            product_category = Product_Category.objects.get(pk=product_category_pk)
            product_sub_categories = Product_Sub_Category.objects.filter(category_id=product_category)
            return product_sub_categories, "Fetched all product sub-categories for a category successfully!" if len(product_sub_categories)>0 else "No product sub-categories found"

        # Handle database-related errors
        except DatabaseError as db_err:
            print(f"Database error occurred: {db_err}")
            new_error = ErrorLogs.objects.create(error_type="DatabaseError", error_message=str(db_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle Operational errors, e.g., connection issues
        except OperationalError as op_err:
            print(f"Operational error occurred: {op_err}")
            new_error = ErrorLogs.objects.create(error_type="OperationalError", error_message=str(op_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle programming errors, e.g., invalid queries
        except ProgrammingError as prog_err:
            print(f"Programming error occurred: {prog_err}")
            new_error = ErrorLogs.objects.create(error_type="ProgrammingError", error_message=str(prog_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle integrity errors, e.g., data inconsistency
        except IntegrityError as integrity_err:
            print(f"Integrity error occurred: {integrity_err}")
            new_error = ErrorLogs.objects.create(error_type="IntegrityError", error_message=str(integrity_err))
            new_error.save()
            return None, "An unexpected error in Database occurred! Please try again later."

        # Handle general exceptions (fallback for unexpected errors)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            new_error = ErrorLogs.objects.create(error_type="UnexpectedError", error_message=str(e))
            new_error.save()
            return None, "An unexpected error occurred! Please try again later."
        
    def create_product_sub_category(request,product_category_pk,sub_category_name,description):

        """
        Create a new product sub-category with detailed exception handling.

        This function attempts to add a new product sub-category to the database. It first checks for
        existing sub-categories to avoid duplicates. If the sub-category does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            product_category_pk (int): The primary key (ID) of the product category.
            sub_category_name (str): The name of the product sub-category to be added.
            description (str): A description of the product sub-category.

        Returns:
            tuple:
                - bool: `True` if the sub-category was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product_sub_category(1, "Lipstick", "Lipstick Item")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating Product Sub Category! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating Product Sub Category! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating Product Sub Category! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating Product Sub Category! Please try again later."

        Notes:
            - The function ensures that sub-category names are checked in a case-insensitive manner to prevent duplicates.
            - If a duplicate sub-category is found, it will not be added, and an appropriate message will be returned.
            - All errors are logged in `ErrorLogs` for debugging and analysis.
        """
        
        try:
            # Fetch product all sub category
            product_sub_categories, message = ManageProducts.fetch_all_product_sub_categories_for_a_category(product_category_pk)
            if product_sub_categories:
                # Check for duplicate types (case-insensitive)
                if any(p.sub_category_name.lower() == sub_category_name.lower() for p in product_sub_categories):
                    return False, "Same type exists in Database!"
            
            product_category = Product_Category.objects.get(pk=product_category_pk)
            sub_category = Product_Sub_Category.objects.create(sub_category_name=sub_category_name,description=description)
            sub_category.category_id.add(product_category)
            SystemLogs.updated_by(request,sub_category)
            SystemLogs.admin_activites(request,f"Created Product Sub Category {sub_category_name}",message="Created")
            return True, f"New Product sub-category, {sub_category_name} successfully added!"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating Product Sub Category! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating Product Sub Category! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating Product Sub Category! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while creating Product Sub Category! Please try again later.")
        except Exception as e:
            # Log the error
            error_type = "UnexpectedError"
            error_message = str(e)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")
            return False, "An unexpected error occurred while creating Product Sub Category! Please try again later."
    
    def update_product_sub_category(request,product_sub_category_pk,category_pk_list,sub_category_name,description):

        """
        Update an existing product sub-category with detailed exception handling.

        This function attempts to update the details of a product sub-category. It checks for changes in
        the associated categories, sub-category name, and description, and updates them accordingly.
        The function includes comprehensive exception handling to log and report any errors that occur.

        Args:
            product_sub_category_pk (int): The primary key (ID) of the product sub-category to be updated.
            category_pk_list (list): A list of primary keys (IDs) of the categories to be associated with the sub-category.
            sub_category_name (str): The new name for the product sub-category.
            description (str): The updated description for the product sub-category.

        Returns:
            tuple:
                - bool: `True` if the sub-category was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product_sub_category(1, [1, 2], "Moisturizer", "Updated description")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating Product Sub Category! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating Product Sub Category! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating Product Sub Category! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating Product Sub Category! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            user_changed_product_categories = [Product_Category.objects.get(pk=category_id) for category_id in category_pk_list]
            # fetching the product sub category
            product_sub_categories = Product_Sub_Category.objects.get(pk=product_sub_category_pk)
            categories_of_sub_category = product_sub_categories.category_id.all()
            if sorted(user_changed_product_categories) != sorted(categories_of_sub_category):
                # removing the previous categories 
                for category in categories_of_sub_category:
                    product_sub_categories.category_id.remove(category)
                # adding the new categories
                for category in category_pk_list:
                    product_sub_categories.category_id.add(Product_Category.objects.get(pk=category))
            #updating the sub category name if changed
            if product_sub_categories.sub_category_name.lower() != sub_category_name.lower():
                product_sub_categories.sub_category_name = sub_category_name
            #updating the sub category description if changed
            if product_sub_categories.description.lower() != description.lower():
                product_sub_categories.description = description
            #saving the changes made
            product_sub_categories.save()
            SystemLogs.updated_by(request,product_sub_categories)
            SystemLogs.admin_activites(request,f"Updated Product Sub Category {product_sub_categories.sub_category_name}",message="Updated")
            return True, "Product Sub Category updated successfully!"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating Product Sub Category! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating Product Sub Category! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating Product Sub Category! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }

            return False, error_messages.get(error_type, "An unexpected error occurred while updating Product Sub Category! Please try again later.")
        except Exception as e:
            # Log the error
            error_type = "UnexpectedError"
            error_message = str(e)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")
            return False, "An unexpected error occurred while updating Product Sub Category! Please try again later."
        
    def delete_product_sub_category(request,product_sub_category_pk):

        """
        Delete an existing product sub-category with detailed exception handling.

        This function attempts to delete a product sub-category from the database. It handles various
        exceptions that might occur during the process, logging each error for further analysis.

        Args:
            product_sub_category_pk (int): The primary key (ID) of the product sub-category to be deleted.

        Returns:
            tuple:
                - bool: `True` if the sub-category was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_product_sub_category(1)
            print(message)

        Exception Handling:
            - **Product_Sub_Category.DoesNotExist**: Handles the case where the sub-category does not exist.
                Message: "Product Sub Category does not exist!"
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting Product Sub Category! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting Product Sub Category! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting Product Sub Category! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting Product Sub Category! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            get_product_sub_category = Product_Sub_Category.objects.get(pk=product_sub_category_pk)
            SystemLogs.admin_activites(request,f"Deleted Product Sub Category {get_product_sub_category.sub_category_name}",message="Deleted")
            get_product_sub_category.delete()
            return True, "Product Sub Category deleted successfully!"
        except Product_Sub_Category.DoesNotExist:
            return False, "Product Sub Category does not exist!"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__
            error_message = str(error)
            ManageErrorLog.create_error_log(error_type, error_message)
            print(f"{error_type} occurred: {error_message}")
            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting Product Sub Category! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting Product Sub Category! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting Product Sub Category! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting Product Sub Category! Please try again later.")

    #Manage Product Brand
    def create_product_brand(request,brand_name,brand_established_year,
                            is_own_brand,brand_country="",brand_description="",brand_logo=""):
        
        """
        Create a new product brand with detailed exception handling.

        This function attempts to add a new product brand to the database. It first checks for
        existing brands to avoid duplicates. If the brand does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            brand_name (str): The name of the product brand to be added.
            brand_country (str): The country of the product brand.
            brand_description (str): A description of the product brand.
            brand_established_year (int): The year the product brand was established.
            is_own_brand (bool): Indicates if the brand is owned by the company.
            brand_logo (str, optional): The logo of the product brand. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the brand was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product_brand("Loreal", "USA", "Loreal Paris", 1909, False)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating Product brand! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating Product brand! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating Product brand! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating Product brand! Please try again later."

        Notes:
            - The function ensures that brand names are checked in a case-insensitive manner to prevent duplicates.
            - If a duplicate brand is found, it will not be added, and an appropriate message will be returned.
            - All errors are logged in `ErrorLogs` for debugging and analysis.
        """
        
        try:
            # Fetch existing product brands
            product_brands = Product_Brands.objects.all()
            if product_brands:
                # Check for duplicate brands (case-insensitive)
                if any(p.brand_name.lower() == brand_name.lower() for p in product_brands):
                    return False, "Same brand exists in Database!"
            
            # Create a new product brand if no duplicates are found
            product_brand = Product_Brands.objects.create(brand_name=brand_name,
                                        brand_established_year=brand_established_year, 
                                        is_own_brand=is_own_brand)
            product_brand.save()
            if (brand_country != ""):
                product_brand.brand_country=brand_country
            if (brand_description != ""):
                product_brand.brand_description=brand_description
            if (brand_logo != ""):
                product_brand.brand_logo=brand_logo
            product_brand.save()
            SystemLogs.updated_by(request,product_brand)
            SystemLogs.admin_activites(request,f"Created Product Brand {brand_name}",message="Created")
            return True, f"New Product brand, {brand_name} successfully added!"
                                              
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating Product brand! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating Product brand! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating Product brand! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating Product brand! Please try again later.")

    def fetch_product_brand(pk="",brand_name=""):

        """
        Fetch a product brand by its name or pk with detailed exception handling.

        Choose any one argument to retrieve. Providing multiple will return the using first paramter.
        This function attempts to retrieve a product brand from the database based on the provided brand name or pk.
        If no brand name or pk is provided, it retrieves all product brands. It handles various errors that might
        occur during the process, logging each error for further analysis.

        Args:
            pk (int): The primary key (ID) of the product brand to be fetched. If provided, brand_name is ignored.
            brand_name (str): The name of the product brand to be fetched. If None, fetches all product brands.

        Returns:
            tuple:
                - Product_Brands or QuerySet: The product brand object if found, or a QuerySet of all product brands.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            brand, message = fetch_product_brand("Loreal")
            print(message)

            brands, message = fetch_product_brand(None)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while fetching Product brand, {brand_name}! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while fetching Product brand, {brand_name}! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while fetching Product brand, {brand_name}! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "An unexpected error in Database occurred while fetching Product brand, {brand_name}! Please try again later."
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while fetching Product brand, {brand_name}! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        
        try:
            if brand_name != "":
                return Product_Brands.objects.get(brand_name=brand_name), "Product brand fetched successfully!"
            elif pk != "":
                return Product_Brands.objects.get(pk=pk), "Product brand fetched successfully!"
            else:
                product_brand = Product_Brands.objects.all()
                return product_brand, "All Product brands fetched successfully!" if len(product_brand)>0 else "No Product brands found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching Product brand! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating Product brand! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating Product brand! Please try again later.",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching Product brand! Please try again later.")
        
    def update_product_brand(request,product_brand_pk,brand_name,brand_established_year,
                            is_own_brand=False,brand_country="",brand_description="",brand_logo=""):
        """
        Update an existing product brand with detailed exception handling.

        This function attempts to update the details of a product brand. It checks for changes in
        the brand name, country, description, established year, ownership status, and logo, and updates them accordingly.
        If a new logo is provided, the previous logo is deleted. The function includes comprehensive exception handling
        to log and report any errors that occur.

        Args:
            product_brand_pk (int): The primary key (ID) of the product brand to be updated.
            brand_name (str): The new name for the product brand.
            brand_country (str): The new country of the product brand. Defaults to None
            brand_description (str): The updated description for the product brand. Defaults to None
            brand_established_year (int): The updated year the product brand was established.
            is_own_brand (bool): Indicates if the brand is owned by the company.
            brand_logo (str, optional): The new logo of the product brand. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the brand was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product_brand(1, "New Brand Name", "USA", "Updated description", 2000, True, new_logo)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating Product brand! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating Product brand! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating Product brand! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating Product brand! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
            - If a new logo is provided, the previous logo is deleted.
        """
        try:
            #get product brand
            product_brand = Product_Brands.objects.get(pk=product_brand_pk)
            all_product_brand,message = ManageProducts.fetch_product_brand()
            #update the product brand name
            if (product_brand.brand_name.lower() != brand_name.lower()):
                for p in all_product_brand:
                    if p != product_brand and p.brand_name.lower() == brand_name.lower():
                        return False, "Same brand already exists!"
                product_brand.brand_name = brand_name
            #update the product brand country
            if (brand_country != ""):
                product_brand.brand_country = brand_country
            #update the product brand description
            if (brand_description != ""):
                product_brand.brand_description = brand_description
            #update the product brand established year
            if (product_brand.brand_established_year != brand_established_year):
                product_brand.brand_established_year = brand_established_year
            #update the product brand own status
            if (product_brand.is_own_brand != is_own_brand):
                product_brand.is_own_brand = is_own_brand
            #update the product brand logo
            if (brand_logo != ""):
                if product_brand.brand_logo:
                    # Delete the previous logo file from local directory
                    path = settings.MEDIA_ROOT+str(product_brand.brand_logo)
                    if os.path.exists(path):
                        os.remove(path)
                    product_brand.brand_logo.delete()
                product_brand.brand_logo = brand_logo
            product_brand.save()
            SystemLogs.updated_by(request,product_brand)
            SystemLogs.admin_activites(request,f"Updated Product Brand {product_brand.brand_name}",message="Updated")
            return True, f"Product brand, {brand_name} updated successfully!"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating Product brand! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating Product brand! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating Product brand! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating Product brand! Please try again later.")
        
    def delete_product_brand(request,product_brand_pk):

        """
        Delete an existing product brand with detailed exception handling.

        This function attempts to delete a product brand from the database. It first deletes the associated logo file
        if it exists, and then deletes the product brand. The function includes comprehensive exception handling
        to log and report any errors that occur.

        Args:
            product_brand_pk (int): The primary key (ID) of the product brand to be deleted.

        Returns:
            tuple:
                - bool: `True` if the brand was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_product_brand(1)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting Product brand! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting Product brand! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting Product brand! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting Product brand! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
            - If the product brand has an associated logo, the logo file is deleted from the local directory before deleting the brand.
        """
        try:
            #get product brand
            product_brand = Product_Brands.objects.get(pk=product_brand_pk)
            #delete the product brand logo first if exists
            if product_brand.brand_logo:
                path = settings.MEDIA_ROOT+str(product_brand.brand_logo)
                if os.path.exists(path):
                    os.remove(path)
            SystemLogs.admin_activites(request,f"Deleted Product Brand {product_brand.brand_name}",message="Deleted")
            product_brand.delete()
            return True, "Product brand deleted successfully!"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting Product brand! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting Product brand! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting Product brand! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting Product brand! Please try again later.")
        
    #Manage Product Flavour
    def fetch_product_flavour(product_flavour_name="",pk=""):

        """
        Fetch a product flavour by its name or primary key with detailed exception handling.

        Choose any one argument to retrieve. Providing multiple will return the using first paramter.
        This function attempts to retrieve a product flavour from the database based on the provided flavour name or primary key.
        If no flavour name or primary key is provided, it retrieves all product flavours. It handles various errors that might
        occur during the process, logging each error for further analysis.

        Args:
            product_flavour_name (str, optional): The name of the product flavour to be fetched. Defaults to None.
            pk (int, optional): The primary key (ID) of the product flavour to be fetched. Defaults to None.

        Returns:
            tuple:
                - Product_Flavours or QuerySet: The product flavour object if found, or a QuerySet of all product flavours.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            flavour, message = fetch_product_flavour("Vanilla")
            print(message)

            flavour, message = fetch_product_flavour(pk=1)
            print(message)

            flavours, message = fetch_product_flavour()
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while fetching product flavour! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while fetching product flavour! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while fetching product flavour! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while fetching product flavour! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:
            if product_flavour_name!= "":
                return Product_Flavours.objects.get(product_flavour_name=product_flavour_name), "Product flavour fetched successfully!"
            elif pk!= "":
                return Product_Flavours.objects.get(pk=pk), "Product flavour fetched successfully!"
            else:
                product_flavour = Product_Flavours.objects.all()
                return product_flavour, "All Product flavours fetched successfully!" if len(product_flavour)>0 else "No Product flavour found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching product flavour! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching product flavour! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching product flavour! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching product flavour! Please try again later.")
    
    def create_product_flavour(request,product_flavour_name):

        """
        Create a new product flavour with detailed exception handling.

        This function attempts to add a new product flavour to the database. It first checks for
        existing flavours to avoid duplicates. If the flavour does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            product_flavour_name (str): The name of the product flavour to be added.

        Returns:
            tuple:
                - bool: `True` if the flavour was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product_flavour("Vanilla")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating product flavour! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating product flavour! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating product flavour! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating product flavour! Please try again later."

        Notes:
            - The function ensures that flavour names are checked in a case-insensitive manner to prevent duplicates.
            - If a duplicate flavour is found, it will not be added, and an appropriate message will be returned.
            - All errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:
            product_flavours,message = ManageProducts.fetch_product_flavour()
            if product_flavours:
                if any(p.product_flavour_name.lower() == product_flavour_name.lower() for p in product_flavours):
                    return False, "Same flavour exists in Database!"
            
            product_flavour = Product_Flavours.objects.create(product_flavour_name=product_flavour_name)
            SystemLogs.updated_by(request,product_flavour)
            SystemLogs.admin_activites(request,f"Created Product Flavour {product_flavour_name}",message="Created")
            return True, f"New Product flavour, {product_flavour_name} successfully added!"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating product flavour! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating product flavour! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating product flavour! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating product flavour! Please try again later.")
        
    def update_product_flavour(request,product_flavour_pk,product_flavour_name):

        """
        Update an existing product flavour with detailed exception handling.

        This function attempts to update the details of a product flavour. It checks for changes in
        the flavour name and updates it accordingly. The function includes comprehensive exception handling
        to log and report any errors that occur.

        Args:
            product_flavour_pk (int): The primary key (ID) of the product flavour to be updated.
            product_flavour_name (str): The new name for the product flavour.

        Returns:
            tuple:
                - bool: `True` if the flavour was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product_flavour(1, "Strawberry")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating product flavour! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating product flavour! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating product flavour! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating product flavour! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #fetch product flavour with pk
            product_flavour,message = ManageProducts.fetch_product_flavour(pk=product_flavour_pk)
            all_product_flavour , message = ManageProducts.fetch_product_flavour()
            #detecting changes
            if (product_flavour.product_flavour_name.lower() != product_flavour_name.lower()):
                for p in all_product_flavour:
                    if p != product_flavour and p.product_flavour_name.lower() == product_flavour_name.lower():
                        return False, "Same product flavour already exists!"
                product_flavour.product_flavour_name = product_flavour_name
            product_flavour.save()
            SystemLogs.updated_by(request,product_flavour)
            SystemLogs.admin_activites(request,f"Updated Product Flavour {product_flavour.product_flavour_name}",message="Updated")
            return True, "Product flavour updated successfully!"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating product flavour! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating product flavour! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating product flavour! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating product flavour! Please try again later.")
        
    def delete_product_flavour(request,product_flavour_pk):

        """
        Delete an existing product flavour with detailed exception handling.

        This function attempts to delete a product flavour from the database. It handles various
        exceptions that might occur during the process, logging each error for further analysis.

        Args:
            product_flavour_pk (int): The primary key (ID) of the product flavour to be deleted.

        Returns:
            tuple:
                - bool: `True` if the flavour was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_product_flavour(1)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting product flavour! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting product flavour! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting product flavour! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting product flavour! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #fetch product flavour with pk
            product_flavour,message = ManageProducts.fetch_product_flavour(pk=product_flavour_pk)
            SystemLogs.admin_activites(request,f"Deleted Product Flavour {product_flavour.product_flavour_name}",message="Deleted")
            product_flavour.delete()
            return True, "Product flavour deleted successfully!"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting product flavour! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting product flavour! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting product flavour! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting product flavour! Please try again later.") 
        
    #Manage Product
    def fetch_product(product_pk="",product_name="",product_brand_pk="",
                      product_category_pk_list=[],product_sub_category_pk_list=[]):
        
        """
        Fetch products based on various optional parameters with detailed exception handling.

        Choose any one argument to retrieve result. Providing multiple will return using first parameter.
        This function attempts to retrieve products from the database based on the provided parameters.
        If no parameter is provided retrieves all products.
        It handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            product_pk (int, optional): The primary key (ID) of the product to be fetched. Defaults to None.
            product_name (str, optional): The name of the product to be fetched. Defaults to None.
            product_brand_pk (int, optional): The primary key (ID) of the product brand to filter by. Defaults to None.
            product_category_pk_list (list, optional): A list of primary keys (IDs) of the product categories to filter by. Defaults to None.
            product_sub_category_pk_list (list, optional): A list of primary keys (IDs) of the product sub-categories to filter by. Defaults to None.

        Returns:
            tuple:
                - QuerySet or Product: A QuerySet of products matching the criteria or a single Product object.
                - Using 'pk' and 'product_name' uses 'get' operation to retrieve. So returns error if not found.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            product, message = fetch_product(product_pk=1)
            print(message)

            products, message = fetch_product(product_name="Shampoo")
            print(message)

            products, message = fetch_product(product_brand_pk=1)
            print(message)

            products, message = fetch_product(product_category_pk_list=[1, 2])
            print(message)

            products, message = fetch_product(product_sub_category_pk_list=[1, 2])
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while fetching product! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while fetching product! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while fetching product! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while fetching product! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #fetching products according to provided arguments
            if product_pk!= "":
                return Product.objects.get(pk=product_pk), "Products fetched successfully!"
            elif product_name!= "":
                return Product.objects.get(product_name=product_name), "Products fetched successfully!"
            elif product_brand_pk!= "":
                product_brand,message = ManageProducts.fetch_product_brand(pk=product_brand_pk)
                products = Product.objects.filter(product_brand=product_brand)
                return products, "Products fetched successfully!" if products else "No products found using this brand"
            elif len(product_category_pk_list)>0:
                product_categories = [Product_Category.objects.get(pk=p) for p in product_category_pk_list]
                products=set()
                for categories in product_categories:
                    products.update(categories.products.all())
                return products, "Products fetched successfully!" if products else "No products found using this categories"
            elif len(product_sub_category_pk_list)>0:
                product_sub_categories = [Product_Sub_Category.objects.get(pk=p) for p in product_sub_category_pk_list]
                products = set()
                for sub_categories in product_sub_categories:
                    products.update(sub_categories.products.all())
                return products,"Products fetched successfully!"if products else "No products found using this sub categories"
            else:
                products = Product.objects.all()
                return products, "All Products fetched successfully!" if len(products)>0 else "No products founds"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching product! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching product! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching product! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching product! Please try again later.") 
    
    def fetch_product_with_sku_and_discount(product_pk="",product_brand_pk="",
                      product_category_pk="",product_sub_category_pk=""):
        
        try:
            product_with_sku_and_discount = {}
            #fetching products according to provided arguments
            if product_pk!= "":
                product,message = ManageProducts.fetch_product(product_pk=product_pk)
                product_skus,message = ManageProducts.fetch_product_sku(product_id=product_pk)
                all_product_discount,message = ManageProducts.fetch_product_discount(product_id=product_pk)
                product_discount = all_product_discount[0] if all_product_discount else ""
                
                product_with_sku_and_discount = {
                'product':product,
                'product_skus':product_skus,
                'product_discount':product_discount,
                }

            elif product_brand_pk!= "":
                products,message = ManageProducts.fetch_product(product_brand_pk=product_brand_pk)
                for p in products:
                    product_with_sku_and_discount[p.pk] = ManageProducts.fetch_product_with_sku_and_discount(product_pk=p.pk)
            elif product_category_pk!= "":
                products,message = ManageProducts.fetch_product(product_category_pk_list=[product_category_pk])
                for p in products:
                    product_with_sku_and_discount[p.pk] = ManageProducts.fetch_product_with_sku_and_discount(product_pk=p.pk)
            elif product_sub_category_pk!= "":
                products,message = ManageProducts.fetch_product(product_sub_category_pk_list=[product_sub_category_pk])
                for p in products:
                    product_with_sku_and_discount[p.pk] = ManageProducts.fetch_product_with_sku_and_discount(product_pk=p.pk)
            
            return product_with_sku_and_discount, "Fetched successfully"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching product! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching product! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching product! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching product! Please try again later.") 
        
    def create_product(request,product_name,product_category_pk_list,product_sub_category_pk_list,product_description,
                       product_summary,product_brand_pk="",product_ingredients="",
                       product_usage_direction=""):
        """
        Create a new product with detailed exception handling.

        This function attempts to add a new product to the database. It first checks if a product with the same name
        already exists. If it does, it returns an error message. Otherwise, it creates a new product with the specified
        attributes and associates it with the provided categories, sub-categories, and optional attributes like brand,
        ingredients, and usage directions. The function handles various errors that might occur during the process,
        logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            product_name (str): The name of the product to be created.
            product_category_pk_list (list): A list of primary keys (IDs) of the product categories to be associated with the product.
            product_sub_category_pk_list (list): A list of primary keys (IDs) of the product sub-categories to be associated with the product.
            product_description (str): The description of the product.
            product_summary (str): The summary of the product.
            product_brand_pk (int, optional): The primary key (ID) of the product brand. Defaults to None.
            product_ingredients (str, optional): The ingredients of the product. Defaults to None.
            product_usage_direction (str, optional): The usage directions of the product. Defaults to None.

        Returns:
            tuple:
                - bool or Product: `False` if the product already exists or an error occurs, otherwise the created product object.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product(
                request,
                product_name="New Product",
                product_category_pk_list=[1, 2],
                product_sub_category_pk_list=[3, 4],
                product_description="This is a new product.",
                product_summary="New product summary",
                product_brand_pk=1,
                product_ingredients="Ingredient1, Ingredient2",
                product_usage_direction="Use as directed."
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating product! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating product! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating product! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating product! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            try:
                #checking to see if product alreadt exists or not. If does returning
                product,message = ManageProducts.fetch_product(product_name=product_name)
                if product.product_name.lower() == product_name.lower():
                    return False, "Same product already exists!"
            except:
                print("creating product as no matching found")
                product = Product.objects.create(product_name=product_name,product_description=product_description,
                                    product_summary=product_summary)
                product.save()
                #getting all category and sub categories and flavours
                product_category = [Product_Category.objects.get(pk=p) for p in product_category_pk_list]
                product_sub_category = [Product_Sub_Category.objects.get(pk=p) for p in product_sub_category_pk_list]
                product.product_category.add(*product_category)
                product.product_sub_category.add(*product_sub_category)
                #checking optional paramters
                if product_brand_pk != "":
                    brand,message = ManageProducts.fetch_product_brand(pk=product_brand_pk)
                    product.product_brand = brand
                if product_ingredients!= "":
                    product.product_ingredients = product_ingredients
                if product_usage_direction!= "":
                    product.product_usage_direction = product_usage_direction
                product.save()
                SystemLogs.updated_by(request,product)
                SystemLogs.admin_activites(request,f"Created Product {product_name}",message="Created")
                return product, f"Product, {product_name} created!"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating product! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating product! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating product! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating product! Please try again later.")

    def update_product(request,product_pk,product_name,product_category_pk_list,product_sub_category_pk_list,product_description,
                       product_summary,product_brand_pk="",product_ingredients="",
                       product_usage_direction=""):

        """
        Update an existing product with detailed exception handling.

        This function attempts to update an existing product in the database. It fetches the product
        using the provided primary key (product_pk) and updates its attributes with the specified values.
        The function handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            product_pk (int): The primary key (ID) of the product to be updated.
            product_name (str): The new name of the product.
            product_category_pk_list (list): A list of primary keys (IDs) of the product categories to be associated with the product.
            product_sub_category_pk_list (list): A list of primary keys (IDs) of the product sub-categories to be associated with the product.
            product_description (str): The new description of the product.
            product_summary (str): The new summary of the product.
            product_brand_pk (int, optional): The primary key (ID) of the product brand. Defaults to None.
            product_ingredients (str, optional): The new ingredients of the product. Defaults to None.
            product_usage_direction (str, optional): The new usage directions of the product. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the product was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product(
                request,
                product_pk=1,
                product_name="Updated Product",
                product_category_pk_list=[1, 2],
                product_sub_category_pk_list=[3, 4],
                product_description="This is an updated product.",
                product_summary="Updated product summary",
                product_brand_pk=1,
                product_ingredients="Updated Ingredient1, Updated Ingredient2",
                product_usage_direction="Use as directed."
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating product! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating product! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating product! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating product! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            new_product_category = sorted([Product_Category.objects.get(pk=p) for p in product_category_pk_list])
            new_product_sub_category = sorted([Product_Sub_Category.objects.get(pk=p) for p in product_sub_category_pk_list])
            
            #getting the product
            product,message = ManageProducts.fetch_product(product_pk=product_pk)
            existing_product_category = sorted(product.product_category.all())
            existing_product_sub_category = sorted(product.product_sub_category.all())
            all_products, message = ManageProducts.fetch_product()
            #updating only if changed
            if product.product_name.lower() != product_name.lower():
                for p in all_products:
                    if p!=product and p.product_name.lower() == product_name.lower():
                        return False,"Same product name already exists!"
                product.product_name = product_name
            if existing_product_category != new_product_category:
                product.product_category.set(new_product_category)
            if existing_product_sub_category != new_product_sub_category:
                product.product_sub_category.set(new_product_sub_category)
            if product.product_description.lower() != product_description.lower():
                product.product_description = product_description
            if product.product_summary.lower() != product_summary.lower():
                product.product_summary = product_summary
            if product_brand_pk!= "":
                product_brand,message = ManageProducts.fetch_product_brand(pk=product_brand_pk)
                product.product_brand = product_brand
            if product_ingredients!= "":
                product.product_ingredients =  product_ingredients
            if product_usage_direction!= "":
                product.product_usage_direction = product_usage_direction
            product.save()
            SystemLogs.updated_by(request,product)
            SystemLogs.admin_activites(request,f"Updated Product {product.product_name}",message="Updated")
            return True, "Product updated successfully!"
            
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating product! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating product! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating product! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating product! Please try again later.")
        
    def delete_product(request,product_pk):

        """
        Delete an existing product with detailed exception handling.

        This function attempts to delete a product from the database. It handles various
        exceptions that might occur during the process, logging each error for further analysis.

        Args:
            product_pk (int): The primary key (ID) of the product to be deleted.

        Returns:
            tuple:
                - bool: `True` if the product was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_product(1)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting product! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting product! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting product! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting product! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:
            #getting the product
            product,message = ManageProducts.fetch_product(product_pk=product_pk)
            SystemLogs.admin_activites(request,f"Deleted Product {product.product_name}",message="Deleted")
            product.delete()
            return True, "Product deleted successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting product! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting product! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting product! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting product! Please try again later.")
    
    #Manage product sku
    def fetch_product_sku(pk="",product_id="",product_name="",product_sku=""):

        """
        Fetch product SKUs based on various optional parameters with detailed exception handling.

        Must provide any one paramter. If no paramter is passed, returns False with a message.
        This function attempts to retrieve product SKUs from the database based on the provided parameters.
        It handles various errors that might occur during the process, logging each error for further analysis.

        Args:
            pk (int, optional): The primary key (ID) of the product SKU to be fetched. Defaults to None.
            product_id (int, optional): The primary key (ID) of the product to filter SKUs by. Defaults to None.
            product_name (str, optional): The name of the product to filter SKUs by. Defaults to None.
            product_sku (str, optional): The SKU code of the product SKU to be fetched. Defaults to None.

        Returns:
            tuple:
                - QuerySet or Product_SKU: A QuerySet of product SKUs matching the criteria or a single Product_SKU object.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            sku, message = fetch_product_sku(pk=1)
            print(message)

            skus, message = fetch_product_sku(product_id=1)
            print(message)

            skus, message = fetch_product_sku(product_name="Shampoo")
            print(message)

            sku, message = fetch_product_sku(product_sku="SKU123")
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating product sku! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating product sku! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating product sku! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating product sku! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """

        try:
            if pk!= "":
                return Product_SKU.objects.get(pk=pk), "Fetched successfully"
            elif product_id!= "":
                product,message = ManageProducts.fetch_product(product_pk=product_id)
                product_skus = Product_SKU.objects.filter(product_id=product)
                return product_skus, "Fetched successfully" if len(product_skus)>0 else "No product sku found"
            elif product_name!= "":
                product,message = ManageProducts.fetch_product(product_name=product_name)
                product_skus = Product_SKU.objects.filter(product_id=product)
                return product_skus, "Fetched successfully" if len(product_skus)>0 else "No product sku found"
            elif product_sku!= "":
                try:
                    return Product_SKU.objects.get(product_sku=product_sku.upper()), "Fetched successfully"
                except:
                    return False, "No sku with this code!"
            else:
                return False , "No parameter passed! Must pass a single parameter"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching product sku! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching product sku! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching product sku! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching product sku! Please try again later.")
        
    def create_product_sku(request,product_pk,product_price,product_stock,product_flavours_pk_list,product_color="",product_size=""):

        """
        Create a new product SKU with detailed exception handling.

        This function attempts to add a new product SKU to the database. It first fetches the product
        using the provided product primary key (product_pk). Then, it creates a new SKU for the product
        with the specified price, stock, and optional attributes like color and size. The function handles
        various errors that might occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            product_pk (int): The primary key (ID) of the product to which the SKU belongs.
            product_price (float): The price of the product SKU.
            product_stock (int): The stock quantity of the product SKU.
            product_flavours_pk_list (list): A list of primary keys (IDs) of the product flavours to be associated with the SKU.
            product_color (str, optional): The color of the product SKU. Defaults to None.
            product_size (str or int, optional): The size of the product SKU. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the product SKU was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product_sku(
                request,
                product_pk=1,
                product_price=25.99,
                product_stock=100,
                product_flavours_pk_list=[1, 2, 3],
                product_color="Red",
                product_size="L"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating product sku! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating product sku! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating product sku! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating product sku! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            product,message = ManageProducts.fetch_product(product_pk=product_pk)
            #creating product sku for this product
            product_sku = Product_SKU.objects.create(product_id=product,product_price=product_price,product_stock=product_stock)
            product_sku.save()
            product_flavours = [Product_Flavours.objects.get(pk=p) for p in product_flavours_pk_list]
            product_sku.product_flavours.add(*product_flavours)
            if product_color!= "":
                product_sku.product_color = product_color
            if product_size!= "":
                if type(product_size) == int:
                    product_sku.product_size = str(product_size)
                else:
                    product_sku.product_size = product_size
            product_sku.save()
            SystemLogs.updated_by(request,product_sku)
            SystemLogs.admin_activites(request,f"Created Product sku with sku - {product_sku.product_sku}",message="Created")
            return True, "Product sku created successfully"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating product sku! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating product sku! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating product sku! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating product sku! Please try again later.")

    def update_product_sku(request,product_sku_pk,product_id,product_price,product_stock,product_flavours_pk_list,product_color="",product_size=""):

        """
        Update an existing product SKU with detailed exception handling.

        This function attempts to update an existing product SKU in the database. It fetches the product
        and the SKU using the provided primary keys. Then, it updates the SKU with the specified price,
        stock, and optional attributes like color and size. The function handles various errors that might
        occur during the process, logging each error for further analysis.

        Args:
            request (Request): The request object containing the user information.
            product_sku_pk (int): The primary key (ID) of the product SKU to be updated.
            product_id (int): The primary key (ID) of the product to which the SKU belongs.
            product_price (float): The new price of the product SKU.
            product_stock (int): The new stock quantity of the product SKU.
            product_flavours_pk_list (list): A list of primary keys (IDs) of the product flavours to be associated with the SKU.
            product_color (str, optional): The new color of the product SKU. Defaults to None.
            product_size (str or int, optional): The new size of the product SKU. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the product SKU was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product_sku(
                request,
                product_sku_pk=1,
                product_id=1,
                product_price=29.99,
                product_stock=150,
                product_flavours_pk_list=[1, 2, 3],
                product_color="Blue",
                product_size="M"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating product sku! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating product sku! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating product sku! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating product sku! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            #new product_id
            product,message = ManageProducts.fetch_product(product_pk=product_id)
            #getting the product sku
            product_sku,message = ManageProducts.fetch_product_sku(pk=product_sku_pk)
            #sku gets updated automatically, no logic needed
            existing_product_flavours = sorted(product_sku.product_flavours.all())
            new_product_flavours = sorted([Product_Flavours.objects.get(pk=p) for p in product_flavours_pk_list])
            if product_sku.product_id != product:
                product_sku.product_id = product
            if product_sku.product_price != product_price:
                product_sku.product_price = product_price
            if product_sku.product_stock != product_stock:
                product_sku.product_stock = product_stock
            if existing_product_flavours != new_product_flavours:
                product_sku.product_flavours.set(new_product_flavours)
            if product_color!= "":
                product_sku.product_color = product_color
            if product_size!= "":
                    if type(product_size) == int:
                        product_sku.product_size = str(product_size)
                    else:
                        product_sku.product_size = product_size
            product_sku.save()
            SystemLogs.updated_by(request,product_sku)
            SystemLogs.admin_activites(request,f"Updated Product sku with sku - {product_sku.product_sku}",message="Updated")
            return True, f"Product sku updated with new sku id"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating product sku! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating product sku! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating product sku! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating product sku! Please try again later.")
        
    def delete_product_sku(request,product_sku_pk):

        """
        Delete an existing product SKU with detailed exception handling.

        This function attempts to delete a product SKU from the database. It handles various
        exceptions that might occur during the process, logging each error for further analysis.

        Args:
            product_sku_pk (int): The primary key (ID) of the product SKU to be deleted.

        Returns:
            tuple:
                - bool: `True` if the product SKU was deleted successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = delete_product_sku(1)
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while deleting product sku! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while deleting product sku! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while deleting product sku! Please try again later."
            - **IntegrityError**: Handles data integrity issues.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while deleting product sku! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        
        try:
            #getting the product sku
            product_sku, message = ManageProducts.fetch_product_sku(pk=product_sku_pk)
            SystemLogs.admin_activites(request,f"Deleted Product sku with sku - {product_sku.product_sku}",message="Deleted")
            product_sku.delete()
            return True, "Product sku successfully deleted!"

        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting product sku! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting product sku! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting product sku! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting product sku! Please try again later.")
    
    #product images
    def fetch_product_image(product_pk="",product_image_pk=""):
        
        """
    Fetch product images based on various optional parameters with detailed exception handling.

    This function attempts to retrieve product images from the database based on the provided parameters.
    It handles various errors that might occur during the process, logging each error for further analysis.

    Args:
        product_pk (int, optional): The primary key (ID) of the product to filter images by. Defaults to None.
        product_image_pk (int, optional): The primary key (ID) of the specific product image to be fetched. Defaults to None.

    Returns:
        tuple:
            - QuerySet or Product_Images: A QuerySet of product images if `product_pk` is provided, a single Product_Images object if `product_image_pk` is provided, or all product images if no parameters are provided.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        # Fetch images for a specific product
        product_images, message = fetch_product_image(product_pk=1)
        print(message)

        # Fetch a specific product image
        product_image, message = fetch_product_image(product_image_pk=1)
        print(message)

        # Fetch all product images
        all_product_images, message = fetch_product_image()
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while fetching product image! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while fetching product image! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while fetching product image! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while fetching product image! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """
        try:
            if product_pk!= "":
                product,message = ManageProducts.fetch_product(product_pk=product_pk)
                product_images = Product_Images.objects.filter(product_id=product)
                return product_images, "Product images fetched successfully" if len(product_images)>0 else "No images found for this product"
            elif product_image_pk!= "":
                product_image = Product_Images.objects.get(pk=product_image_pk)
                return product_image, "Product images fetched successfully"
            else:
                product_images = Product_Images.objects.all()
                return product_images, "All product images fetched successfully" if len(product_images)>0 else "No images found"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching product image! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching product image! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching product image! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching product image! Please try again later.")
    
    def create_product_image(request,product_id,product_image_list,color="",size=""):

        """
    Create new product images with detailed exception handling.

    This function attempts to add new images to a product in the database. It first fetches the product
    using the provided product primary key (product_id). Then, it creates new images for the product
    with the specified attributes like color and size. The function handles various errors that might
    occur during the process, logging each error for further analysis.

    Args:
        request (Request): The request object containing the user information.
        product_id (int): The primary key (ID) of the product to which the images belong.
        product_image_list (list): A list of image files to be associated with the product.
        color (str, optional): The color of the product images. Defaults to None.
        size (str or int, optional): The size of the product images. Defaults to None.

    Returns:
        tuple:
            - bool: `True` if the product images were created successfully, `False` otherwise.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        success, message = create_product_image(
            request,
            product_id=1,
            product_image_list=[image1, image2],
            color="Red",
            size="L"
        )
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while creating product image! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while creating product image! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while creating product image! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while creating product image! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """
        try:
            #getting the product
            try:
                product,message = ManageProducts.fetch_product(product_pk=product_id)
                for i in product_image_list:
                    product_image_created = Product_Images.objects.create(product_id=product,product_image = i)
                    product_image_created.save()
                    if color!= "":
                        product_image_created.color = color
                    if size!= "":
                        if type(size) == int:
                            product_image_created.size = str(size)
                        else:
                            product_image_created.size = size
                    product_image_created.save()
                    SystemLogs.updated_by(request,product_image_created)
                    SystemLogs.admin_activites(request,f"Created Product image for the product, {product_image_created.product_id.product_name}",message="Created Product Image")
                return True, "Product image created successfully"
            except:
                return False, "No product image found"
            
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating product image! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating product image! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating product image! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating product image! Please try again later.")
        
    def update_product_image(request,product_image_pk,new_image="",color="",size=""):

        """
    Update an existing product image with detailed exception handling.

    This function attempts to update an existing product image in the database. It fetches the product image
    using the provided primary key (product_image_pk) and updates its attributes with the specified values.
    The function handles various errors that might occur during the process, logging each error for further analysis.

    Args:
        request (Request): The request object containing the user information.
        product_image_pk (int): The primary key (ID) of the product image to be updated.
        new_image (File, optional): The new image file to replace the existing one. Defaults to None.
        color (str, optional): The new color of the product image. Defaults to None.
        size (str or int, optional): The new size of the product image. Defaults to None.

    Returns:
        tuple:
            - bool: `True` if the product image was updated successfully, `False` otherwise.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        success, message = update_product_image(
            request,
            product_image_pk=1,
            new_image=new_image_file,
            color="Blue",
            size="M"
        )
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while updating product image! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while updating product image! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while updating product image! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while updating product image! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """
        try:
            #getting the product images
            product_image ,message = ManageProducts.fetch_product_image(product_image_pk=product_image_pk)
            if new_image!= "":
                if product_image.product_image:
                    path = settings.MEDIA_ROOT+str(product_image.product_image)
                    if os.path.exists(path):
                        os.remove(path)
                    product_image.product_image.delete()
                product_image.product_image = new_image
            if color!= "":
                product_image.color = color
            if size!= "":
                size = str(size)
                product_image.size = size
            
            product_image.save()
            SystemLogs.updated_by(request,product_image)
            SystemLogs.admin_activites(request,f"Updated Product image for the product, {product_image.product_id.product_name}",message="Updated Product Image")
            return True,"Product image updated successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating product image! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating product image! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating product image! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating product image! Please try again later.")
    
    def delete_product_image(request,product_image_pk):

        """
    Delete an existing product image with detailed exception handling.

    This function attempts to delete an existing product image from the database. It fetches the product image
    using the provided primary key (product_image_pk) and deletes it along with the associated image file.
    The function handles various errors that might occur during the process, logging each error for further analysis.

    Args:
        request (Request): The request object containing the user information.
        product_image_pk (int): The primary key (ID) of the product image to be deleted.

    Returns:
        tuple:
            - bool: `True` if the product image was deleted successfully, `False` otherwise.
            - str: A message indicating the success or failure of the operation.

    Example Usage:
        success, message = delete_product_image(
            request,
            product_image_pk=1
        )
        print(message)

    Exception Handling:
        - **DatabaseError**: Catches general database-related issues.
            Message: "An unexpected error in Database occurred while deleting product image! Please try again later."
        - **OperationalError**: Handles server-related issues such as connection problems.
            Message: "An unexpected error in server occurred while deleting product image! Please try again later."
        - **ProgrammingError**: Catches programming errors such as invalid queries.
            Message: "An unexpected error in server occurred while deleting product image! Please try again later."
        - **IntegrityError**: Handles data integrity issues.
            Message: "Same type exists in Database!"
        - **Exception**: A catch-all for any other unexpected errors.
            Message: "An unexpected error occurred while deleting product image! Please try again later."

    Notes:
        - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
    """
        
        try:
            #getting the product image
            product_image,message = ManageProducts.fetch_product_image(product_image_pk=product_image_pk)
            if product_image.product_image:
                path = settings.MEDIA_ROOT+str(product_image.product_image)
                if os.path.exists(path):
                    os.remove(path)
                product_image.product_image.delete()
            SystemLogs.admin_activites(request,f"Deleted Product image for the product, {product_image.product_id.product_name}",message="Deleted Product Image")
            product_image.delete()
            return True,"Product image deleted successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting product image! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting product image! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting product image! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting product image! Please try again later.")
        
    #product discount
    def fetch_product_discount(product_id="",discount_name="",is_active=False,product_discount_pk="",brand_id="",sub_category_pk="",category_pk=""):

        try:
            if product_id!= "":
                product,message = ManageProducts.fetch_product(product_pk=product_id)
                product_discount = Product_Discount.objects.filter(product_id=product).order_by('-pk')
                return product_discount, "Product Discounts fetched successfully" if len(product_discount)>0 else "No product discount found"
            elif product_discount_pk!= "":
                product_discount = Product_Discount.objects.get(pk=product_discount_pk)
                return product_discount,"Product Discount fetched successfully"
            elif discount_name!= "":
                product,message = ManageProducts.fetch_product(product_pk=product_id)
                product_discount = Product_Discount.objects.get(discount_name=discount_name)
                return product_discount, "Product Discount fetched successfully"
            elif is_active == True:
                now = timezone.now()
                product_discount = Product_Discount.objects.filter(start_date__lte=now, end_date__gte=now).order_by('-pk')
                return product_discount, "Active Product Discount fetched successfully"
            elif brand_id!= "":
                brand,message = ManageProducts.fetch_product_brand(pk=brand_id)
                product_discount = Product_Discount.objects.filter(brand_id=brand).order_by('-pk')
                return product_discount,"Product Discounts fetched successfully" if len(product_discount)>0 else "No product discount found"
            elif sub_category_pk!= "":
                sub_category,message = ManageProducts.fetch_product_sub_category(product_sub_category_pk=sub_category_pk)
                product_discount = Product_Discount.objects.filter(sub_category_id=sub_category)
                return product_discount,"Product Discounts fetched successfully" if len(product_discount)>0 else "No product discount found"
            elif category_pk!= "":
                category,message = ManageProducts.fetch_product_categories(product_category_pk=category_pk)
                product_discount=Product_Discount.objects.filter(category_id=category)
                return product_discount,"Product Discounts fetched successfully" if len(product_discount)>0 else "No product discount found"
            else:
                product_discount = Product_Discount.objects.all()
                return product_discount,"All product discounts fetched successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while fetching product discount! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while fetching product discount! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while fetching product discount! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while fetching product discount! Please try again later.")
         
    def create_product_discount(request,discount_name,discount_amount,start_date,end_date,product_id=[],brand_id=[],sub_category_id=[],category_id=[]):

        try:

            if len(product_id)>0:
                for prod in product_id:
                    print(prod)
                    product,message = ManageProducts.fetch_product(product_pk=prod)#single product
                    existing_discount = Product_Discount.objects.filter(
                    product_id=product)
                    if any(p.is_discount_active() for p in existing_discount):
                        return False, "Product already has a discount and is active"
                for prod in product_id:
                    product,message = ManageProducts.fetch_product(product_pk=prod)#single product
                    product_discount = Product_Discount.objects.create(product_id=product,
                            discount_name=discount_name,
                            discount_amount=discount_amount,
                            start_date=start_date,
                            end_date=end_date)
                    product_discount.save()
                    SystemLogs.updated_by(request,product_discount)
                    SystemLogs.admin_activites(request,f"Created Product Discount for the product, {product_discount.product_id.product_name}",message="Created Product Discount")
            
            elif len(brand_id)>0:

                for b in brand_id:
                    products,message = ManageProducts.fetch_product(product_brand_pk=b)#multiple products
                    brand,message = ManageProducts.fetch_product_brand(pk=b)
                    existing_discount = Product_Discount.objects.filter(brand_id=brand)
                    if any(p.is_discount_active() for p in existing_discount):
                        return False, f"Products of the brand already has a discount and is active"
                    
                for b in brand_id: 
                    products,message = ManageProducts.fetch_product(product_brand_pk=b)#multiple products
                    brand,message = ManageProducts.fetch_product_brand(pk=b)
                    for p in products:
                        product_discount = Product_Discount.objects.create(product_id=p,
                                brand_id =  brand,                                         
                                discount_name=discount_name,
                                discount_amount=discount_amount,
                                start_date=start_date,
                                end_date=end_date)
                        product_discount.save()
                        SystemLogs.updated_by(request,product_discount)
                        SystemLogs.admin_activites(request,f"Created Product Discount for the product, {product_discount.product_id.product_name}",message="Created Product Discount")

            elif len(sub_category_id)>0:
                for sub_cat in sub_category_id:
                    products,message = ManageProducts.fetch_product(product_sub_category_pk_list=[sub_cat])#multiple
                    sub_category,message = ManageProducts.fetch_product_sub_category(product_sub_category_pk=sub_cat)
                    existing_discount = Product_Discount.objects.filter(sub_category_id=sub_category)
                    if any(p.is_discount_active() for p in existing_discount):
                        return False, "Products of this sub category already has a discount and is active"
                
                for sub_cat in sub_category_id:
                    products,message = ManageProducts.fetch_product(product_sub_category_pk_list=[sub_cat])#multiple
                    sub_category,message = ManageProducts.fetch_product_sub_category(product_sub_category_pk=sub_cat)    
                    for p in products:
                        product_discount = Product_Discount.objects.create(product_id=p,
                                sub_category_id = sub_category,                                          
                                discount_name=discount_name,
                                discount_amount=discount_amount,
                                start_date=start_date,
                                end_date=end_date)
                        product_discount.save()
                        SystemLogs.updated_by(request,product_discount)
                        SystemLogs.admin_activites(request,f"Created Product Discount for the product, {product_discount.product_id.product_name}",message="Created Product Discount")

            elif len(category_id)>0:
                for cat in category_id:
                    products,message = ManageProducts.fetch_product(product_category_pk_list=[cat])#multiple
                    category,message = ManageProducts.fetch_product_categories(product_category_pk=cat)
                    existing_discount = Product_Discount.objects.filter(category_id=category)
                    if any(p.is_discount_active() for p in existing_discount):
                        return False, "Products of this category already has a discount and is active"
                    
                for cat in category_id:
                    products,message = ManageProducts.fetch_product(product_category_pk_list=[cat])#multiple
                    category,message = ManageProducts.fetch_product_categories(product_category_pk=cat)
                    for p in products:
                        product_discount = Product_Discount.objects.create(product_id=p,
                                category_id = category,
                                discount_name=discount_name,
                                discount_amount=discount_amount,
                                start_date=start_date,
                                end_date=end_date)
                        product_discount.save()
                        SystemLogs.updated_by(request,product_discount)
                        SystemLogs.admin_activites(request,f"Created Product Discount for the product, {product_discount.product_id.product_name}",message="Created Product Discount")

            return True,"Product discount created successfully"
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while creating product discount! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while creating product discount! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while creating product discount! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while creating product discount! Please try again later.")
        
    def update_product_discount(request,product_discount_pk,discount_name="",discount_amount="",start_date="",end_date="",product_id=[],sub_category_id=[],category_id=[]):

        try:
            pass
        
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while updating product discount! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while updating product discount! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while updating product discount! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while updating product discount! Please try again later.") 
        
    def delete_product_discount(request,product_discount_pk):
        """
    Deletes an existing product discount.

    Parameters:
    -----------
    request : HttpRequest
        The HTTP request object (used for logging purposes).
    product_discount_pk : int
        The primary key of the product discount to be deleted.

    Returns:
    --------
    tuple
        - If successful: (True, "Product discount deleted successfully")
        - If an error occurs: (False, "Error Message")

    Process:
    --------
    1. Fetches the existing `Product_Discount` using `ManageProducts.fetch_product_discount`.
    2. Logs the action in `SystemLogs`.
    3. Deletes the fetched `product_discount`.
    4. Returns a success message if deletion is successful.

    Error Handling:
    ---------------
    - Logs errors in the `ErrorLogs` model.
    - Handles various exceptions such as:
        - `DatabaseError`: Issues with database queries.
        - `OperationalError`: Unexpected server-related errors.
        - `ProgrammingError`: Code-related issues.
        - `IntegrityError`: Database integrity constraints.
    - Provides a specific error message based on the error type.

    Example Usage:
    --------------
    >>> delete_product_discount(request, 1)
    (True, "Product discount deleted successfully")

    >>> delete_product_discount(request, 100)
    (False, "An unexpected error occurred while deleting product discount! Please try again later.")
    
    If any database-related issue occurs, it returns a user-friendly error message.

    """
        try:
            #getting the product discount
            product_discount,message = ManageProducts.fetch_product_discount(product_discount_pk=product_discount_pk)
            SystemLogs.admin_activites(request,f"Updated Product Discount for the product, {product_discount.product_id.product_name}",message="Updated Product Discount")
            product_discount.delete()
            return True,"Product discount deleted successfully"
        except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
            # Log the error
            error_type = type(error).__name__  # Get the name of the error as a string
            error_message = str(error)
            ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
            print(f"{error_type} occurred: {error_message}")

            # Return appropriate messages based on the error type
            error_messages = {
                "DatabaseError": "An unexpected error in Database occurred while deleting product discount! Please try again later.",
                "OperationalError": "An unexpected error in server occurred while deleting product discount! Please try again later.",
                "ProgrammingError": "An unexpected error in server occurred while deleting product discount! Please try again later.",
                "IntegrityError": "Same type exists in Database!",
            }
            return False, error_messages.get(error_type, "An unexpected error occurred while deleting product discount! Please try again later.") 

        