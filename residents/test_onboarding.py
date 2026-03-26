from django.test import TestCase
from django.urls import reverse
from core.models import User
from residents.models import Society, Building, Flat, ResidentProfile

class AdminOnboardingTest(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@esociety.com',
            password='testpassword'
        )
        self.admin_user.role = 'admin'
        self.admin_user.save()

        # Create a pending resident
        self.pending_resident = User.objects.create_user(
            email='resident@esociety.com',
            password='testpassword'
        )
        self.pending_resident.role = 'resident'
        self.pending_resident.save()

        # Create some society structure
        self.society = Society.objects.create(name='Test Society', address='123 Test St')
        self.building = Building.objects.create(name='A Wing', society=self.society)
        self.flat = Flat.objects.create(number='101', building=self.building)

    def test_admin_can_access_onboarding_view(self):
        """Admin should be able to see the onboarding page"""
        self.client.login(email='admin@esociety.com', password='testpassword')
        url = reverse('onboard_resident', kwargs={'user_id': self.pending_resident.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'residents/onboard_resident.html')

    def test_resident_cannot_access_onboarding_view(self):
        """A normal resident should be redirected if trying to access onboarding view"""
        self.client.login(email='resident@esociety.com', password='testpassword')
        url = reverse('onboard_resident', kwargs={'user_id': self.pending_resident.id})
        response = self.client.get(url)
        # Should redirect to resident dashboard
        self.assertEqual(response.status_code, 302)

    def test_onboarding_process_creates_profile(self):
        """Submitting the form should create a profile and assign the flat"""
        self.client.login(email='admin@esociety.com', password='testpassword')
        url = reverse('onboard_resident', kwargs={'user_id': self.pending_resident.id})
        
        response = self.client.post(url, {
            'flat': self.flat.id,
            'move_in_date': '2025-01-01'
        })
        
        # Should redirect to admin dashboard
        self.assertEqual(response.status_code, 302)
        
        # Verify the profile was created
        profile = ResidentProfile.objects.filter(user=self.pending_resident).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.flat, self.flat)
        self.assertEqual(str(profile.move_in_date), '2025-01-01')
