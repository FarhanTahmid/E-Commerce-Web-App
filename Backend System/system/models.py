from django.db import models

# Create your models here.

class ErrorLogs(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically logs the time of the error
    error_type = models.CharField(max_length=255)  # The type of error, e.g., "DatabaseError"
    error_message = models.TextField()  # The detailed error message

    class Meta:
        verbose_name = "Error Log"
        verbose_name_plural = "Error Logs"
        ordering = ['-timestamp']  # Orders the errors by latest timestamp first

    def __str__(self):
        return f"{self.timestamp} - {self.error_type}"