from django.db import models
from django.conf import settings

# --- Society Structure Models ---
# These models define the physical layout of the society

class Society(models.Model):
    """
    Represents the overarching Society or housing complex.
    """
    name = models.CharField(max_length=200)
    address = models.TextField()
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Building(models.Model):
    """
    Represents a specific building or block within the Society.
    A Society can have multiple Buildings.
    """
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=100) # e.g., "A Wing", "Block B"
    floors = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} - {self.society.name}"

class Flat(models.Model):
    """
    Represents an individual residential unit (Flat/Apartment) inside a Building.
    """
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='flats')
    number = models.CharField(max_length=20) # e.g., "101", "404B"
    owner_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        # Prevent duplicate flat numbers in the same building
        unique_together = ('building', 'number')

    def __str__(self):
        return f"Flat {self.number} ({self.building.name})"


# --- Resident Data Models ---
# These models store user-specific data related to their residence

class ResidentProfile(models.Model):
    """
    Links a standard Django/Core User to a specific Flat in the society.
    This holds resident-specific metadata.
    """
    # 1-to-1 link with the custom User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resident_profile')
    
    # The flat they currently reside in (can be null if not yet assigned)
    flat = models.ForeignKey(Flat, on_delete=models.SET_NULL, null=True, blank=True, related_name='residents')
    move_in_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Profile: {self.user.email} (Flat {self.flat.number if self.flat else 'Unassigned'})"


class FamilyMember(models.Model):
    """
    Represents additional family members living with the primary Resident.
    """
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=150)
    relation = models.CharField(max_length=50) # e.g., "Spouse", "Child", "Parent"
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relation} to {self.resident.user.email})"


class Vehicle(models.Model):
    """
    Stores data about vehicles owned by a Resident for parking management.
    """
    VEHICLE_TYPES = (
        ('car', 'Car'),
        ('bike', 'Bike'),
    )
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='vehicles')
    number = models.CharField(max_length=20, unique=True) # License plate number
    type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    parking_slot = models.CharField(max_length=20, blank=True, null=True) # Assigned parking space

    def __str__(self):
        return f"{self.number} ({self.get_type_display()}) - {self.resident.user.email}"
