from .models import *
from system.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.manage_error_log import ManageErrorLog
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

            return False, message

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


