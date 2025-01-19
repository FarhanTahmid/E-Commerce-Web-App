from .models import *
from system.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.manage_error_log import ManageErrorLog
from e_commerce_app import settings
import os

class ManageProducts:
    
    # Manage Product Category
    def fetch_all_product_categories():

        """
        Retrieve all product categories from the database with detailed exception handling.

        This function fetches all records from the `Product_Category` model and returns them as a queryset.
        It includes comprehensive exception handling to manage various types of errors that may occur during the query.

        Returns:
            tuple:
                - QuerySet or None: A queryset containing all `Product_Category` records if successful,
                or `None` if an error occurs.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            product_categories, message = fetch_all_product_categories()
            if product_categories:
                print(message)
                for category in product_categories:
                    print(f"ID: {category.pk}, Name: {category.name}, Description: {category.description}")
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
                
            **All errors are logged in `system.models.ErrorLogs`. This helps to identify and debug issues in the system.

        Notes:
            - The returned queryset allows you to access individual objects and their attributes.
            - The `message` provides user-friendly feedback on the success or failure of the operation.
        """
        try:
            product_category = Product_Category.objects.all()
            return product_category, "Fetched all product categories successfully!"

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

    def create_product_category(product_category_name,description):

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
            product_categories, message = ManageProducts.fetch_all_product_categories()
            if product_categories:
                # Check for duplicate types (case-insensitive)
                if any(p.category_name.lower() == product_category_name.lower() for p in product_categories):
                    return False, "Same type exists in Database!"

            # Create a new product type if no duplicates are found
            Product_Category.objects.create(category_name=product_category_name, description=description)
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

    def update_product_category(product_category_pk,new_category_name,description):
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
            product_categories, message = ManageProducts.fetch_all_product_categories()
            if product_categories:
                # Check for duplicate types (case-insensitive)
                if any(p.category_name.lower() == new_category_name.lower() for p in product_categories):
                    return False, "Same type exists in Database!" 
            
            # Get the product type object
            product_category = Product_Category.objects.get(pk=product_category_pk)

            # Update the product type
            product_category.category_name = new_category_name  # Ensure this is a string
            product_category.description = description
            product_category.save()

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

    def delete_product_category(product_category_pk):

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
            return product_sub_categories, "Fetched all product sub-categories for a category successfully!"

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
        
    def create_product_sub_category(product_category_pk,sub_category_name,description):

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
    
    def update_product_sub_category(product_sub_category_pk,category_pk_list,sub_category_name,description):

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
        
    def delete_product_sub_category(product_sub_category_pk):

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
    def create_product_brand(brand_name,brand_established_year,
                            is_own_brand,brand_country=None,brand_description=None,brand_logo=None):
        
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
            if (brand_country):
                brand_country=brand_country
            if (brand_description):
                brand_description=brand_description
            if (brand_logo):
                brand_logo=brand_logo
            product_brand.save()
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

    def fetch_product_brand(pk=None,brand_name=None):

        """
        Fetch a product brand by its name with detailed exception handling.

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
            if brand_name:
                return Product_Brands.objects.get(brand_name=brand_name), "Product brand fetched successfully!"
            elif pk:
                return Product_Brands.objects.get(pk=pk), "Product brand fetched successfully!"
            else:
                return Product_Brands.objects.all(), "All Product brands fetched successfully!"
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
        
    def update_product_brand(product_brand_pk,brand_name,brand_established_year,
                            is_own_brand,brand_country=None,brand_description=None,brand_logo=None):
        """
        Update an existing product brand with detailed exception handling.

        This function attempts to update the details of a product brand. It checks for changes in
        the brand name, country, description, established year, ownership status, and logo, and updates them accordingly.
        If a new logo is provided, the previous logo is deleted. The function includes comprehensive exception handling
        to log and report any errors that occur.

        Args:
            product_brand_pk (int): The primary key (ID) of the product brand to be updated.
            brand_name (str): The new name for the product brand.
            brand_country (str): The new country of the product brand.
            brand_description (str): The updated description for the product brand.
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
            #update the product brand name
            if (product_brand.brand_name.lower() != brand_name.lower()):
                product_brand.brand_name = brand_name
            #update the product brand country
            if (brand_country and product_brand.brand_country.lower() != brand_country.lower()):
                product_brand.brand_country = brand_country
            #update the product brand description
            if (brand_description and product_brand.brand_description.lower() != brand_description.lower()):
                product_brand.brand_description = brand_description
            #update the product brand established year
            if (product_brand.brand_established_year != brand_established_year):
                product_brand.brand_established_year = brand_established_year
            #update the product brand own status
            if (product_brand.is_own_brand != is_own_brand):
                product_brand.is_own_brand = is_own_brand
            #update the product brand logo
            if (brand_logo and product_brand.brand_logo != brand_logo):
                # Delete the previous logo if a new one is provided
                if product_brand.brand_logo:
                    # Delete the previous logo file from local directory
                    path = settings.MEDIA_ROOT+str(product_brand.brand_logo)
                    if os.path.exists(path):
                        os.remove(path)
                    product_brand.brand_logo.delete()
                product_brand.brand_logo = brand_logo
            product_brand.save()
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
        
    def delete_product_brand(product_brand_pk):

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
    def fetch_product_flavour(product_flavour_name=None,pk=None):

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
            if product_flavour_name:
                return Product_Flavours.objects.get(product_flavour_name=product_flavour_name), "Product flavour fetched successfully!"
            elif pk:
                return Product_Flavours.objects.get(pk=pk), "Product flavour fetched successfully!"
            else:
                return Product_Flavours.objects.all(), "All Product flavours fetched successfully!"
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
    
    def create_product_flavour(product_flavour_name):

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
            
            Product_Flavours.objects.create(product_flavour_name=product_flavour_name)
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
        
    def update_product_flavour(product_flavour_pk,product_flavour_name):

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
            #detecting changes
            if (product_flavour.product_flavour_name.lower() != product_flavour_name.lower()):
                product_flavour.product_flavour_name = product_flavour_name
            product_flavour.save()
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
        
    def delete_product_flavour(product_flavour_pk):

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
    def fetch_product(product_pk=None,product_name=None,product_brand_pk=None,
                      product_category_pk_list=None,product_sub_category_pk_list=None):
        
        """
        Fetch products based on various optional parameters with detailed exception handling.

        Choose any one argument to retrieve result. Providing multiple will return using first parameter.
        This function attempts to retrieve products from the database based on the provided parameters.
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
            if product_pk:
                return Product.objects.get(pk=product_pk), "Products fetched successfully!"
            elif product_name:
                return Product.objects.get(product_name=product_name), "Products fetched successfully!"
            elif product_brand_pk:
                product_brand,message = ManageProducts.fetch_product_brand(pk=product_brand_pk)
                products = Product.objects.filter(product_brand=product_brand)
                return products, "Products fetched successfully!" if products else "No products found using this brand"
            elif product_category_pk_list:
                product_categories = [Product_Category.objects.get(pk=p) for p in product_category_pk_list]
                products=set()
                for categories in product_categories:
                    products.update(categories.products.all())
                return products, "Products fetched successfully!" if products else "No products found using this categories"
            elif product_sub_category_pk_list:
                product_sub_categories = [Product_Sub_Category.objects.get(pk=p) for p in product_sub_category_pk_list]
                products = set()
                for sub_categories in product_sub_categories:
                    products.update(sub_categories.products.all())
                return products,"Products fetched successfully!"if products else "No products found using this sub categories"
            else:
                return Product.objects.all(), "All Products fetched successfully!"
            
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
        
    def create_product(product_name,product_category_pk_list,product_sub_category_pk_list,product_description,
                       product_summary,product_flavours_pk_list,product_brand_pk=None,product_ingredients=None,
                       product_usage_direction=None):
        
        """
        Create a new product with detailed exception handling.

        This function attempts to add a new product to the database. It first checks for
        existing product using the product_name to avoid duplicates. If the product does not exist, it is created.
        The function handles various errors that might occur during the process, logging each
        error for further analysis.

        Args:
            product_name (str): The name of the product to be added.
            product_category_pk_list (list): A list of primary keys (IDs) of the product categories to be associated with the product.
            product_sub_category_pk_list (list): A list of primary keys (IDs) of the product sub-categories to be associated with the product.
            product_description (str): A description of the product.
            product_summary (str): A summary of the product.
            product_flavours_pk_list (list): A list of primary keys (IDs) of the product flavours to be associated with the product.
            product_brand_pk (int, optional): The primary key (ID) of the product brand to be associated with the product. Defaults to None.
            product_ingredients (str, optional): The ingredients of the product. Defaults to None.
            product_usage_direction (str, optional): The usage directions of the product. Defaults to None.

        Returns:
            tuple:
                - Product or bool: The created product object if successful, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            product, message = create_product(
                product_name="Shampoo",
                product_category_pk_list=[1, 2],
                product_sub_category_pk_list=[3, 4],
                product_description="A cleansing shampoo",
                product_summary="Cleansing shampoo for all hair types",
                product_flavours_pk_list=[5, 6],
                product_brand_pk=1,
                product_ingredients="Water, Sodium Laureth Sulfate",
                product_usage_direction="Use as needed"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating product! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating product! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating product! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while creating product! Please try again later."

        Notes:
            - The function ensures that product names are checked in a case-insensitive manner to prevent duplicates.
            - If a duplicate product is found, it will not be added, and an appropriate message will be returned.
            - All errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            try:
                #checking to see if product alreadt exists or not. If does returning
                product,message = ManageProducts.fetch_product(product_name=product_name)
                if product.product_name.lower() == product_name.lower():
                    return False, "Same product already exists!"
            except:
                product = Product.objects.create(product_name=product_name,product_description=product_description,
                                    product_summary=product_summary)
                product.save()
                #getting all category and sub categories and flavours
                product_category = [Product_Category.objects.get(pk=p) for p in product_category_pk_list]
                product_sub_category = [Product_Sub_Category.objects.get(pk=p) for p in product_sub_category_pk_list]
                product_flavours = [Product_Flavours.objects.get(pk=p) for p in product_flavours_pk_list]
                product.product_category.add(*product_category)
                product.product_sub_category.add(*product_sub_category)
                product.product_flavours.add(*product_flavours)
                #checking optional paramters
                if product_brand_pk:
                    brand,message = ManageProducts.fetch_product_brand(pk=product_brand_pk)
                    product.product_brand = brand
                if product_ingredients:
                    product.product_ingredients = product_ingredients
                if product_usage_direction:
                    product.product_usage_direction = product_usage_direction
                product.save()

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

    def update_product(product_pk,product_name,product_category_pk_list,product_sub_category_pk_list,product_description,
                       product_summary,product_flavours_pk_list,product_brand_pk=None,product_ingredients=None,
                       product_usage_direction=None):

        """
        Update an existing product with detailed exception handling.

        This function attempts to update the details of a product. It checks for changes in
        the product name, categories, sub-categories, description, summary, flavours, brand, ingredients, and usage directions,
        and updates them accordingly. The function includes comprehensive exception handling to log and report any errors that occur.

        Args:
            product_pk (int): The primary key (ID) of the product to be updated.
            product_name (str): The new name for the product.
            product_category_pk_list (list): A list of primary keys (IDs) of the product categories to be associated with the product.
            product_sub_category_pk_list (list): A list of primary keys (IDs) of the product sub-categories to be associated with the product.
            product_description (str): The updated description of the product.
            product_summary (str): The updated summary of the product.
            product_flavours_pk_list (list): A list of primary keys (IDs) of the product flavours to be associated with the product.
            product_brand_pk (int, optional): The primary key (ID) of the product brand to be associated with the product. Defaults to None.
            product_ingredients (str, optional): The updated ingredients of the product. Defaults to None.
            product_usage_direction (str, optional): The updated usage directions of the product. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the product was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product(
                product_pk=1,
                product_name="Updated Shampoo",
                product_category_pk_list=[1, 2],
                product_sub_category_pk_list=[3, 4],
                product_description="An updated cleansing shampoo",
                product_summary="Updated cleansing shampoo for all hair types",
                product_flavours_pk_list=[5, 6],
                product_brand_pk=1,
                product_ingredients="Updated ingredients",
                product_usage_direction="Updated usage directions"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while updating product! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while updating product! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while updating product! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
                Message: "Same type exists in Database!"
            - **Exception**: A catch-all for any other unexpected errors.
                Message: "An unexpected error occurred while updating product! Please try again later."

        Notes:
            - The function ensures that all errors are logged in `ErrorLogs` for debugging and analysis.
        """
        try:
            new_product_category = sorted([Product_Category.objects.get(pk=p) for p in product_category_pk_list])
            new_product_sub_category = sorted([Product_Sub_Category.objects.get(pk=p) for p in product_sub_category_pk_list])
            new_product_flavours = sorted([Product_Flavours.objects.get(pk=p) for p in product_flavours_pk_list])
            #getting the product
            product,message = ManageProducts.fetch_product(product_pk=product_pk)
            existing_product_category = sorted(product.product_category.all())
            existing_product_sub_category = sorted(product.product_sub_category.all())
            existing_product_flavours = sorted(product.product_flavours.all())
            #updating only if changed
            if product.product_name.lower() != product_name.lower():
                product.product_name = product_name
            if existing_product_category != new_product_category:
                product.product_category.set(new_product_category)
            if existing_product_sub_category != new_product_sub_category:
                product.product_sub_category.set(new_product_sub_category)
            if existing_product_flavours != new_product_flavours:
                product.product_flavours.set(new_product_flavours)
            if product.product_description.lower() != product_description.lower():
                product.product_description = product_description
            if product.product_summary.lower() != product_summary.lower():
                product.product_summary = product_summary
            if product_brand_pk and product_brand_pk != product.product_brand.pk:
                product_brand,message = ManageProducts.fetch_product_brand(pk=product_brand_pk)
                product.product_brand = product_brand
            if product_ingredients and product.product_ingredients.lower() != product_ingredients.lower():
                product.product_ingredients =  product_ingredients
            if product_usage_direction and product.product_usage_direction.lower() != product_usage_direction.lower():
                product.product_usage_direction = product_usage_direction
            product.save()

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
        
    def delete_product(product_pk):

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
    def fetch_product_sku(pk=None,product_id=None,product_name=None,product_sku=None):

        """
        Fetch product SKUs based on various optional parameters with detailed exception handling.

        Must provide any one argument
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
            if pk:
                return Product_SKU.objects.get(pk=pk), "Fetched successfully"
            elif product_id:
                product,message = ManageProducts.fetch_product(product_pk=product_id)
                return Product_SKU.objects.filter(product_id=product), "Fetched successfully"
            elif product_name:
                product,message = ManageProducts.fetch_product(product_name=product_name)
                return Product_SKU.objects.filter(product_id=product), "Fetched successfully"
            elif product_sku:
                try:
                    return Product_SKU.objects.get(product_sku=product_sku.upper()), "Fetched successfully"
                except:
                    return False, "No sku with this code!"
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
        
    def create_product_sku(product_pk,product_price,product_stock,product_color=None,product_size=None):

        """
        Create a new product SKU with detailed exception handling.

        This function attempts to add a new product SKU to the database for a given product. It handles various errors
        that might occur during the process, logging each error for further analysis.

        Args:
            product_pk (int): The primary key (ID) of the product to which the SKU will be associated.
            product_price (float): The price of the product SKU.
            product_stock (int): The stock quantity of the product SKU.
            product_color (str, optional): The color of the product SKU. Defaults to None.
            product_size (str or int, optional): The size of the product SKU. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the product SKU was created successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = create_product_sku(
                product_pk=1,
                product_price=19.99,
                product_stock=100,
                product_color="Red",
                product_size="M"
            )
            print(message)

        Exception Handling:
            - **DatabaseError**: Catches general database-related issues.
                Message: "An unexpected error in Database occurred while creating product sku! Please try again later."
            - **OperationalError**: Handles server-related issues such as connection problems.
                Message: "An unexpected error in server occurred while creating product sku! Please try again later."
            - **ProgrammingError**: Catches programming errors such as invalid queries.
                Message: "An unexpected error in server occurred while creating product sku! Please try again later."
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
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
            if product_color:
                product_sku.product_color = product_color
            if product_size:
                if type(product_size) == int:
                    product_sku.product_size = str(product_size)
                else:
                    product_sku.product_size = product_size
            product_sku.save()
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

    def update_product_sku(product_sku_pk,product_id,product_price,product_stock,product_color=None,product_size=None):

        """
        Update an existing product SKU with detailed exception handling.

        This function attempts to update the details of a product SKU. It checks for changes in
        the product ID, price, stock, color, and size, and updates them accordingly. The function includes comprehensive
        exception handling to log and report any errors that occur. Product sku code gets updated auto.

        Args:
            product_sku_pk (int): The primary key (ID) of the product SKU to be updated.
            product_id (int): The primary key (ID) of the product to which the SKU is associated.
            product_price (float): The updated price of the product SKU.
            product_stock (int): The updated stock quantity of the product SKU.
            product_color (str, optional): The updated color of the product SKU. Defaults to None.
            product_size (str or int, optional): The updated size of the product SKU. Defaults to None.

        Returns:
            tuple:
                - bool: `True` if the product SKU was updated successfully, `False` otherwise.
                - str: A message indicating the success or failure of the operation.

        Example Usage:
            success, message = update_product_sku(
                product_sku_pk=1,
                product_id=1,
                product_price=19.99,
                product_stock=100,
                product_color="Red",
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
            - **IntegrityError**: Handles data integrity issues such as duplicate entries.
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
            if product_sku.product_id != product:
                product_sku.product_id = product
            if product_sku.product_price != product_price:
                product_sku.product_price = product_price
            if product_sku.product_stock != product_stock:
                product_sku.product_stock = product_stock
            if product_color and product_sku.product_color != product_color:
                product_sku.product_color = product_color
            if product_size  and product_sku.product_size != product_size:
                if type(product_size) == int:
                    product_sku.product_size = str(product_size)
                else:
                    product_sku.product_size = product_size
            product_sku.save()
            
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
        
    def delete_product_sku(product_sku_pk):
        pass