from django.db import models
from user.models import User

class UserFilter(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="saved_filter"
    )
    # Optional user-saved defaults (nullable so user can leave any blank)
    gender   = models.CharField(max_length=6, blank=True, null=True)
    nation   = models.CharField(max_length=100, blank=True, null=True)
    state    = models.CharField(max_length=100, blank=True, null=True)
    city     = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    mandal   = models.CharField(max_length=100, blank=True, null=True)
    village  = models.CharField(max_length=100, blank=True, null=True)
    pincode  = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        # Display user's username and saved filters
        filters = []
        for field in ["gender", "nation", "state", "city", "district", "mandal", "village", "pincode"]:
            value = getattr(self, field)
            if value:
                filters.append(f"{field}: {value}")
        filters_str = ", ".join(filters) if filters else "No filters set"
        return f"{self.user.username} - {filters_str}"
