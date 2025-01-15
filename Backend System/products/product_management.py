from .models import *
from system.models import *
from django.db import DatabaseError,OperationalError,IntegrityError,ProgrammingError
from system.manage_error_log import ManageErrorLog
class ManageProducts:
    # Manage Product Types
    
    # def fetch_all_product_types():
    #     """
    #     Retrieve all product types from the database with detailed exception handling.

    #     This function fetches all records from the `Product_type` model and returns them as a queryset.
    #     It includes comprehensive exception handling to manage various types of errors that may occur during the query.

    #     Returns:
    #         tuple:
    #             - QuerySet or None: A queryset containing all `Product_type` records if successful,
    #             or `None` if an error occurs.
    #             - str: A message indicating the success or failure of the operation.

    #     Example Usage:
    #         product_types, message = fetch_all_product_types()
    #         if product_types:
    #             print(message)
    #             for product in product_types:
    #                 print(f"ID: {product.pk}, Type: {product.type}, Description: {product.description}")
    #         else:
    #             print(message)

    #     Exception Handling:
    #         - **DatabaseError**: Catches general database-related issues and logs the error.
    #             Example: Issues with the database engine or query execution.
    #             Message: "An unexpected error in Database occurred! Please try again later."
    #         - **OperationalError**: Handles server-related errors such as connection issues or timeouts.
    #             Message: "An unexpected error in server occurred! Please try again later."
    #         - **ProgrammingError**: Catches programming errors such as invalid queries or schema mismatches.
    #             Message: "An unexpected error in server occurred! Please try again later."
    #         - **IntegrityError**: Handles data integrity issues such as duplicate entries or constraint violations.
    #             Message: "Same type exists in Database!"
    #         - **Exception**: A catch-all for unexpected errors, ensuring the application remains stable.
    #             Message: "An unexpected error occurred! Please try again later."
                
    #         **All the error gets logged in system.models.ErrorLogs. This helps to identify the errors in the system.

    #     Notes:
    #         - The returned queryset allows you to access individual objects and their attributes.
    #         - The `message` provides user-friendly feedback on the success or failure of the operation.

    #     """
    #     try:
    #         product_types = Product_type.objects.all()
    #         return product_types, "Fetched all product types successfully!"

    #     # Handle database-related errors
    #     except DatabaseError as db_err:
    #         print(f"Database error occurred: {db_err}")
    #         new_error=ErrorLogs.objects.create(error_type="DatabaseError", error_message=str(db_err))
    #         new_error.save()
    #         return None, "An unexpected error in Database occurred! Please try again later."

    #     # Handle Operational errors, e.g., connection issues
    #     except OperationalError as op_err:
    #         print(f"Operational error occurred: {op_err}")
    #         new_error=ErrorLogs.objects.create(error_type="OperationalError", error_message=str(op_err))
    #         new_error.save()
    #         return None, "An unexpected error in server occurred! Please try again later."

    #     # Handle programming errors, e.g., invalid queries
    #     except ProgrammingError as prog_err:
    #         print(f"Programming error occurred: {prog_err}")
    #         new_error=ErrorLogs.objects.create(error_type="ProgrammingError", error_message=str(prog_err))
    #         new_error.save()
    #         return None, "An unexpected error in server occurred! Please try again later."

    #     # Handle integrity errors, e.g., data inconsistency
    #     except IntegrityError as integrity_err:
    #         print(f"Integrity error occurred: {integrity_err}")
    #         new_error=ErrorLogs.objects.create(error_type="IntegrityError", error_message=str(integrity_err))
    #         new_error.save()
    #         return None, "Same type exists in Database!"

    #     # Handle general exceptions (fallback for unexpected errors)
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    #         new_error=ErrorLogs.objects.create(error_type="UnexpectedError", error_message=str(e))
    #         new_error.save()
    #         return None, "An unexpected error occurred! Please try again later."
    
    # def create_product_type(product_type, description):
    #     """
    #         Create a new product type in the database.

    #         This function performs the following operations:
    #         1. Fetches all existing product types using `ManageProducts.fetch_all_product_types`.
    #         2. Checks if a product type with the same name already exists (case-insensitive comparison).
    #         3. If no matching type exists:
    #             - Creates a new `Product_type` record with the given `product_type` and `description`.
    #             - Returns a success status and message.
    #         4. If a matching type exists:
    #             - Returns a failure status and a message indicating duplication.
    #         5. Handles and logs any errors encountered during the process.

    #         Args:
    #             product_type (str): The name of the product type to be created.
    #             description (str): A brief description of the product type.

    #         Returns:
    #             tuple:
    #                 - bool: Indicates success (`True`) or failure (`False`) of the operation.
    #                 - str: A message describing the result of the operation.

    #         Example Usage:
    #             success, message = create_product_type("Electronics", "Products related to electronic items")
    #             if success:
    #                 print(message)
    #             else:
    #                 print(f"Failed to create product type: {message}")

    #         Workflow:
    #             1. Retrieve existing product types using `ManageProducts.fetch_all_product_types`.
    #             2. Check if a duplicate product type exists:
    #                 - Perform a case-insensitive comparison of the provided `product_type` with existing records.
    #             3. If no duplicate exists:
    #                 - Create a new `Product_type` record using `Product_type.objects.create`.
    #                 - Return a success status and message.
    #             4. If a duplicate exists:
    #                 - Return a failure status with the message "Same type exists in Database!".
    #             5. Handle any errors during the process:
    #                 - Log errors in the `ErrorLogs` model with details such as:
    #                     - `error_type`: The type of error (e.g., `DatabaseError`).
    #                     - `error_message`: The specific error message.
    #                 - Return an appropriate error message to the caller.

    #         Error Handling:
    #             - **DatabaseError**: Indicates a general database-related issue.
    #             - **OperationalError**: Indicates server-related issues such as connection problems.
    #             - **ProgrammingError**: Indicates issues like invalid queries or schema mismatches.
    #             - **IntegrityError**: Indicates data integrity issues, such as duplicate entries.
    #             - **Exception**: Handles all unexpected errors as a fallback.

    #         Error Logging:
    #             - Errors are logged in the `ErrorLogs` model with the following fields:
    #                 - `error_type` (str): The type of error encountered.
    #                 - `error_message` (str): A detailed error message describing the issue.

    #         Error Messages Returned:
    #             - **DatabaseError**:
    #                 "An unexpected error in Database occurred while creating Product Type! Please try again later."
    #             - **OperationalError**:
    #                 "An unexpected error in server occurred while creating Product Type! Please try again later."
    #             - **ProgrammingError**:
    #                 "An unexpected error in server occurred while creating Product Type! Please try again later."
    #             - **IntegrityError**:
    #                 "Same type exists in Database!"
    #             - **General Error**:
    #                 "An unexpected error occurred while creating Product Type! Please try again later."

    #         Returns in Various Scenarios:
    #             - **Success**:
    #                 (True, "New Product type <product_type> successfully added!")
    #             - **Duplicate Product Type**:
    #                 (False, "Same type exists in Database!")
    #             - **Error Scenarios**:
    #                 (False, "<Error-specific message>")
    #     """
        
    #     try:
    #         # Fetch existing product types
    #         product_types, message = ManageProducts.fetch_all_product_types()
    #         if product_types:
    #             # Check for duplicate types (case-insensitive)
    #             if any(p.type.lower() == product_type.lower() for p in product_types):
    #                 return False, "Same type exists in Database!"

    #             # Create a new product type if no duplicates are found
    #             Product_type.objects.create(type=product_type, description=description)
    #             return True, f"New Product type {product_type} successfully added!"

    #         return False, message

    #     except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
    #         # Log the error
    #         error_type = type(error).__name__  # Get the name of the error as a string
    #         error_message = str(error)
    #         ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
    #         print(f"{error_type} occurred: {error_message}")

    #         # Return appropriate messages based on the error type
    #         error_messages = {
    #             "DatabaseError": "An unexpected error in Database occurred while creating Product Type! Please try again later.",
    #             "OperationalError": "An unexpected error in server occurred while creating Product Type! Please try again later.",
    #             "ProgrammingError": "An unexpected error in server occurred while creating Product Type! Please try again later.",
    #             "IntegrityError": "Same type exists in Database!",
    #         }

    #     return False, error_messages.get(error_type, "An unexpected error occurred while creating Product Type! Please try again later.")
    
    # def update_product_type(product_type_pk, new_type, description):
    #     """
    #         Update an existing product type in the database.

    #         This function performs the following operations:
    #         1. Fetches all existing product types using `ManageProducts.fetch_all_product_types`.
    #         2. Checks if a product type with the same name already exists (case-insensitive comparison).
    #         3. If no duplicate exists:
    #             - Retrieves the product type to update using its primary key (`product_type_pk`).
    #             - Updates the product type's `type` and `description` fields with the provided values.
    #             - Saves the changes to the database.
    #             - Returns a success status and message.
    #         4. If a duplicate exists:
    #             - Returns a failure status and a message indicating duplication.
    #         5. Handles and logs any errors encountered during the process.

    #         Args:
    #             product_type_pk (int): The primary key of the product type to be updated.
    #             new_type (str): The new name for the product type.
    #             description (str): The new description for the product type.

    #         Returns:
    #             tuple:
    #                 - bool: Indicates success (`True`) or failure (`False`) of the operation.
    #                 - str: A message describing the result of the operation.

    #         Example Usage:
    #             success, message = update_product_type(
    #                 product_type_pk=1, 
    #                 new_type="Updated Electronics", 
    #                 description="Updated description for electronics"
    #             )
    #             if success:
    #                 print(message)
    #             else:
    #                 print(f"Failed to update product type: {message}")

    #         Workflow:
    #             1. Retrieve existing product types using `ManageProducts.fetch_all_product_types`.
    #             2. Check if a duplicate product type exists:
    #                 - Perform a case-insensitive comparison of `new_type` with existing records.
    #             3. If no duplicate exists:
    #                 - Use `Product_type.objects.get` to retrieve the product type by its primary key.
    #                 - Update the `type` and `description` fields.
    #                 - Save the changes to the database.
    #                 - Return a success status and message.
    #             4. If a duplicate exists:
    #                 - Return a failure status with the message "Same type exists in Database!".
    #             5. Handle any errors during the process:
    #                 - Log errors in the `ErrorLogs` model with details such as:
    #                     - `error_type`: The type of error (e.g., `DatabaseError`).
    #                     - `error_message`: The specific error message.
    #                 - Return an appropriate error message to the caller.

    #         Error Handling:
    #             - **Product_type.DoesNotExist**:
    #                 - Raised if the specified product type does not exist in the database.
    #                 - Returns (False, "Product Type does not exist!").
    #             - **DatabaseError**: Indicates a general database-related issue.
    #             - **OperationalError**: Indicates server-related issues such as connection problems.
    #             - **ProgrammingError**: Indicates issues like invalid queries or schema mismatches.
    #             - **IntegrityError**: Indicates data integrity issues, such as duplicate entries.
    #             - **Exception**: Handles all unexpected errors as a fallback.

    #         Error Logging:
    #             - Errors are logged in the `ErrorLogs` model with the following fields:
    #                 - `error_type` (str): The type of error encountered.
    #                 - `error_message` (str): A detailed error message describing the issue.

    #         Error Messages Returned:
    #             - **DoesNotExist**:
    #                 "Product Type does not exist!"
    #             - **DatabaseError**:
    #                 "An unexpected error in Database occurred while updating Product Type! Please try again later."
    #             - **OperationalError**:
    #                 "An unexpected error in server occurred while updating Product Type! Please try again later."
    #             - **ProgrammingError**:
    #                 "An unexpected error in server occurred while updating Product Type! Please try again later."
    #             - **IntegrityError**:
    #                 "Same type exists in Database!"
    #             - **General Error**:
    #                 "An unexpected error occurred while updating Product Type! Please try again later."

    #         Returns in Various Scenarios:
    #             - **Success**:
    #                 (True, "Product Type updated successfully!")
    #             - **Duplicate Product Type**:
    #                 (False, "Same type exists in Database!")
    #             - **Non-existent Product Type**:
    #                 (False, "Product Type does not exist!")
    #             - **Error Scenarios**:
    #                 (False, "<Error-specific message>")
    #     """
    #     try:
    #         # Fetch existing product types
    #         product_types, message = ManageProducts.fetch_all_product_types()
    #         if product_types:
    #             # Check for duplicate types (case-insensitive)
    #             if any(p.type.lower() == new_type.lower() for p in product_types):
    #                 return False, "Same type exists in Database!" 
            
    #         # Get the product type object
    #         product_type = Product_type.objects.get(pk=product_type_pk)

    #         # Update the product type
    #         product_type.type = new_type  # Ensure this is a string
    #         product_type.description = description
    #         product_type.save()

    #         return True, "Product Type updated successfully!"
        
    #     except Product_type.DoesNotExist:
    #         return False, "Product Type does not exist!"
        
    #     except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
    #         # Log the error
    #         error_type = type(error).__name__
    #         error_message = str(error)
    #         ErrorLogs.objects.create(error_type=error_type, error_message=error_message)
    #         print(f"{error_type} occurred: {error_message}")
            
    #         # Return appropriate messages based on the error type
    #         error_messages = {
    #             "DatabaseError": "An unexpected error in Database occurred while updating Product Type! Please try again later.",
    #             "OperationalError": "An unexpected error in server occurred while updating Product Type! Please try again later.",
    #             "ProgrammingError": "An unexpected error in server occurred while updating Product Type! Please try again later.",
    #             "IntegrityError": "Same type exists in Database!",
    #         }
    #         return False, error_messages.get(error_type, "An unexpected error occurred while updating Product Type! Please try again later.")

    # def delete_product_type(product_type_pk):
        # """
        #     Delete a product type from the database.

        #     This function attempts to delete a product type identified by its primary key (`product_type_pk`).
        #     If the product type exists, it is deleted, and a success message is returned.
        #     If the product type does not exist or an error occurs, appropriate error messages are logged and returned.

        #     Args:
        #         product_type_pk (int): The primary key of the product type to delete.

        #     Returns:
        #         tuple:
        #             - bool: Indicates success (`True`) or failure (`False`) of the operation.
        #             - str: A message describing the result of the operation.

        #     Example Usage:
        #         success, message = delete_product_type(1)
        #         if success:
        #             print(message)
        #         else:
        #             print(f"Failed to delete product type: {message}")

        #     Workflow:
        #         1. Retrieve the product type using `Product_type.objects.get` with the provided primary key.
        #         2. Delete the product type if it exists.
        #         3. Handle cases where the product type does not exist by returning an appropriate error message.
        #         4. Log errors using `ManageErrorLog.create_error_log` for various exception types.
        #         5. Return an error message based on the type of exception encountered.

        #     Error Handling:
        #         - **DoesNotExist**:
        #             - Raised if the specified product type does not exist in the database.
        #             - Returns (False, "Product Type does not exist!").
        #         - **DatabaseError**:
        #             - Indicates a general database-related issue.
        #             - Logs the error and returns (False, "An unexpected error in Database occurred while deleting Product Type! Please try again later.").
        #         - **OperationalError**:
        #             - Indicates server-related issues such as connection problems.
        #             - Logs the error and returns (False, "An unexpected error in server occurred while deleting Product Type! Please try again later.").
        #         - **ProgrammingError**:
        #             - Indicates issues like invalid queries or schema mismatches.
        #             - Logs the error and returns (False, "An unexpected error in server occurred while deleting Product Type! Please try again later.").
        #         - **IntegrityError**:
        #             - Indicates data integrity issues, such as constraint violations.
        #             - Logs the error and returns (False, "Same type exists in Database!").
        #         - **Exception**:
        #             - Catches any other unexpected errors.
        #             - Logs the error and returns (False, "An unexpected error occurred while deleting Product Type! Please try again later.").

        #     Error Logging:
        #         - Errors are logged in the `ErrorLogs` model using the `ManageErrorLog.create_error_log` method.
        #         - Each error log includes:
        #             - `error_type` (str): The type of error encountered (e.g., "DatabaseError").
        #             - `error_message` (str): A detailed error message describing the issue.

        #     Returns in Various Scenarios:
        #         - **Success**:
        #             (True, "Product Type deleted successfully!")
        #         - **Non-existent Product Type**:
        #             (False, "Product Type does not exist!")
        #         - **Error Scenarios**:
        #             - DatabaseError: "An unexpected error in Database occurred while deleting Product Type! Please try again later."
        #             - OperationalError: "An unexpected error in server occurred while deleting Product Type! Please try again later."
        #             - ProgrammingError: "An unexpected error in server occurred while deleting Product Type! Please try again later."
        #             - IntegrityError: "Same type exists in Database!"
        #             - General Error: "An unexpected error occurred while deleting Product Type! Please try again later."
        #     """
        # # Get the product type with product_type_pk
        # try:
        #     get_product_type = Product_type.objects.get(pk=product_type_pk)
        #     get_product_type.delete()
        #     return True, "Product Type deleted successfully!"
        # except Product_type.DoesNotExist:
        #     return False, "Product Type does not exist!"
        # except (DatabaseError, OperationalError, ProgrammingError, IntegrityError, Exception) as error:
        #     # Log the error
        #     error_type = type(error).__name__
        #     error_message = str(error)
        #     ManageErrorLog.create_error_log(error_type, error_message)
        #     print(f"{error_type} occurred: {error_message}")
        #     # Return appropriate messages based on the error type
        #     error_messages = {
        #         "DatabaseError": "An unexpected error in Database occurred while deleting Product Type! Please try again later.",
        #         "OperationalError": "An unexpected error in server occurred while deleting Product Type! Please try again later.",
        #         "ProgrammingError": "An unexpected error in server occurred while deleting Product Type! Please try again later.",
        #         "IntegrityError": "Same type exists in Database!",
        #     }
        #     return False, error_messages.get(error_type, "An unexpected error occurred while deleting Product Type! Please try again later.")

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
        pass

    def fetch_all_product_categories():
        pass
    
    # Manage Product Sub Category
    def create_product_sub_category(product_category_pk,sub_category,description):
        pass
    def update_product_sub_category(product_type_id,category,description):
        pass 


